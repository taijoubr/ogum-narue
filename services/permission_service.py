from models.user_level import UserLevel


class PermissionService:
    @staticmethod
    def can_manage_users(level: str) -> bool:
        return level in (UserLevel.PROGRAMADOR.value, UserLevel.ADMINISTRADOR.value)

    @staticmethod
    def can_view_finance(level: str) -> bool:
        return level in (UserLevel.PROGRAMADOR.value, UserLevel.ADMINISTRADOR.value, UserLevel.TESOURARIA.value)

    @staticmethod
    def can_access_logs(level: str) -> bool:
        return level == UserLevel.PROGRAMADOR.value

    @staticmethod
    def is_programador(level: str) -> bool:
        return level == UserLevel.PROGRAMADOR.value
