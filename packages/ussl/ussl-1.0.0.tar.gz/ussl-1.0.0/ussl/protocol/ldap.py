from typing import Optional

import ldap
from ldap.ldapobject import LDAPObject

from Libraries.USSL.ussl.utils.exceptions import ProtocolConnectionError
from ..model import Protocol
from .base import BaseProtocol


class LDAPProtocol(BaseProtocol):
    name = 'ldap'

    def __init__(self):
        self.base: Optional[str] = None
        self.con: Optional[LDAPObject] = None

    def connect(self, protocol: Protocol) -> None:
        server = f'ldap://{protocol.host}'
        ldap_login = f'{protocol.username}@{protocol.domain}'
        self.base = ', '.join(f'dc={i}' for i in protocol.domain.split('.'))
        try:
            self.con = ldap.initialize(server, bytes_mode=False)
            self.con.protocol_version = ldap.VERSION3
            self.con.set_option(ldap.OPT_REFERRALS, 0)
        except ldap.SERVER_DOWN:
            raise ProtocolConnectionError("Нет доступа к серверу.")
        except Exception:
            raise ProtocolConnectionError("Неожиданная ошибка.")

        try:
            self.con.simple_bind_s(ldap_login, protocol.password)
        except ldap.SERVER_DOWN:
            raise ProtocolConnectionError("Неверный пароль.")
        except Exception:
            raise ProtocolConnectionError("Неожиданная ошибка.")

    def close(self) -> None:
        try:
            self.con.unbind()
        except Exception:
            raise ProtocolConnectionError("Неожиданная ошибка.")
        self.con = None
