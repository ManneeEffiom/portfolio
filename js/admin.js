(function () {
  const API = window.APP_CONFIG.API_BASE;
  const login = document.getElementById("login");
  const panel = document.getElementById("panel");
  const msg = document.getElementById("login-msg");
  const pmsg = document.getElementById("panel-msg");
  let token = localStorage.getItem("zion_token") || "";

  if (token) showPanel();

  function showPanel() {
    login.classList.add("hidden");
    panel.classList.remove("hidden");
    loadProjects();
  }

  document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const res = await fetch(API + "/api/admin/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    const data = await res.json();
    if (res.ok) {
      token = data.token;
      localStorage.setItem("zion_token", token);
      showPanel();
    } else {
      msg.textContent = "// " + (data.error || "access denied");
    }
  });

  document.getElementById("logout").addEventListener("click", () => {
    token = "";
    localStorage.removeItem("zion_token");
    location.reload();
  });

  document.getElementById("project-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const res = await fetch(API + "/api/admin/projects", {
      method: "POST",
      headers: { Authorization: "Bearer " + token },
      body: fd,
    });
    const data = await res.json();
    pmsg.textContent = res.ok ? "// node uploaded: " + (data.title || "") : "// " + (data.error || "failed");
    if (res.ok) { e.target.reset(); loadProjects(); }
  });

  async function loadProjects() {
    const res = await fetch(API + "/api/admin/projects", {
      headers: { Authorization: "Bearer " + token },
    });
    const data = await res.json();
    const list = document.getElementById("admin-list");
    if (!res.ok) { list.innerHTML = "<p>// auth expired</p>"; return; }
    list.innerHTML = (data.projects || [])
      .map((p) => `<div class="node"><h3>${escapeHtml(p.title)}</h3>
        <button data-del="${p.id}">delete</button></div>`)
      .join("");
    list.querySelectorAll("[data-del]").forEach((b) =>
      b.addEventListener("click", deleteProject)
    );
  }

  async function deleteProject(e) {
    const id = e.target.getAttribute("data-del");
    const res = await fetch(API + "/api/admin/projects/" + id, {
      method: "DELETE",
      headers: { Authorization: "Bearer " + token },
    });
    pmsg.textContent = res.ok ? "// node purged" : "// delete failed";
    loadProjects();
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }
})();
