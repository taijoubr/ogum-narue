import os
try:
    from supabase import create_client
except Exception:
    create_client = None

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

def get_supabase_client():
    if create_client is None:
        raise RuntimeError("supabase package not installed")
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("SUPABASE_URL or SUPABASE_KEY not set in environment")
    return create_client(SUPABASE_URL, SUPABASE_KEY)
