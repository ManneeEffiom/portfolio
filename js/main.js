(function () {
  const API = window.APP_CONFIG.API_BASE;

  // Typewriter intro
  const lines = [
    "> wake up, neo...",
    "> initializing profile...",
    "> backend developer // Python · Flask · Django · FastAPI · MySQL",
    "> follow the white rabbit.",
  ];
  const el = document.getElementById("typed");
  let li = 0, ci = 0;
  function tick() {
    if (!el) return;
    if (li >= lines.length) return;
    const line = lines[li];
    el.textContent = lines.slice(0, li).join("\n") + (li ? "\n" : "") + line.slice(0, ci);
    ci++;
    if (ci > line.length) {
      li++; ci = 0;
      setTimeout(tick, 400);
    } else {
      setTimeout(tick, 35);
    }
  }
  tick();

  // Load projects from the decoupled backend
  fetch(API + "/api/projects")
    .then((r) => r.json())
    .then((data) => renderProjects(data.projects || []))
    .catch(() => {
      const g = document.getElementById("projects-grid");
      if (g) g.innerHTML = '<p class="msg">// connection to matrix failed</p>';
    });

  function renderProjects(projects) {
    const g = document.getElementById("projects-grid");
    if (!g) return;
    if (!projects.length) {
      g.innerHTML = '<p class="msg">// no nodes online</p>';
      return;
    }
    g.innerHTML = projects
      .map((p) => {
        const stack = (p.stack || []).join(" · ");
        const live = p.live_url ? `<a href="${p.live_url}" target="_blank" rel="noopener">[live]</a>` : "";
        const repo = p.repo_url ? `<a href="${p.repo_url}" target="_blank" rel="noopener">[repo]</a>` : "";
        const doc = p.doc_url ? `<a href="${p.doc_url}" target="_blank" rel="noopener">[doc]</a>` : "";
        return `<div class="node">
          <h3>${escapeHtml(p.title)}</h3>
          <div class="stack">${escapeHtml(stack)}</div>
          <p>${escapeHtml(p.description || "")}</p>
          <div>${live} ${repo} ${doc}</div>
        </div>`;
      })
      .join("");
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }
})();
