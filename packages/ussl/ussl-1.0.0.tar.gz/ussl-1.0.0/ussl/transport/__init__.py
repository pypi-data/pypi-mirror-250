from typing import Union

from ..protocol import (
    INTERFACES,
    base
)
from ..utils import exceptions
from ..model import Protocol, Response


class Transport:
    def __init__(self) -> None:
        pass

    def _connect(self, protocol: Protocol):
        if not protocol.interface:
            raise exceptions.ProtocolExecutionError('Do not specify the interface on which you want to communicate')
        if protocol.interface not in INTERFACES:
            raise exceptions.ProtocolExecutionError('Specified interface not supported')

        self.proto: base.BaseProtocol = INTERFACES[protocol.interface]()
        self.proto.connect(protocol)

    def _execute(self, query: Union[dict, list]) -> str:
        try:
            if isinstance(query, list):
                for q in range(len(query)):
                    response: Response = self.proto.execute(query[q])
                    if response.status is False:
                        return response
            else:
                response: Response = self.proto.execute(query)

            return response
        finally:
            self.proto.close()

    @classmethod
    def connect(self, protocol: Protocol):
        self._connect(self, protocol)

    @classmethod
    def execute(self, query: Union[dict, list]) -> str:
        return self._execute(self, query)

    @classmethod
    def connect_and_execute(self, protocol: Protocol) -> str:
        query = protocol.query
        self._connect(self, protocol)
        return self._execute(self, query)
