import os
import requests

from app.celery_app import celery_app


@celery_app.task(name="tasks.process_doc")
def process_doc(doc_url, project_id):
    # Placeholder async work for uploaded docs. Since docs are served locally
    # (path like /docs/<file>), we mark them indexed; swap in extraction /
    # thumbnail / notification logic as needed.
    if doc_url and doc_url.startswith("/"):
        indexed = True
    else:
        try:
            resp = requests.head(doc_url, timeout=10)
            indexed = resp.status_code == 200
        except requests.RequestException:
            indexed = False
    return {"project_id": project_id, "indexed": indexed, "doc_url": doc_url}
