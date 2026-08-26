import os
import uuid

import uuid

from flask import current_app
from sqlalchemy import Integer, String, Boolean, Text, DateTime, func, ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy

from app.config import config


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Project(db.Model):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    stack: Mapped[list] = mapped_column(ARRAY(String), default=list)
    live_url: Mapped[str] = mapped_column(String(500), default="")
    repo_url: Mapped[str] = mapped_column(String(500), default="")
    doc_url: Mapped[str] = mapped_column(String(500), default="")
    published: Mapped[bool] = mapped_column(Boolean, default=False)
    featured: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )


def _coerce(payload):
    p = dict(payload)
    for b in ("published", "featured"):
        if b in p:
            p[b] = str(p[b]).strip().lower() in ("true", "1", "on", "yes")
    if "stack" in p and isinstance(p["stack"], str):
        p["stack"] = [s.strip() for s in p["stack"].split(",") if s.strip()]
    return p


def _serialize(p):
    return {
        "id": str(p.id),
        "title": p.title,
        "slug": p.slug,
        "description": p.description,
        "stack": p.stack or [],
        "live_url": p.live_url,
        "repo_url": p.repo_url,
        "doc_url": p.doc_url,
        "published": p.published,
        "featured": p.featured,
        "created_at": p.created_at.isoformat() if p.created_at else None,
        "updated_at": p.updated_at.isoformat() if p.updated_at else None,
    }


def list_projects(public=True):
    q = Project.query
    if public:
        q = q.filter_by(published=True)
    return [_serialize(p) for p in q.order_by(Project.created_at.desc()).all()]


def get_project(project_id):
    try:
        pid = uuid.UUID(project_id)
    except (ValueError, AttributeError):
        return None
    p = db.session.get(Project, pid)
    return _serialize(p) if p else None


def create_project(payload):
    p = Project(**_coerce(payload))
    db.session.add(p)
    db.session.commit()
    return _serialize(p)


def update_project(project_id, payload):
    try:
        pid = uuid.UUID(project_id)
    except (ValueError, AttributeError):
        return None
    p = db.session.get(Project, pid)
    if not p:
        return None
    for k, v in _coerce(payload).items():
        setattr(p, k, v)
    db.session.commit()
    return _serialize(p)


def delete_project(project_id):
    try:
        pid = uuid.UUID(project_id)
    except (ValueError, AttributeError):
        return None
    p = db.session.get(Project, pid)
    if not p:
        return None
    db.session.delete(p)
    db.session.commit()
    return _serialize(p)


def save_doc(file_storage, slug):
    folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(folder, exist_ok=True)
    ext = os.path.splitext(file_storage.filename)[1]
    filename = f"{slug}-{uuid.uuid4().hex}{ext}"
    path = os.path.join(folder, filename)
    file_storage.save(path)
    return filename


def doc_public_url(filename):
    return f"/docs/{filename}"
