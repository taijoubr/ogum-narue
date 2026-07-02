import os
from typing import Dict, List, Optional

from models.user_level import UserLevel
from services.supabase_client import get_supabase_client


def _parse_email_list(value: str) -> List[str]:
    return [email.strip().lower() for email in value.split(",") if email.strip()]


def is_supabase_auth_enabled() -> bool:
    return bool(os.environ.get("SUPABASE_URL") and os.environ.get("SUPABASE_KEY"))


def _load_role_email_lists() -> Dict[str, List[str]]:
    return {
        UserLevel.PROGRAMADOR.value: _parse_email_list(
            os.environ.get("SUPABASE_PROGRAMADOR_EMAILS", "")
        ),
        UserLevel.ADMINISTRADOR.value: _parse_email_list(
            os.environ.get("SUPABASE_ADMIN_EMAILS", "")
        ),
        UserLevel.SECRETARIA.value: _parse_email_list(
            os.environ.get("SUPABASE_SECRETARIA_EMAILS", "")
        ),
        UserLevel.TESOURARIA.value: _parse_email_list(
            os.environ.get("SUPABASE_TESOURARIA_EMAILS", "")
        ),
    }


def determine_user_level(email: str) -> Optional[str]:
    email_value = email.strip().lower()
    role_email_lists = _load_role_email_lists()
    configured_roles = any(role_email_lists.values())

    for level, emails in role_email_lists.items():
        if email_value in emails:
            return level

    if configured_roles:
        return None

    return UserLevel.ADMINISTRADOR.value


def supabase_sign_in(email: str, password: str) -> dict:
    client = get_supabase_client()
    response = client.auth.sign_in_with_password({"email": email, "password": password})
    error = getattr(response, "error", None)
    if error:
        message = getattr(error, "message", None) or str(error)
        raise RuntimeError(message)

    data = getattr(response, "data", None)
    if data is None:
        raise RuntimeError("Falha ao autenticar no Supabase")

    if hasattr(data, "dict"):
        data = data.dict()

    return data
