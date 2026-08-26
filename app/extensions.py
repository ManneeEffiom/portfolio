from supabase import create_client

from app.config import config

supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
