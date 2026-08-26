from datetime import datetime, timezone

from flask import current_app

from app.extensions import supabase


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def list_projects(public=True):
    query = supabase.table("projects").select("*")
    if public:
        query = query.eq("published", True)
    res = query.order("created_at", desc=True).execute()
    return res.data or []


def get_project(project_id):
    res = supabase.table("projects").select("*").eq("id", project_id).execute()
    rows = res.data or []
    return rows[0] if rows else None


def create_project(payload):
    payload = {**payload, "created_at": _now_iso(), "updated_at": _now_iso()}
    res = supabase.table("projects").insert(payload).execute()
    return (res.data or [None])[0]


def update_project(project_id, payload):
    payload = {**payload, "updated_at": _now_iso()}
    res = supabase.table("projects").update(payload).eq("id", project_id).execute()
    return (res.data or [None])[0]


def delete_project(project_id):
    res = supabase.table("projects").delete().eq("id", project_id).execute()
    return (res.data or [None])[0]


def upload_doc(file_obj, filename):
    bucket = current_app.config["SUPABASE_BUCKET"]
    res = supabase.storage.from_(bucket).upload(
        filename, file_obj, {"content-type": "application/octet-stream", "upsert": "true"}
    )
    return res


def get_public_doc_url(filename):
    bucket = current_app.config["SUPABASE_BUCKET"]
    return supabase.storage.from_(bucket).get_public_url(filename)
