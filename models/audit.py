from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from utils.db import Base


class Audit(Base):
    __tablename__ = "audit"

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String(150), nullable=False)
    acao = Column(String(150), nullable=False)
    descricao = Column(Text, nullable=True)
    ip = Column(String(45), nullable=True)
    data = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "usuario": self.usuario,
            "acao": self.acao,
            "descricao": self.descricao,
            "ip": self.ip,
            "data": self.data.isoformat() if self.data else None,
        }
