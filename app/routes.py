import functools

import jwt
from flask import Blueprint, jsonify, request, send_from_directory, current_app

from app.auth import encode_token, login_required
from app.models import (
    create_project,
    delete_project,
    doc_public_url,
    get_project,
    list_projects,
    save_doc,
    update_project,
)

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "online", "matrix": "follow the white rabbit"})


@api.route("/projects", methods=["GET"])
def projects():
    rows = list_projects(public=True)
    return jsonify({"projects": rows, "count": len(rows)})


@api.route("/projects/<project_id>", methods=["GET"])
def project_detail(project_id):
    row = get_project(project_id)
    if not row:
        return jsonify({"error": "node not found"}), 404
    return jsonify(row)


@api.route("/docs/<path:filename>", methods=["GET"])
def serve_doc(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)


# ---------- Admin: Zion Control ----------
@api.route("/admin/login", methods=["POST"])
def admin_login():
    data = request.get_json(silent=True) or {}
    if (
        data.get("username") != __import__("app.config").config.ADMIN_USERNAME
        or data.get("password") != __import__("app.config").config.ADMIN_PASSWORD
    ):
        return jsonify({"error": "access denied"}), 401
    return jsonify({"token": encode_token()})


@api.route("/admin/projects", methods=["GET"])
@login_required
def admin_list():
    rows = list_projects(public=False)
    return jsonify({"projects": rows})


@api.route("/admin/projects", methods=["POST"])
@login_required
def admin_create():
    payload = request.form.to_dict()
    doc = request.files.get("doc")
    if doc and doc.filename:
        filename = save_doc(doc, payload.get("slug", "doc"))
        payload["doc_url"] = doc_public_url(filename)
    row = create_project(payload)
    if row and row.get("doc_url"):
        from app.tasks import process_doc

        process_doc.delay(row["doc_url"], row["id"])
    return jsonify(row), 201


@api.route("/admin/projects/<project_id>", methods=["PUT", "DELETE"])
@login_required
def admin_modify(project_id):
    if request.method == "PUT":
        payload = request.form.to_dict()
        doc = request.files.get("doc")
        if doc and doc.filename:
            filename = save_doc(doc, payload.get("slug", "doc"))
            payload["doc_url"] = doc_public_url(filename)
        row = update_project(project_id, payload)
        return jsonify(row)
    row = delete_project(project_id)
    return jsonify(row)
