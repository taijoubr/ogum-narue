from typing import Optional
from services.supabase_client import get_supabase_client


def insert_audit_supabase(entry: dict) -> Optional[dict]:
    """Insert an audit entry into Supabase `audit` table. Returns response or None on error."""
    try:
        client = get_supabase_client()
        res = client.table("audit").insert(entry).execute()
        return res
    except Exception:
        return None


def upload_file_to_bucket(bucket: str, path: str, file_obj, content_type: Optional[str] = None):
    """Upload a file-like object to Supabase Storage bucket."""
    client = get_supabase_client()
    storage = client.storage()
    if content_type:
        res = storage.from_(bucket).upload(path, file_obj, {'content-type': content_type})
    else:
        res = storage.from_(bucket).upload(path, file_obj)
    return res
