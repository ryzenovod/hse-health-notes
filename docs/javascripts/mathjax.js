/* Local MathJax 3.2.2, loaded only when the current article contains formulas. */
(() => {
  const scriptUrl = document.currentScript.src;
  const engineUrl = new URL("vendor/mathjax-3.2.2/tex-svg-full.js", scriptUrl);
  const engineRoot = new URL("./", engineUrl).href.replace(/\/$/, "");
  let enginePromise;
  let queue = Promise.resolve();
  let revision = 0;

  function loadEngine() {
    if (enginePromise) return enginePromise;
    window.MathJax = {
      loader: { paths: { mathjax: engineRoot } },
      startup: { typeset: false },
      tex: {
        inlineMath: [["\\(", "\\)"]],
        displayMath: [["\\[", "\\]"]],
        processEscapes: true,
        processEnvironments: true
      },
      svg: { fontCache: "local" },
      options: {
        ignoreHtmlClass: ".*",
        processHtmlClass: "arithmatex",
        enableMenu: false
      }
    };
    enginePromise = new Promise((resolve, reject) => {
      const script = document.createElement("script");
      script.src = engineUrl.href;
      script.async = true;
      script.onload = () => {
        const startup = window.MathJax && window.MathJax.startup;
        if (!startup || !startup.promise) {
          reject(new Error("MathJax startup unavailable"));
          return;
        }
        startup.promise.then(() => resolve(window.MathJax), reject);
      };
      script.onerror = () => {
        script.remove();
        reject(new Error("MathJax failed to load"));
      };
      document.head.appendChild(script);
    }).catch(error => {
      enginePromise = undefined;
      throw error;
    });
    return enginePromise;
  }

  function renderArticle() {
    const currentRevision = ++revision;
    const article = document.querySelector(".md-content__inner");
    const hasMath = article && article.querySelector(".arithmatex");
    queue = queue.catch(() => {}).then(async () => {
      if (currentRevision !== revision) return;
      if (!hasMath) {
        if (window.MathJax && window.MathJax.typesetClear) {
          window.MathJax.typesetClear();
        }
        return;
      }
      const mathjax = await loadEngine();
      if (currentRevision !== revision || !article.isConnected) return;
      mathjax.typesetClear();
      mathjax.texReset();
      await mathjax.typesetPromise([article]);
    }).catch(() => {
      // Source TeX remains visible if loading or rendering fails.
    });
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(renderArticle);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderArticle, { once: true });
  } else {
    renderArticle();
  }
})();
