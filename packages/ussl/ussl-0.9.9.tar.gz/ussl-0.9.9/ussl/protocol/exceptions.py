class ProtocolError(Exception):
    pass


class ProtocolConnectionError(ProtocolError):
    pass


class ProtocolExecutionError(ProtocolError):
    pass


class NotEnoughData(ProtocolError):
    pass
