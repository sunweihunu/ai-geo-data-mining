#!/usr/bin/env node
/**
 * build_refcode.mjs —— 「参考代码」网站板块一键生成
 *
 * 从 refcode_archives/ 中的原始 zip 出发：
 *   1. 纯 Node 解压（支持嵌套 zip、GBK 文件名解码）；
 *   2. 源文件编码归一为 UTF-8（原始文件 GBK / UTF-8 各占一半）；
 *   3. 按清单分配到 docs/refcode/src/chXX/，并生成每章浏览页与总览页；
 *   4. 打包每章 zip（UTF-8 文件名，macOS/Linux 解压不乱码）到 docs/refcode/downloads/。
 *
 * 运行：node tools/build_refcode.mjs   （在仓库根目录执行）
 * 更新代码后重跑即可，输出完全覆盖重建。
 */
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';

const ROOT = path.resolve(import.meta.dirname, '..');
const ARCHIVES = path.join(ROOT, 'refcode_archives');
const OUT = path.join(ROOT, 'docs', 'refcode');
const SRC = path.join(OUT, 'src');
const DL = path.join(OUT, 'downloads');
/** 「在 MATLAB Online 中打开」按钮指向的 GitHub 仓库（owner/repo）；仓库发布后按钮即生效 */
const GITHUB_REPO = 'sunweihunu/ai-geo-data-mining';

const gbkDec = new TextDecoder('gbk');

/* ---------------- zip 读取（stored / deflate，含嵌套 zip 与 GBK 文件名） ---------------- */

function readZipEntries(buf) {
  let eocd = buf.length - 22;
  while (eocd >= 0 && buf.readUInt32LE(eocd) !== 0x06054b50) eocd--;
  if (eocd < 0) throw new Error('zip: End of Central Directory 未找到');
  const count = buf.readUInt16LE(eocd + 10);
  let off = buf.readUInt32LE(eocd + 16);
  const entries = [];
  for (let n = 0; n < count; n++) {
    if (buf.readUInt32LE(off) !== 0x02014b50) throw new Error('zip: Central Directory 损坏');
    const flags = buf.readUInt16LE(off + 8);
    const method = buf.readUInt16LE(off + 10);
    const csize = buf.readUInt32LE(off + 20);
    const nameLen = buf.readUInt16LE(off + 28);
    const extraLen = buf.readUInt16LE(off + 30);
    const commentLen = buf.readUInt16LE(off + 32);
    const lho = buf.readUInt32LE(off + 42);
    const nameBuf = buf.subarray(off + 46, off + 46 + nameLen);
    const name = (flags & 0x800) ? nameBuf.toString('utf8') : gbkDec.decode(nameBuf);
    const lnLen = buf.readUInt16LE(lho + 26);
    const leLen = buf.readUInt16LE(lho + 28);
    const dataStart = lho + 30 + lnLen + leLen;
    const raw = buf.subarray(dataStart, dataStart + csize);
    const data = method === 0 ? Buffer.from(raw) : zlib.inflateRawSync(raw);
    entries.push({ name: name.replace(/\\/g, '/'), data });
    off += 46 + nameLen + extraLen + commentLen;
  }
  return entries;
}

/** 递归展开 zip（zip 内还套 zip 时继续下钻），返回 [{vpath, data}] */
function expandZip(buf, prefix, out) {
  for (const e of readZipEntries(buf)) {
    if (e.dir || !e.data.length && e.name.endsWith('/')) continue;
    const vp = `${prefix}/${e.name}`;
    if (/\.zip$/i.test(e.name)) {
      expandZip(e.data, vp, out);
    } else {
      out.push({ vpath: vp, data: e.data });
    }
  }
  return out;
}

function loadAllArchives() {
  const all = [];
  for (const f of fs.readdirSync(ARCHIVES).sort()) {
    if (!/\.zip$/i.test(f)) continue;
    const entries = expandZip(fs.readFileSync(path.join(ARCHIVES, f)), f, []);
    console.log(`  ${f}: ${entries.length} 个文件`);
    all.push(...entries);
  }
  return all;
}

/* ---------------- 文本与元信息 ---------------- */

function decodeText(buf) {
  try { return { text: new TextDecoder('utf-8', { fatal: true }).decode(buf), enc: 'utf8' }; }
  catch { return { text: gbkDec.decode(buf), enc: 'gbk' }; }
}

/** 取文件开头的第一个连续注释块：首行为标题，其余为说明 */
function extractMeta(text) {
  const lines = text.split(/\r?\n/);
  let start = -1;
  for (let i = 0; i < Math.min(lines.length, 25); i++) {
    if (/^\s*%/.test(lines[i])) { start = i; break; }
  }
  if (start < 0) return { title: '', desc: '', lines: lines.length };
  const block = [];
  for (let i = start; i < lines.length && /^\s*%/.test(lines[i]); i++) {
    block.push(lines[i].replace(/^\s*%+\s?/, '').trim());
  }
  while (block.length && !block[block.length - 1]) block.pop();
  const title = block.shift() ?? '';
  const desc = block.filter(Boolean).slice(0, 6).join(' ');
  return { title, desc, lines: lines.length };
}

/* ---------------- 打包（store 方式 + UTF-8 文件名标志位） ---------------- */

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

/* ---------------- 章节清单 ---------------- */

const CHAPTERS = [
  {
    id: 'ch04', zip: 'Cluster_Analysis.zip', label: '聚类分析', book: '第04章 聚类分析',
    picks: [
      { re: /^CA_\d+.*\.m$/i }, { re: /^CA_CD_\d+.*\.m$/i }, { re: /^Kmean_.*\.m$/i },
      { re: /\.xls$/i, rename: '福冈等城市气候条件.xls' },
      { re: /^ywh_.*\.m$/i },
    ],
    groups: [
      { title: '层次聚类程序（CA_01–CA_15）', re: /^CA_\d+/i },
      { title: 'clusterdata 一体化与 K-均值（CA_CD、Kmean）', re: /^CA_CD|^Kmean/i },
      { title: '鸢尾花案例（ywh 系列：K-均值 / 余弦距离 / 层次聚类）', re: /^ywh_/i },
      { title: '数据文件', re: /\.(xls|csv)$/i, noCode: true },
    ],
  },
  {
    id: 'ch05', zip: 'DR.zip', label: '降维', book: '第05章 降维',
    picks: [
      { re: /^PCA_M\d+\.m$/i }, { re: /^FA_.*\.m$/i }, { re: /^exp_pca.*\.m$/i },
      { re: /^cities\d*\.m$/i }, { re: /^regions\d*\.m$/i },
    ],
    groups: [
      { title: '主成分分析（PCA 三种求法）', re: /^PCA_M/i },
      { title: '因子分析（FA）', re: /^FA_/i },
      { title: '`pca` 函数入门示例（exp_pca）', re: /^exp_pca/i },
      { title: '数据文件（以 .m 矩阵形式提供）', re: /^(cities|regions)/i },
    ],
  },
  {
    id: 'ch06', zip: 'LDA.zip', label: '线性模型（判别分析）', book: '第06章 线性模型',
    picks: [
      { re: /^DA2C_.*\.m$/i }, { re: /^DA_2C_.*\.m$/i }, { re: /^DA_3C_.*\.m$/i }, { re: /^UNDP.*\.m$/i },
    ],
    groups: [
      { title: '二分类判别（线性 / 二次 / 马氏）', re: /^DA2C_/i },
      { title: '二分类进阶（手算全过程 / 与多元回归对照）', re: /^DA_2C_/i },
      { title: '三分类判别与 K-均值结合', re: /^DA_3C_/i },
      { title: 'UNDP 数据综合案例', re: /^UNDP/i },
    ],
  },
  {
    id: 'ch07', zip: 'kNN.zip', label: 'k 最近邻', book: '第07章 k最近邻（kNN）模型',
    picks: [{ re: /^kNN_|^knn_/i }],
    groups: [
      { title: 'kNN 分类', re: /^kNN_exp0/i },
      { title: 'kNN 回归', re: /^kNN_exp1/i },
      { title: '最近邻搜索专题（距离度量 / Kd-树 / 范围搜索）', re: /^knn_sip/i },
    ],
  },
  {
    id: 'ch08', zip: 'DecisionTree_v2.zip', label: '决策树', book: '第08章 决策树',
    picks: [{ re: /^cart_.*\.m$/i }],
    groups: [{ title: 'CART 决策树示例（分类树 / 回归树 / 剪枝与调优）', re: /./ }],
  },
  {
    id: 'ch09', zip: 'ANN.zip', label: '人工神经网络', book: '第09章 人工神经网络',
    picks: [
      { re: /^ANN_\d+.*\.m$/i, zipSub: /ANN\.zip\/ANN\// },
      { re: /^New_ANN_.*\.m$/i }, { re: /^UNDP.*\.m$/i },
    ],
    groups: [
      { title: '经典讲义程序（ANN_01–27：线性网络、感知器、LVQ、BP、竞争网络）', re: /^ANN_\d/i },
      { title: '新版工具箱示例（New_ANN：拟合、分类、聚类、正则化与早停）', re: /^New_ANN/i },
      { title: 'UNDP 数据判别案例', re: /^UNDP/i },
    ],
  },
  {
    id: 'ch10', zip: 'SVM_V1.zip', label: '支持向量机', book: '第10章 支持向量机',
    picks: [{ re: /^SVM_/i }, { re: /^mysigmoid.*\.m$/i }, { re: /\.csv$/i }],
    groups: [
      { title: 'SVM 分类（SVM_C）', re: /^SVM_C/i },
      { title: 'SVM 回归 / SVR（SVM_R）', re: /^SVM_R/i },
      { title: '辅助函数与数据文件', re: /./, noCode: (f) => !f.name.endsWith('.m') },
    ],
  },
];

/* ---------------- 主流程 ---------------- */

console.log('== 读取原始压缩包 ==');
const all = loadAllArchives();

fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(SRC, { recursive: true });
fs.mkdirSync(DL, { recursive: true });

for (const ch of CHAPTERS) {
  const dir = path.join(SRC, ch.id);
  fs.mkdirSync(dir, { recursive: true });

  // 1) 按清单挑文件并归一编码
  const staged = [];
  const taken = new Map(); // 目标名 -> 已挑来源
  for (const pick of ch.picks) {
    for (const e of all) {
      const base = e.vpath.split('/').pop();
      if (!pick.re.test(base)) continue;
      if (pick.zipSub && !pick.zipSub.test(e.vpath)) continue;
      const name = pick.rename ?? base;
      if (taken.has(name)) continue;
      taken.set(name, e.vpath);
      const isM = /\.m$/i.test(name);
      let buf = e.data, enc = null;
      if (isM) {
        const t = decodeText(e.data);
        enc = t.enc;
        buf = Buffer.from(t.text.replace(/\r\n/g, '\n'), 'utf8');
      }
      fs.writeFileSync(path.join(dir, name), buf);
      staged.push({ name, buf, isM, enc, vpath: e.vpath });
    }
  }

  // 2) 元信息与分组
  const files = staged
    .map((s) => ({ ...s, ...extractMeta(decodeText(s.buf).text), ext: s.name.split('.').pop().toLowerCase() }))
    .sort((a, b) => a.name.localeCompare(b.name, 'zh', { numeric: true }));
  for (const f of files) {
    f.group = ch.groups.find((g) => g.re.test(f.name)) ?? { title: '其他', noCode: false };
  }
  const gOrder = new Map(ch.groups.map((g, i) => [g.title, i]));
  files.sort((a, b) => (gOrder.get(a.group.title) - gOrder.get(b.group.title))
    || a.name.localeCompare(b.name, 'zh', { numeric: true }));

  // 3) 打包下载 zip
  const zipName = `${ch.id}_${ch.label}_参考代码.zip`;
  fs.writeFileSync(path.join(DL, zipName), makeZip(files.map((f) => ({ name: `${ch.id}/${f.name}`, data: f.buf }))));

  // 4) 生成章节页
  const rel = (f) => `src/${ch.id}/${f.name}`;
  const fence = (code) => {
    const longest = Math.max(0, ...[...code.matchAll(/`+/g)].map((m) => m[0].length));
    return '`'.repeat(Math.max(3, longest + 1));
  };
  const md = [];
  const nM = files.filter((f) => f.isM).length;
  md.push(`# ${ch.book} · 参考代码`, '');
  md.push(`> 对应书稿《人工智能与地理数据挖掘》**${ch.book}**。共 ${files.length} 个文件（MATLAB 脚本 ${nM} 个、数据文件 ${files.length - nM} 个），来自随书配套代码 ${ch.zip}。`, '');
  md.push(`[⬇ 打包下载 ${zipName}](downloads/${encodeURIComponent(zipName)}){ .md-button }　单文件下载见各节与文件总览。`, '');
  md.push(`!!! tip`, '', `    原始文件编码不一（GBK 与 UTF-8 各半），此处已**统一转为 UTF-8**；运行时把 MATLAB「当前文件夹」切到对应目录，直接运行任一脚本即可。多数脚本依赖 Statistics and Machine Learning Toolbox。`, '');
  md.push(`## 文件总览`, '');
  md.push('| 文件 | 标题 | 行数 |', '|------|------|-----:|');
  for (const f of files) {
    const t = f.title ? f.title.slice(0, 48) : '—';
    md.push(`| [${f.name}](#:file-${ch.id}-${f.name.replace(/\W+/g, '-').toLowerCase()}) | ${t} | ${f.lines} |`);
  }
  md.push('');
  let cur = null;
  for (const f of files) {
    if (f.group.title !== cur) {
      cur = f.group.title;
      md.push(`## ${cur}`, '');
    }
    const id = `:file-${ch.id}-${f.name.replace(/\W+/g, '-').toLowerCase()}`;
    md.push(`### ${f.name} {#${id}}`, '');
    md.push(`**${f.title || '（无标题注释）'}** · ${f.lines} 行`, '');
    // 操作按钮：复制代码（JS 实现）+ 在 MATLAB Online 中打开 + 下载原文件
    const repoFile = `docs/refcode/${rel(f)}`;
    const matlabUrl = `https://matlab.mathworks.com/open/github/v1?repo=${GITHUB_REPO}&file=${repoFile}`;
    const actions = [];
    if (f.isM) {
      actions.push(`<button class="md-button refcopy" type="button">复制代码</button>`);
      actions.push(`<a class="md-button" href="${matlabUrl}" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a>`);
    }
    actions.push(`<a class="md-button" href="${rel(f).split('/').map(encodeURIComponent).join('/')}" download>下载 ${f.name}</a>`);
    md.push(`<p class="refcode-actions">${actions.join(' ')}</p>`, '');
    if (f.desc) md.push(f.desc, '');
    const noCode = f.group.noCode === true || (typeof f.group.noCode === 'function' && f.group.noCode(f));
    if (f.isM && !noCode) {
      const code = decodeText(f.buf).text.replace(/\r\n/g, '\n').trimEnd();
      const bt = fence(code);
      md.push('??? example "展开代码"', '');
      md.push(`    ${bt}matlab`);
      for (const line of code.split('\n')) md.push(`    ${line}`);
      md.push(`    ${bt}`, '');
    }
  }
  fs.writeFileSync(path.join(OUT, `${ch.id}.md`), md.join('\n'), 'utf8');
  console.log(`  ${ch.id} ${ch.label}: ${files.length} 文件 -> ${ch.id}.md + ${zipName}`);
}

// 5) 总览页
const idx = [];
idx.push('# 参考代码总览', '');
idx.push('这里是随书各章**参考代码**的在线浏览页：每个脚本均展示完整源码与注释说明，可单文件下载，也可整章打包下载。', '');
idx.push('| 章节 | 文件数 | 页面 | 打包下载 |', '|------|-------:|------|----------|');
for (const ch of CHAPTERS) {
  const n = fs.readdirSync(path.join(SRC, ch.id)).length;
  const z = `${ch.id}_${ch.label}_参考代码.zip`;
  idx.push(`| ${ch.book} | ${n} | [浏览](./${ch.id}.md) | [${z}](downloads/${encodeURIComponent(z)}) |`);
}
idx.push('', '## 使用说明', '');
idx.push('1. **运行环境**：MATLAB R2014b 及以上；多数脚本依赖 Statistics and Machine Learning Toolbox（`pca`、`fitcknn`、`fitcsvm`、`fitctree`、`fitcdiscr`、`linkage`、`kmeans` 等）。第09章 `ANN_01–27` 使用较旧的神经网络工具箱函数（`newff`、`trainlm`），在较新版本中仍可用。');
idx.push('2. **运行方法**：下载后把 MATLAB「当前文件夹」切换到脚本所在目录，打开脚本直接运行；需要数据的脚本会自动加载同目录的数据文件（或 `fisheriris` 等内置数据集）。');
idx.push('3. **编码说明**：原始参考代码中 GBK 与 UTF-8 编码各占一半，本站所有文本已统一转为 UTF-8；脚本内容未做任何改动。');
idx.push('4. **按钮说明**：「复制代码」一键复制完整脚本；「在 MATLAB Online 中打开」会在 [MATLAB Online](https://matlab.mathworks.com/) 中克隆本站 GitHub 仓库并打开当前脚本（需登录 MathWorks 账号，仓库发布到 GitHub 后生效）；「下载」保存原文件。');
idx.push('5. **与书稿的关系**：脚本的编号与书稿中的例题、图表对应（如 `ANN_18_BP.m` 对应第09章 BP 网络示例）；各章正文中的「配套代码」指的是经重写注释的 `code/ChapterX` 精选脚本，此处为更完整的原始参考代码。');
fs.writeFileSync(path.join(OUT, 'index.md'), idx.join('\n'), 'utf8');
console.log('  index.md 生成完毕');
console.log('== 完成 ==');
