import os
from flask import request
from models.audit import Audit
from utils.db import get_db_session, engine


def record_audit(usuario: str, acao: str, descricao: str = None, ip: str = None):
    db = get_db_session()
    try:
        entry = Audit(usuario=usuario, acao=acao, descricao=descricao, ip=ip)
        db.add(entry)
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()

def ensure_tables():
    # create audit table if not exists
    from models.audit import Audit as _Audit
    Audit.metadata.create_all(bind=engine)
