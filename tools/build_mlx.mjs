#!/usr/bin/env node
/**
 * build_mlx.mjs —— 「MLX 实时脚本」网站板块一键生成
 *
 * 从站外源目录（默认 ../Code_Mlx，可用第一个命令行参数覆盖）中的 .mlx 文件出发：
 *   1. 纯 Node 解出每个 .mlx（OPC zip 包）内 matlab/document.xml 的段落
 *      （pStyle = title / heading / text / code），并把「GBK 字节被当作 Latin-1 存入
 *      XML」的旧文件正文还原为中文（新文件本身是 UTF-8，不受影响）；
 *   2. 原始 .mlx 原样复制到 docs/mlx/src/<目录>/，供下载与 MATLAB Online 打开；
 *   3. 为每个 .mlx 生成单独页面 docs/mlx/<目录>/<文件名>.md，为每个目录生成
 *      汇总页 docs/mlx/<目录>/index.md，并生成总览页 docs/mlx/index.md；
 *   4. 每个目录打包一个 zip（UTF-8 文件名）到 docs/mlx/downloads/；
 *   5. 重写 mkdocs.yml 中 «# === MLX NAV BEGIN/END ===» 标记之间的导航块。
 *
 * 运行：node tools/build_mlx.mjs   （在仓库根目录执行；docs/mlx/ 为生成物，勿手改）
 */
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';

const ROOT = path.resolve(import.meta.dirname, '..');
const MLX_ROOT = path.resolve(process.argv[2] ?? path.join(ROOT, '..', 'Code_Mlx'));
const OUT = path.join(ROOT, 'docs', 'mlx');
const SRC = path.join(OUT, 'src');
const DL = path.join(OUT, 'downloads');
const MKDOCS_YML = path.join(ROOT, 'mkdocs.yml');
/** 「在 MATLAB Online 中打开」按钮指向的 GitHub 仓库（owner/repo）；仓库推送后按钮即生效 */
const GITHUB_REPO = 'sunweihunu/ai-geo-data-mining';

const gbkDec = new TextDecoder('gbk');

/* ---------------- 目录清单（顺序即导航顺序，对应书稿章节） ---------------- */

const FOLDERS = [
  { id: 'DR', label: '降维（DR）', chapter: '第05章 降维', sub: 'Code_DR' },
  { id: 'LDA', label: '判别分析（LDA）', chapter: '第06章 线性模型', sub: 'Code_LDA' },
  { id: 'kNN', label: 'k 最近邻（kNN）', chapter: '第07章 k最近邻（kNN）模型', sub: '' },
  { id: 'DecisionTree_v2', label: '决策树（CART）', chapter: '第08章 决策树', sub: '' },
  { id: 'ANN', label: '人工神经网络（ANN）', chapter: '第09章 人工神经网络', sub: '' },
  { id: 'SVM_V1', label: '支持向量机（SVM）', chapter: '第10章 支持向量机', sub: '' },
  { id: 'DeepL_V2', label: '深度学习（DeepL）', chapter: '第11章 深度学习', sub: '' },
];

/** 个别脚本自动提取的标题可读性差，按 .mlx 文件名人工覆盖（仅限此处，勿按内容硬编码） */
const titleOverrides = {
  'half.mlx': '涡扇发动机 RUL 预测 · 测试评估段',
};

/* ---------------- zip 读取（仅读单一条目）与打包 ---------------- */

function readEntry(buf, want) {
  let eocd = buf.length - 22;
  while (eocd >= 0 && buf.readUInt32LE(eocd) !== 0x06054b50) eocd--;
  if (eocd < 0) return null;
  const count = buf.readUInt16LE(eocd + 10);
  let off = buf.readUInt32LE(eocd + 16);
  for (let n = 0; n < count; n++) {
    if (buf.readUInt32LE(off) !== 0x02014b50) return null;
    const flags = buf.readUInt16LE(off + 8);
    const method = buf.readUInt16LE(off + 10);
    const csize = buf.readUInt32LE(off + 20);
    const nameLen = buf.readUInt16LE(off + 28);
    const extraLen = buf.readUInt16LE(off + 30);
    const commentLen = buf.readUInt16LE(off + 32);
    const lho = buf.readUInt32LE(off + 42);
    const nameBuf = buf.subarray(off + 46, off + 46 + nameLen);
    const name = (flags & 0x800) ? nameBuf.toString('utf8') : gbkDec.decode(nameBuf);
    if (name.replace(/\\/g, '/') === want) {
      const lnLen = buf.readUInt16LE(lho + 26);
      const leLen = buf.readUInt16LE(lho + 28);
      const dataStart = lho + 30 + lnLen + leLen;
      const raw = buf.subarray(dataStart, dataStart + csize);
      return method === 0 ? Buffer.from(raw) : zlib.inflateRawSync(raw);
    }
    off += 46 + nameLen + extraLen + commentLen;
  }
  return null;
}

function crc32(buf) {
  let c, table = crc32.table;
  if (!table) {
    table = crc32.table = new Int32Array(256);
    for (let n = 0; n < 256; n++) {
      c = n;
      for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
      table[n] = c;
    }
  }
  c = -1;
  for (let i = 0; i < buf.length; i++) c = (c >>> 8) ^ table[(c ^ buf[i]) & 0xff];
  return (c ^ -1) >>> 0;
}

/** 生成仅 store（不压缩）的 zip，全部条目带 UTF-8 标志，跨平台文件名不乱码 */
function makeZip(files) {
  const chunks = [], central = [];
  let offset = 0;
  for (const { name, data } of files) {
    const nb = Buffer.from(name, 'utf8');
    const crc = crc32(data);
    const local = Buffer.alloc(30);
    local.writeUInt32LE(0x04034b50, 0);
    local.writeUInt16LE(0x0800, 6);              // UTF-8 文件名
    local.writeUInt16LE(0, 8);                   // store
    local.writeUInt32LE(crc, 14);
    local.writeUInt32LE(data.length, 18);
    local.writeUInt32LE(data.length, 22);
    local.writeUInt16LE(nb.length, 26);
    chunks.push(local, nb, data);
    const cd = Buffer.alloc(46);
    cd.writeUInt32LE(0x02014b50, 0);
    cd.writeUInt16LE(0x0800, 8);
    cd.writeUInt16LE(0, 10);
    cd.writeUInt32LE(crc, 16);
    cd.writeUInt32LE(data.length, 20);
    cd.writeUInt32LE(data.length, 24);
    cd.writeUInt16LE(nb.length, 28);
    cd.writeUInt32LE(offset, 42);
    central.push(cd, nb);
    offset += 30 + nb.length + data.length;
  }
  const cdBuf = Buffer.concat(central);
  const end = Buffer.alloc(22);
  end.writeUInt32LE(0x06054b50, 0);
  end.writeUInt16LE(files.length, 8);
  end.writeUInt16LE(files.length, 10);
  end.writeUInt32LE(cdBuf.length, 12);
  end.writeUInt32LE(offset, 16);
  return Buffer.concat([...chunks, cdBuf, end]);
}

/* ---------------- mlx document.xml 解析 ---------------- */

function stripCdata(s) {
  return s.startsWith('<![CDATA[') ? s.slice(9, s.endsWith(']]>') ? -3 : undefined) : s;
}

function xmlText(s) {
  return stripCdata(s)
    .replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&apos;/g, "'")
    .replace(/&#(\d+);/g, (_, d) => String.fromCodePoint(+d))
    .replace(/&amp;/g, '&');
}

/** 旧版 MATLAB 把 GBK 正文的每个字节当 Latin-1 字符存进 UTF-8 XML；
 *  特征是全文都落在 U+0080–U+00FF 区间，把字符还原回字节再按 GBK 解码即可 */
function fixMojibake(s) {
  if (!/[\x80-\xff]/.test(s)) return s;
  const bytes = [];
  for (const ch of s) {
    const c = ch.codePointAt(0);
    if (c >= 256) return s;
    bytes.push(c);
  }
  return gbkDec.decode(Buffer.from(bytes));
}

/** 解析 document.xml，返回按文档顺序的段落 [{style, text}] */
function parseParagraphs(docBuf) {
  let xml;
  try { xml = new TextDecoder('utf-8', { fatal: true }).decode(docBuf); }
  catch { xml = gbkDec.decode(docBuf); }
  const paras = [];
  for (const m of xml.matchAll(/<w:p(?:\s[^>]*)?>([\s\S]*?)<\/w:p>/g)) {
    const body = m[1];
    const style = body.match(/<w:pStyle w:val="([^"]+)"/)?.[1] ?? '(none)';
    const text = fixMojibake(
      [...body.matchAll(/<w:t(?:\s[^>]*)?>([\s\S]*?)<\/w:t>|<w:t\/>/g)]
        .map((t) => (t[1] ? xmlText(t[1]) : '')).join(''),
    );
    paras.push({ style, text });
  }
  return paras;
}

/** 纯装饰性分隔线：去掉行首 % 后只由分隔字符与空白组成且总长度 ≥ 6（如 % ============）；
 *  以及两侧各由 ≥12 个分隔字符包夹的长横幅行（如 cart_exp04/08 的
 *  % ====== 注释中英文对照 ======，两侧各 16 个 =）——均为装饰性分隔注释，不作标题。
 *  短包夹（两侧 <12）通常是「====== 标题 ======」式带框标题，保留（如 knn_sip1/2） */
const isDecorative = (c) =>
  /^[=\-_*~·—–\s]{6,}$/.test(c) ||
  /^[=\-_*~·—–\s]{12,}[\s\S]*[=\-_*~·—–\s]{12,}$/.test(c);

/** 从段落中取展示标题与说明：优先 title 段落，否则取首段代码开头连续的注释行（跳过装饰性分隔线） */
function extractMeta(paras) {
  const titlePara = paras.find((p) => p.style === 'title' && p.text.trim());
  const firstCode = paras.find((p) => p.style === 'code' && p.text.trim());
  if (titlePara) return { title: titlePara.text.trim(), desc: '' };
  if (!firstCode) return { title: '', desc: '' };
  const lines = firstCode.text.split(/\r?\n/);
  let start = lines.findIndex((l) => /^\s*%/.test(l));
  if (start < 0) return { title: '', desc: '' };
  const comments = [];
  for (let i = start; i < lines.length && /^\s*%/.test(lines[i]); i++) {
    const c = lines[i].replace(/^\s*%+\s?/, '').trim();
    if (c && !isDecorative(c)) comments.push(c);
  }
  return { title: comments[0] ?? '', desc: comments.slice(1, 3).join(' ') };
}

/* ---------------- 文本工具 ---------------- */

function humanSize(n) {
  return n >= 1048576 ? `${(n / 1048576).toFixed(1)} MB` : `${(n / 1024).toFixed(1)} KB`;
}

const encPath = (p) => p.split('/').map(encodeURIComponent).join('/');

/** 围栏长度取比代码中最长反引号串更长的一档 */
function fence(code) {
  const longest = Math.max(0, ...[...code.matchAll(/`+/g)].map((m) => m[0].length));
  return '`'.repeat(Math.max(3, longest + 1));
}

/** 文字段落转 Markdown：规避行首被解析成标题/列表/引用 */
function mdText(s) {
  return s.split(/\r?\n/).map((l) => l.replace(/^(#{1,6}\s|>\s|[-*+]\s|\d+\.\s)/, '\\$1')).join('\n');
}

/* ---------------- 主流程 ---------------- */

console.log(`== 读取 ${MLX_ROOT} ==`);
fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(SRC, { recursive: true });
fs.mkdirSync(DL, { recursive: true });

const navLines = [];
let totalFiles = 0, totalBytes = 0;

for (const folder of FOLDERS) {
  const srcDir = path.join(MLX_ROOT, folder.id, folder.sub);
  if (!fs.existsSync(srcDir)) { console.error(`  !! 目录不存在: ${srcDir}`); process.exit(1); }

  const entries = fs.readdirSync(srcDir).sort((a, b) => a.localeCompare(b, 'zh', { numeric: true }));
  const files = [], datas = [];
  for (const name of entries) {
    const buf = fs.readFileSync(path.join(srcDir, name));
    if (name.toLowerCase().endsWith('.mlx')) {
      const paras = parseParagraphs(readEntry(buf, 'matlab/document.xml') ?? Buffer.alloc(0));
      if (!paras.some((p) => p.style === 'code')) console.warn(`  !! ${folder.id}/${name} 未提取到代码段`);
      const meta = extractMeta(paras);
      const title = titleOverrides[name] ?? meta.title;
      const codeLines = paras.filter((p) => p.style === 'code')
        .reduce((a, p) => a + p.text.split(/\r?\n/).length, 0);
      files.push({ name, buf, paras, title, desc: meta.desc, codeLines, size: buf.length });
    } else {
      datas.push({ name, buf, size: buf.length });
    }
  }

  // 1) 原样复制源文件
  fs.mkdirSync(path.join(SRC, folder.id), { recursive: true });
  for (const f of [...files, ...datas]) {
    fs.writeFileSync(path.join(SRC, folder.id, f.name), f.buf);
    totalFiles++; totalBytes += f.size;
  }

  // 2) 每目录打包 zip
  const zipName = `MLX_${folder.id}.zip`;
  fs.writeFileSync(
    path.join(DL, zipName),
    makeZip([...files, ...datas].map((f) => ({ name: `${folder.id}/${f.name}`, data: f.buf }))),
  );

  // 3) 每个文件单独页面
  fs.mkdirSync(path.join(OUT, folder.id), { recursive: true });
  for (const f of files) {
    const base = f.name.replace(/\.mlx$/i, '');
    const md = [];
    md.push(`# ${f.name}`, '');
    md.push(`「${folder.label}」目录 · 对应书稿 **${folder.chapter}** · ${humanSize(f.size)} · 代码 ${f.codeLines} 行`, '');
    const matlabUrl = `https://matlab.mathworks.com/open/github/v1?repo=${GITHUB_REPO}&file=docs/mlx/src/${folder.id}/${f.name}`;
    md.push(`<p class="refcode-actions"><a class="md-button" href="${matlabUrl}" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="${encPath(`../src/${folder.id}/${f.name}`)}" download>下载 ${f.name}</a></p>`, '');
    md.push('!!! tip "MATLAB 实时脚本（.mlx）"',
      '',
      '    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。', '');
    if (f.title) md.push(`**${f.title}**`, '');
    if (f.desc) md.push(f.desc, '');
    md.push('## 脚本内容', '');
    // 按文档顺序渲染；相邻代码段合并为一个代码块
    let buf = null;
    const flush = () => {
      if (!buf) return;
      const code = buf.replace(/\r\n/g, '\n').split('\n').map((l) => l.replace(/\s+$/, '')).join('\n')
        .replace(/^\n+/, '').replace(/\n+$/, '\n').trimEnd();
      if (code) {
        const bt = fence(code);
        md.push(`${bt}matlab`, ...code.split('\n'), `${bt}`, '');
      }
      buf = null;
    };
    for (const p of f.paras) {
      if (p.style === 'code') { buf = buf === null ? p.text : `${buf}\n\n${p.text}`; continue; }
      flush();
      const t = p.text.trim();
      if (!t) continue;
      if (p.style === 'heading' || p.style === 'title') md.push(`## ${t}`, '');
      else md.push(mdText(p.text.trimEnd()), '');
    }
    flush();
    fs.writeFileSync(path.join(OUT, folder.id, `${base}.md`), md.join('\n'), 'utf8');
  }

  // 4) 目录汇总页
  const idx = [];
  idx.push(`# ${folder.label} · MLX 实时脚本`, '');
  idx.push(`对应书稿 **${folder.chapter}**。本目录共 ${files.length} 个 MATLAB 实时脚本${datas.length ? `，另有 ${datas.length} 个数据文件` : ''}，来自课程源文件夹 \`Code_Mlx/${folder.id}\`。`, '');
  idx.push(`[⬇ 打包下载 ${zipName}](../downloads/${encodeURIComponent(zipName)}){ .md-button }　单文件下载与在线打开见各脚本页面。`, '');
  idx.push('| 脚本 | 说明 | 代码行 | 大小 |', '|------|------|-------:|-----:|');
  for (const f of files) {
    const base = f.name.replace(/\.mlx$/i, '');
    const t = (f.title || '—').replace(/\|/g, '\\|').slice(0, 60);
    idx.push(`| [${f.name}](${encPath(`../${folder.id}/${base}.md`)}) | ${t} | ${f.codeLines} | ${humanSize(f.size)} |`);
  }
  for (const d of datas) {
    idx.push(`| [${d.name}](${encPath(`../src/${folder.id}/${d.name}`)})（数据文件，直接下载） | — | — | ${humanSize(d.size)} |`);
  }
  fs.mkdirSync(path.join(OUT, folder.id), { recursive: true });
  fs.writeFileSync(path.join(OUT, folder.id, 'index.md'), idx.join('\n'), 'utf8');
  console.log(`  ${folder.id}（${folder.label}）: ${files.length} 个脚本 + ${datas.length} 个数据文件 -> ${folder.id}/index.md + ${files.length} 个页面 + ${zipName}`);

  // 5) 导航块
  navLines.push(`      - ${folder.label}:`, `          - mlx/${folder.id}/index.md`);
  for (const f of files) {
    const base = f.name.replace(/\.mlx$/i, '');
    navLines.push(`          - ${base}: mlx/${folder.id}/${base}.md`);
  }
}

// 6) 总览页
const ov = [];
ov.push('# MLX 实时脚本总览', '');
ov.push('这里收录课程配套的 **MATLAB 实时脚本（Live Script，.mlx）**：代码、文字说明与运行结果在同一文档中交替呈现，适合边看边运行。每个脚本有单独页面展示其代码与说明，并提供「在 MATLAB Online 中打开」「复制代码」「下载」三种操作。', '');
ov.push('| 目录 | 对应章节 | 脚本数 | 打包下载 |', '|------|----------|-------:|----------|');
for (const folder of FOLDERS) {
  const n = fs.readdirSync(path.join(SRC, folder.id)).filter((f) => f.toLowerCase().endsWith('.mlx')).length;
  ov.push(`| [${folder.label}](./${encPath(`${folder.id}/index.md`)}) | ${folder.chapter} | ${n} | [MLX_${folder.id}.zip](downloads/${encodeURIComponent(`MLX_${folder.id}.zip`)}) |`);
}
ov.push('', '## 使用说明', '');
ov.push('1. **运行环境**：实时脚本需 MATLAB R2016a 及以上版本；多数脚本依赖 Statistics and Machine Learning Toolbox，第09章 `ANN_01–27` 使用较旧的神经网络工具箱函数（`newff`、`trainlm` 等），较新版本中仍可用。第11章（DeepL_V2）需 **Deep Learning Toolbox**，`Cam_*` / `Img_*` 首次运行会提示安装预训练网络与摄像头支持包；`seq_LSTM_Reg_V2_seq` 需 C-MAPSS 数据集（可在「参考代码」板块第11章页面下载 CMAPSSData.zip）。');
ov.push('2. **三种操作**：「在 MATLAB Online 中打开」在本站仓库推送 GitHub 后生效（需登录 MathWorks 账号）；「复制代码」把脚本全部代码复制到剪贴板；「下载」保存原始 .mlx 文件，在本地 MATLAB 中直接打开。');
ov.push('3. **网页摘录说明**：页面展示脚本中的代码与文字说明；运行输出（命令行结果与图窗）保存在 .mlx 内部，不随网页展示，打开原文件即可看到。早期脚本中的中文注释在网页展示时已做编码还原，原始文件未做任何改动。');
ov.push('4. **与「参考代码」板块的关系**：本板块的实时脚本与[参考代码](../refcode/)中的 .m 脚本同源（如 `ANN_01_Lin.mlx` 与 `ANN_01_Lin.m`），.mlx 版本保留原讲义排版，适合对照书稿阅读。');
fs.writeFileSync(path.join(OUT, 'index.md'), ov.join('\n'), 'utf8');
console.log('  index.md 生成完毕');

// 7) 重写 mkdocs.yml 导航块
let yml = fs.readFileSync(MKDOCS_YML, 'utf8');
const BEGIN = '      # === MLX NAV BEGIN（由 tools/build_mlx.mjs 生成，勿手改） ===';
const END = '      # === MLX NAV END ===';
const block = [BEGIN, ...navLines, END].join('\n');
const b = yml.indexOf(BEGIN), e = yml.indexOf(END);
if (b >= 0 && e > b) {
  yml = yml.slice(0, b) + block + yml.slice(e + END.length);
} else if (b < 0 && e < 0) {
  console.error('!! mkdocs.yml 中缺少 MLX NAV BEGIN/END 标记，请先在 nav 的「MLX 实时脚本」小节恢复标记'); process.exit(1);
} else {
  console.error('!! mkdocs.yml 中 MLX NAV 标记不成对'); process.exit(1);
}
fs.writeFileSync(MKDOCS_YML, yml, 'utf8');

console.log(`== 完成 == 共 ${totalFiles} 个文件（${(totalBytes / 1048576).toFixed(1)} MB）`);
