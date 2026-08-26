from flask import Blueprint, jsonify, request

from app.auth import encode_token, login_required
from app.models import (
    create_project,
    delete_project,
    get_project,
    list_projects,
    update_project,
    upload_doc,
    get_public_doc_url,
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
    if doc:
        filename = f"{payload.get('slug', 'doc')}-{doc.filename}"
        upload_doc(doc.stream, filename)
        payload["doc_url"] = get_public_doc_url(filename)
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
        if doc:
            filename = f"{payload.get('slug', 'doc')}-{doc.filename}"
            upload_doc(doc.stream, filename)
            payload["doc_url"] = get_public_doc_url(filename)
        row = update_project(project_id, payload)
        return jsonify(row)
    row = delete_project(project_id)
    return jsonify(row)
