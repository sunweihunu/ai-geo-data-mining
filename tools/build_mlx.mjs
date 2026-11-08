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
 *   5. 重写 mkdocs.yml 中 «# === MLX NAV BEGIN/END ===» 标记之间的导航块；
 *   6. 若存在 MATLAB export 命令导出的运行输出（tools/export_mlx_outputs.m 生成，
 *      默认 ../Code_Mlx_export/<目录>/<文件名>.md），把其中已保存的命令行输出与
 *      图窗按代码内容对齐注入页面，图文并茂；无导出或无输出时行为同旧版。
 *
 * 运行：node tools/build_mlx.mjs [mlx源目录] [export输出目录]
 *      （在仓库根目录执行；docs/mlx/ 为生成物，勿手改）
 */
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';

const ROOT = path.resolve(import.meta.dirname, '..');
const MLX_ROOT = path.resolve(process.argv[2] ?? path.join(ROOT, '..', 'Code_Mlx'));
const EXP_ROOT = path.resolve(process.argv[3] ?? path.join(ROOT, '..', 'Code_Mlx_export'));
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

const escapeHtml = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

/* ---------------- MATLAB export 导出的运行输出（tools/export_mlx_outputs.m 产物） ---------------- */

/**
 * 解析 export(Format="markdown") 的产物：每个 ```matlab 代码围栏为一个单元，
 * 紧随其后的 ```matlabTextOutput（命令行输出）与图片行（图窗）归属该单元，
 * 其余（文字段落转成的 # 标题等）忽略——文字由 .mlx 的 document.xml 提取。
 * 返回 [{code: string[], out: string[]}]，out 为可直接插入页面的 Markdown 片段。
 */
function parseExportUnits(txt, base) {
  const units = [];
  let figNo = 0;
  const lines = txt.split(/\r?\n/);
  let i = 0;
  while (i < lines.length) {
    const m = lines[i].match(/^```(\S*)\s*$/);
    if (!m || m[1] !== 'matlab') { i++; continue; }
    const unit = { code: [], out: [] };
    for (i++; i < lines.length && !/^```\s*$/.test(lines[i]); i++) unit.code.push(lines[i]);
    i++;                                     // 跳过代码围栏收尾
    // 单元输出区：直到下一 ```matlab 代码段为止；其间收集图窗与 matlabTextOutput
    while (i < lines.length) {
      const line = lines[i].trim();
      if (/^```matlab\s*$/.test(line)) break;                       // 新代码段，交回主循环（不跳过）
      if (!line || /^```(?!matlabTextOutput)/.test(line)) { i++; continue; }
      const m2 = line.match(/^!\[([^\]]*)\]\(([^)]+)\)$/);
      if (m2) {
        figNo++;
        const mediaRef = encPath(`../${base}_media/${path.basename(m2[2])}`);
        // 用原始 <img> 而非 Markdown 图片：mkdocs 的链接校验按文件相对路径解析，
        // 而目录式 URL 下浏览器按页面 URL（深一层）解析，Markdown 图片会误报死链
        unit.out.push(`<img src="${mediaRef}" alt="图窗 ${figNo}" loading="lazy" />`);
        i++; continue;
      }
      if (/^```matlabTextOutput\s*$/.test(line)) {                  // 命令行输出
        const buf2 = [];
        for (i++; i < lines.length && !/^```\s*$/.test(lines[i]); i++) buf2.push(lines[i]);
        i++;                                                        // 跳过收尾围栏
        const t = buf2.join('\n').replace(/\s+$/, '');
        if (t) unit.out.push(`<pre class="mlx-out">${escapeHtml(t)}</pre>`);
        continue;
      }
      i++;
    }
    units.push(unit);
  }
  return units;
}

/**
 * 把导出单元按代码内容对齐到 .mlx 的代码段落上：逐单元在剩余代码行序列中找连续
 * 匹配段（两侧都做 GBK 还原；匹配分三档——行 trim 精确、去空白后精确、少量字符
 * 差异的近似，并允许跳过被导出器挪到围栏外的行）。匹配不上的单元归入 orphan
 * （页尾统一以「运行输出（未对齐部分）」小节补出）。
 */
function alignUnits(paras, units) {
  const SKIP = 6, SIM_T = 0.2;
  const xmlLines = [];
  paras.forEach((p, pi) => {
    if (p.style !== 'code') return;
    p.text.split(/\r?\n/).forEach((ln, li) => {
      if (!ln.trim()) return;
      const fixed = fixMojibake(ln);
      xmlLines.push({ pi, li, norm: fixed.trim(), loose: fixed.replace(/\s+/g, '') });
    });
  });
  const unitOfXml = new Array(xmlLines.length).fill(null);
  const taken = new Array(xmlLines.length).fill(false);
  const orphan = [];
  let cur = 0;
  const simOk = (a, b) => {
    if (!a || !b || Math.abs(a.length - b.length) > 3) return false;
    if (a.includes(b) || b.includes(a)) return true;      // 导出器偶尔在行首/行尾混入残字符
    let d = 0;
    for (let k = 0; k < Math.max(a.length, b.length); k++) if (a[k] !== b[k]) d++;
    return d / Math.max(a.length, b.length, 1) <= SIM_T;
  };
  // 逐围栏行匹配一个起点偏移 off；严格（exact/loose/相似）都要求逐行连续命中
  const tryMatch = (uN, from, mode) => {
    let i = from;
    for (const ln of uN) {
      const looseN = ln.replace(/\s+/g, '');
      let p = -1;
      if (mode === 'scan') {                              // 兜底：允许跳过少量未命中的 XML 行
        for (let k = i; k < Math.min(xmlLines.length, i + SKIP); k++) {
          if (taken[k]) continue;
          if (xmlLines[k].norm === ln || xmlLines[k].loose === looseN || simOk(xmlLines[k].loose, looseN)) { p = k; break; }
        }
      } else {
        if (i >= xmlLines.length) return null;
        const x = xmlLines[i];
        const hit = mode === 'exact' ? x.norm === ln
          : mode === 'loose' ? x.loose === looseN
          : simOk(x.loose, looseN);
        if (hit && !taken[i]) p = i;
      }
      if (p < 0) return null;
      i = p + 1;
    }
    return i;                                             // 匹配区间终点
  };
  for (const u of units) {
    const uN = u.code.map((l) => fixMojibake(l).trim()).filter(Boolean);
    if (!uN.length) continue;
    let end = null;
    for (const mode of ['exact', 'loose', 'sim', 'scan']) {
      end = tryMatch(uN, cur, mode);
      if (end !== null) break;
    }
    if (end === null) { orphan.push(u); continue; }
    for (let k = cur; k < end; k++) { unitOfXml[k] = u; taken[k] = true; }
    cur = end;
  }
  // 摊平到段落行：paraLineUnits.get(pi)[li] = unit|null
  const paraLineUnits = new Map();
  xmlLines.forEach(({ pi, li }, idx) => {
    if (!unitOfXml[idx]) return;
    if (!paraLineUnits.has(pi)) paraLineUnits.set(pi, []);
    paraLineUnits.get(pi)[li] = unitOfXml[idx];
  });
  return { paraLineUnits, orphan };
}

/* ---------------- 主流程 ---------------- */

console.log(`== 读取 ${MLX_ROOT} ==`);
fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(SRC, { recursive: true });
fs.mkdirSync(DL, { recursive: true });

const navLines = [];
let totalFiles = 0, totalBytes = 0;
let totalFig = 0, totalOut = 0, totalPlain = 0;
if (!fs.existsSync(EXP_ROOT)) console.warn(`  !! 未找到运行输出目录 ${EXP_ROOT}（可用 MATLAB 跑 tools/export_mlx_outputs.m 生成）；页面将仅含代码与文字`);

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
      const base = name.replace(/\.mlx$/i, '');
      // MATLAB export 的运行输出（可选）：解析 + 按代码内容对齐（导出无输出则不注入）
      let units = null, paraLineUnits = null, orphan = [];
      const expPath = path.join(EXP_ROOT, folder.id, `${base}.md`);
      if (fs.existsSync(expPath)) {
        const parsed = parseExportUnits(fs.readFileSync(expPath, 'utf8'), base);
        if (parsed.some((u) => u.out.length)) {
          units = parsed;
          ({ paraLineUnits, orphan } = alignUnits(paras, units));
          if (orphan.length) console.warn(`  !! ${folder.id}/${name} 有 ${orphan.length} 个单元未能对齐到代码段`);
        }
      }
      const figCount = units ? units.reduce((a, u) => a + u.out.filter((s) => s.startsWith('<img')).length, 0) : 0;
      const outCount = units ? units.reduce((a, u) => a + u.out.filter((s) => !s.startsWith('<img')).length, 0) : 0;
      files.push({ name, buf, paras, title, desc: meta.desc, codeLines, size: buf.length, base, units, paraLineUnits, orphan, figCount, outCount });
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
  let nFig = 0, nOut = 0, nPlain = 0;
  for (const f of files) {
    if (f.figCount) nFig++; else if (f.outCount) nOut++; else nPlain++;
    totalFig += f.figCount;
    const base = f.base;
    // 图窗媒体文件（可选）
    if (f.figCount) {
      const mediaSrc = path.join(EXP_ROOT, folder.id, `${base}_media`);
      if (fs.existsSync(mediaSrc)) fs.cpSync(mediaSrc, path.join(OUT, folder.id, `${base}_media`), { recursive: true });
    }
    const md = [];
    md.push(`# ${f.name}`, '');
    const extras = [f.figCount ? `图窗 ${f.figCount}` : '', !f.figCount && f.outCount ? `运行输出 ${f.outCount}` : '']
      .filter(Boolean).join(' · ');
    md.push(`「${folder.label}」目录 · 对应书稿 **${folder.chapter}** · ${humanSize(f.size)} · 代码 ${f.codeLines} 行${extras ? ` · ${extras}` : ''}`, '');
    const matlabUrl = `https://matlab.mathworks.com/open/github/v1?repo=${GITHUB_REPO}&file=docs/mlx/src/${folder.id}/${f.name}`;
    md.push(`<p class="refcode-actions"><a class="md-button" href="${matlabUrl}" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="${encPath(`../../src/${folder.id}/${f.name}`)}" download>下载 ${f.name}</a></p>`, '');
    if (f.figCount || f.outCount) {
      md.push('!!! tip "MATLAB 实时脚本（.mlx）"',
        '',
        '    本页展示脚本内的文字说明与代码，并嵌入由 MATLAB `export` 命令从 .mlx 导出的运行结果——命令行输出与图窗均取自作者在实时脚本中保存的内容。「复制代码」仅复制脚本代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。', '');
    } else {
      md.push('!!! tip "MATLAB 实时脚本（.mlx）"',
        '',
        '    本页是该实时脚本内代码与文字的网页摘录（脚本保存时未存运行输出，故无结果展示；在 MATLAB 中运行即可查看）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。', '');
    }
    if (f.title) md.push(`**${f.title}**`, '');
    if (f.desc) md.push(f.desc, '');
    md.push('## 脚本内容', '');
    // 按文档顺序渲染；相邻代码段合并为一个代码块；代码单元切换处切分并注入输出
    let codeBuf = null;      // { lines: string[], unit: object|null, paraStart: boolean }
    const flush = () => {
      if (!codeBuf) return;
      const code = codeBuf.lines.join('\n').split('\n').map((l) => l.replace(/\s+$/, '')).join('\n')
        .replace(/^\n+/, '').replace(/\s+$/, '');
      if (code) {
        const bt = fence(code);
        md.push(`${bt}matlab`, ...code.split('\n'), `${bt}`, '');
      }
      if (codeBuf.unit) for (const c of codeBuf.unit.out) md.push(c, '');
      codeBuf = null;
    };
    f.paras.forEach((p, pi) => {
      if (p.style === 'code') {
        const lu = f.paraLineUnits?.get(pi);
        p.text.split(/\r?\n/).forEach((ln, li) => {
          const u = lu?.[li] ?? null;
          const blank = !/\S/.test(ln);
          if (codeBuf === null) codeBuf = { lines: [], unit: blank ? null : u };
          else if (!blank && (codeBuf.unit ?? null) !== (u ?? null)) { flush(); codeBuf = { lines: [], unit: u }; } // 空行不切分代码块
          else if (li === 0 && codeBuf.lines.length) codeBuf.lines.push('');   // 相邻代码段落之间保留一个空行（同旧版）
          codeBuf.lines.push(ln);
        });
        return;
      }
      flush();
      const t = p.text.trim();
      if (!t) return;
      if (p.style === 'heading' || p.style === 'title') md.push(`## ${t}`, '');
      else md.push(mdText(p.text.trimEnd()), '');
    });
    flush();
    // 未能对齐到代码段的输出，附于页尾
    if (f.orphan?.some((u) => u.out.length)) {
      md.push('## 运行输出（未对齐部分）', '');
      for (const u of f.orphan) for (const c of u.out) md.push(c, '');
    }
    fs.writeFileSync(path.join(OUT, folder.id, `${base}.md`), md.join('\n'), 'utf8');
  }

  // 4) 目录汇总页
  const idx = [];
  idx.push(`# ${folder.label} · MLX 实时脚本`, '');
  idx.push(`对应书稿 **${folder.chapter}**。本目录共 ${files.length} 个 MATLAB 实时脚本${datas.length ? `，另有 ${datas.length} 个数据文件` : ''}，来自课程源文件夹 \`Code_Mlx/${folder.id}\`。`, '');
  idx.push(`[⬇ 打包下载 ${zipName}](../downloads/${encodeURIComponent(zipName)}){ .md-button }　单文件下载与在线打开见各脚本页面。`, '');
  idx.push('| 脚本 | 说明 | 代码行 | 图窗 | 大小 |', '|------|------|-------:|-------:|-----:|');
  for (const f of files) {
    const base = f.name.replace(/\.mlx$/i, '');
    const t = (f.title || '—').replace(/\|/g, '\\|').slice(0, 60);
    idx.push(`| [${f.name}](${encPath(`../${folder.id}/${base}.md`)}) | ${t} | ${f.codeLines} | ${f.figCount || '—'} | ${humanSize(f.size)} |`);
  }
  for (const d of datas) {
    idx.push(`| [${d.name}](${encPath(`../src/${folder.id}/${d.name}`)})（数据文件，直接下载） | — | — | — | ${humanSize(d.size)} |`);
  }
  fs.mkdirSync(path.join(OUT, folder.id), { recursive: true });
  fs.writeFileSync(path.join(OUT, folder.id, 'index.md'), idx.join('\n'), 'utf8');
  console.log(`  ${folder.id}（${folder.label}）: ${files.length} 个脚本 + ${datas.length} 个数据文件 -> index + 页面 + ${zipName}　[图窗 ${nFig} / 仅文本输出 ${nOut} / 无输出 ${nPlain}]`);
  totalOut += nOut; totalPlain += nPlain;

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
ov.push('这里收录课程配套的 **MATLAB 实时脚本（Live Script，.mlx）**：代码、文字说明与运行结果在同一文档中交替呈现，适合边看边运行。每个脚本有单独页面展示其代码、文字说明与作者保存的运行结果（命令行输出与图窗），并提供「在 MATLAB Online 中打开」「复制代码」「下载」三种操作。', '');
ov.push('| 目录 | 对应章节 | 脚本数 | 打包下载 |', '|------|----------|-------:|----------|');
for (const folder of FOLDERS) {
  const n = fs.readdirSync(path.join(SRC, folder.id)).filter((f) => f.toLowerCase().endsWith('.mlx')).length;
  ov.push(`| [${folder.label}](./${encPath(`${folder.id}/index.md`)}) | ${folder.chapter} | ${n} | [MLX_${folder.id}.zip](downloads/${encodeURIComponent(`MLX_${folder.id}.zip`)}) |`);
}
ov.push('', '## 使用说明', '');
ov.push('1. **运行环境**：实时脚本需 MATLAB R2016a 及以上版本；多数脚本依赖 Statistics and Machine Learning Toolbox，第09章 `ANN_01–27` 使用较旧的神经网络工具箱函数（`newff`、`trainlm` 等），较新版本中仍可用。第11章（DeepL_V2）需 **Deep Learning Toolbox**，`Cam_*` / `Img_*` 首次运行会提示安装预训练网络与摄像头支持包；`seq_LSTM_Reg_V2_seq` 需 C-MAPSS 数据集（可在「参考代码」板块第11章页面下载 CMAPSSData.zip）。');
ov.push('2. **三种操作**：「在 MATLAB Online 中打开」在本站仓库推送 GitHub 后生效（需登录 MathWorks 账号）；「复制代码」把脚本全部代码复制到剪贴板；「下载」保存原始 .mlx 文件，在本地 MATLAB 中直接打开。');
ov.push(`3. **网页内容**：页面由脚本源文件（文字与代码）加 MATLAB \`export\` 命令导出的运行结果自动生成——凡作者保存过输出的脚本，页面嵌入其命令行输出与图窗（本板块 ${totalFig} 个脚本带图窗、${totalOut} 个仅带文本输出；第11章深度学习脚本保存时未存输出，页面仅展示代码与文字）。早期脚本中的中文注释在网页展示时已做编码还原，原始文件未做任何改动。`);
ov.push('4. **与「参考代码」板块的关系**：本板块的实时脚本与[参考代码](../refcode/index.md)中的 .m 脚本同源（如 `ANN_01_Lin.mlx` 与 `ANN_01_Lin.m`），.mlx 版本保留原讲义排版，适合对照书稿阅读。');
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
