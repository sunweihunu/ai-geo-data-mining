# 人工智能与地理数据挖掘 · 课程网站

**作者**：孙伟 · 中山大学地理科学与规划学院

《人工智能与地理数据挖掘》课程在线书稿，使用 [MkDocs](https://www.mkdocs.org/) + [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) 构建，由 GitHub Actions 自动发布到 GitHub Pages。

**在线阅读**：<https://sunweihunu.github.io/ai-geo-data-mining/>

## 版权

© 2026 孙伟 · 中山大学地理科学与规划学院。本作品采用 [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.zh) 许可协议：

- **署名（BY）**：使用时须保留作者署名及原始出处；
- **非商业（NC）**：不得用于任何商业目的；
- **禁止演绎（ND）**：不得修改、转换或基于本作品再创作。

## 仓库结构

```
├── docs/            # 书稿内容（网站源文件）
│   ├── index.md     # 首页
│   ├── ch01.md … ch11.md   # 第 1–11 章
│   ├── figs/        # 章节插图（ch01–ch11）
│   ├── ppt/         # 课程PPT（各章 PDF 原文件 + 内嵌展示页）
│   └── refcode/     # 参考代码浏览页（自动生成，勿手改；src/ 为归一后的源文件）
├── refcode_archives/ # 各章原始参考代码压缩包（build_refcode 的输入）
├── tools/build_refcode.mjs # 参考代码板块一键生成脚本（node tools/build_refcode.mjs）
├── mkdocs.yml       # 网站配置（导航、主题、插件）
└── .github/workflows/ci.yml   # 自动构建发布工作流
```

## 如何更新书稿

1. 修改 `docs/` 下对应的章节 Markdown（如 `docs/ch04.md`），插图放 `docs/figs/chXX/`；
2. 新增章节时：把章节文件放入 `docs/`，并在 `mkdocs.yml` 的 `nav` 中登记；
3. 提交并推送到 `main` 分支即可，GitHub Actions 会自动重新构建并发布网站（约 1–2 分钟）。

```bash
git add docs/
git commit -m "更新第04章"
git push
```

各章插图脚本与示例数据存放在私人仓库 [sunweihunu/ai-geo-data-mining-scripts](https://github.com/sunweihunu/ai-geo-data-mining-scripts)（本机为 `code/` 目录下的嵌套 git 仓库，已加入 .gitignore），不随书稿公开；公开仓库只保留最终插图 `docs/figs/`。

## 本地预览（可选）

```bash
pip install mkdocs-material
mkdocs serve   # 浏览器打开 http://127.0.0.1:8000
```
