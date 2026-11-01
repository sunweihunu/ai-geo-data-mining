/* MLX 实时脚本板块：复制代码按钮（复制页面内全部代码段，按出现顺序拼接） */
document$.subscribe(() => {
  document.querySelectorAll('p.refcode-actions button.mlxcopy').forEach((btn) => {
    if (btn.dataset.mlxcopyReady) return;
    btn.dataset.mlxcopyReady = '1';
    btn.addEventListener('click', async () => {
      const article = btn.closest('article');
      const codes = article ? [...article.querySelectorAll('.md-typeset pre code')] : [];
      const text = codes.map((c) => c.textContent).join('\n\n');
      if (!text) return;
      try {
        await navigator.clipboard.writeText(text);
      } catch {
        const ta = document.createElement('textarea'); // 非安全上下文兜底
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        ta.remove();
      }
      const old = btn.textContent;
      btn.textContent = '已复制 ✓';
      btn.classList.add('refcopy-done');
      setTimeout(() => { btn.textContent = old; btn.classList.remove('refcopy-done'); }, 1600);
    });
  });
});
