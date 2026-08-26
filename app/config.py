import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")

    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")  # service role key (server-side only)
    SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")
    SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET", "project-docs")

    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "change-me")
    JWT_TTL_SECONDS = int(os.environ.get("JWT_TTL_SECONDS", 86400))

    # Upstash Redis (used as Celery broker + result backend)
    UPSTASH_REDIS_URL = os.environ.get("UPSTASH_REDIS_URL")

    FRONTEND_ORIGIN = os.environ.get("FRONTEND_ORIGIN", "*")

    @property
    def celery_broker_url(self):
        return self.UPSTASH_REDIS_URL

    @property
    def celery_result_backend(self):
        return self.UPSTASH_REDIS_URL


config = Config()
