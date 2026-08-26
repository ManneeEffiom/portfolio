# Portfolio — Frontend (Matrix theme)

Decoupled static frontend for the Matrix-style portfolio. It consumes the
Flask backend API (hosted separately on the `backend` branch / Render).

## Structure
- `index.html` — public site: digital rain, typed intro, projects grid, contact
- `admin.html` — "Zion Control" admin panel (login + project/doc upload)
- `css/matrix.css` — Matrix styling (green phosphor, scanlines, glow)
- `js/rain.js` — canvas digital-rain effect
- `js/main.js` — fetches `/api/projects` from the backend
- `js/admin.js` — admin auth + upload to backend
- `js/config.js` — **set `API_BASE` to your deployed backend URL**

## Configure
Open `js/config.js` and point `API_BASE` at the backend:
```js
window.APP_CONFIG = { API_BASE: "https://your-backend.onrender.com" };
```

## Deploy (Render static site)
1. Connect this repo, branch `frontend`.
2. Static site, build command empty, publish directory `.` (root).
3. Set the backend `FRONTEND_ORIGIN` env var to this site's URL for CORS.

The backend code lives on the `backend` branch.
