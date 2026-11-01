/* 参考代码板块：复制代码按钮 */
document$.subscribe(() => {
  document.querySelectorAll('p.refcode-actions button.refcopy').forEach((btn) => {
    if (btn.dataset.refcopyReady) return;
    btn.dataset.refcopyReady = '1';
    btn.addEventListener('click', async () => {
      let el = btn.closest('p').nextElementSibling;   // 同一文件小节内、按钮组之后的 details
      while (el && el.tagName !== 'DETAILS') el = el.nextElementSibling;
      const code = el && el.querySelector('pre code');
      if (!code) return;
      const text = code.textContent;
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
