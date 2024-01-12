from typing import List


class ProtocolError(Exception):
    pass


class ProtocolConnectionError(ProtocolError):
    pass


class ProtocolExecutionError(ProtocolError):
    pass


class NotEnoughData(ProtocolError):
    pass


class ValidationError(Exception):
    args: List[str]
    _return_code: int = 1
    @property
    def return_code(self):
        return self._return_code

    def __init__(self, property_names: List[str]) -> None:
        self.args = property_names


class NoInputData(ValidationError):
    _return_code: int = 1
    _MISSING_INPUTS = 'Отсутствуют обязательные входные аргументы: {names}.'

    def __str__(self):
        return self._MISSING_INPUTS.format(names=', '.join(self.args))


class NoSecrets(ValidationError):
    _return_code: int = 1
    _MISSING_SECRETS = 'Отсутствуют секреты: {names}.'

    def __str__(self):
        return self._MISSING_SECRETS.format(names=', '.join(self.args))
