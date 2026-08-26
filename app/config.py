import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")

    # Supabase Postgres connection (transaction pooler)
    DATABASE_URL = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres.vviehdpjntgrtbiktfxg:M%40nn333ff10m@aws-1-eu-west-1.pooler.supabase.com:6543/postgres?sslmode=require",
    )

    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "change-me")
    JWT_TTL_SECONDS = int(os.environ.get("JWT_TTL_SECONDS", 86400))

    # Upstash Redis (used as Celery broker + result backend)
    UPSTASH_REDIS_URL = os.environ.get("UPSTASH_REDIS_URL")

    # When True, tasks run inline in the web process (no worker needed).
    # Set to False on the Fly.io worker so it consumes the broker instead.
    CELERY_TASK_ALWAYS_EAGER = os.environ.get("CELERY_TASK_ALWAYS_EAGER", "True").lower() in (
        "true",
        "1",
        "on",
        "yes",
    )

    FRONTEND_ORIGIN = os.environ.get("FRONTEND_ORIGIN", "*")

    # Local doc storage (Supabase Storage keys not yet available)
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "uploads")

    @property
    def celery_broker_url(self):
        return self.UPSTASH_REDIS_URL

    @property
    def celery_result_backend(self):
        return self.UPSTASH_REDIS_URL


config = Config()
