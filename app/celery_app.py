from celery import Celery

from app.config import config

celery_app = Celery(
    "portfolio",
    broker=config.celery_broker_url,
    backend=config.celery_result_backend,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_track_started=True,
    worker_prefetch_multiplier=1,
)
