from enum import Enum


class UserLevel(Enum):
    PROGRAMADOR = "PROGRAMADOR"
    ADMINISTRADOR = "ADMINISTRADOR"
    SECRETARIA = "SECRETARIA"
    TESOURARIA = "TESOURARIA"

    @classmethod
    def choices(cls):
        return [e.value for e in cls]
