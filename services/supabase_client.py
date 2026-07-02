import os
from dotenv import load_dotenv

try:
    from supabase import create_client
except Exception:
    create_client = None

load_dotenv()

def get_supabase_client():
    if create_client is None:
        raise RuntimeError("supabase package not installed")

    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    if not supabase_url or not supabase_key:
        raise RuntimeError("SUPABASE_URL or SUPABASE_KEY not set in environment")

    return create_client(supabase_url, supabase_key)
