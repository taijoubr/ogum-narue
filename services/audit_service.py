import os
from flask import request
from models.audit import Audit
from utils.db import get_db_session, engine
from services.supabase_service import insert_audit_supabase


def record_audit(usuario: str, acao: str, descricao: str = None, ip: str = None):
    """Record audit locally (DB) and attempt to replicate to Supabase if configured."""
    db = get_db_session()
    try:
        entry = Audit(usuario=usuario, acao=acao, descricao=descricao, ip=ip)
        db.add(entry)
        db.commit()
        # attempt to replicate to supabase (best-effort)
        try:
            insert_audit_supabase({
                "usuario": usuario,
                "acao": acao,
                "descricao": descricao,
                "ip": ip,
            })
        except Exception:
            pass
    except Exception:
        db.rollback()
    finally:
        db.close()


def ensure_tables():
    # create audit table if not exists
    from models.audit import Audit as _Audit
    Audit.metadata.create_all(bind=engine)
