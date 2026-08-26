import requests

from app.celery_app import celery_app


@celery_app.task(name="tasks.process_doc")
def process_doc(doc_url, project_id):
    # Placeholder async work: fetch uploaded doc and "index" it.
    # Extend with text extraction, thumbnail generation, notifications, etc.
    try:
        resp = requests.head(doc_url, timeout=10)
        indexed = resp.status_code == 200
    except requests.RequestException:
        indexed = False
    return {"project_id": project_id, "indexed": indexed, "doc_url": doc_url}
