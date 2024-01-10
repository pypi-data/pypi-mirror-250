import sys
import json
from typing import Union
import warnings

import pathlib
import ussl.postprocessing as pp

warnings.filterwarnings("ignore")


class BaseFunction:
    """
    Является базовым классом для всех скриптов, участвующих в обогащении и реагировании.

    При использовании класса необходимо реализовать метод ``function``.

    Автоматически принимаемые значения:

        ``input_json``: Первым аргументом принимает информацию, переданную на вход плейбука;

        ``secrets``: Вторым аргументом приниает секреты.
    """
    def __init__(self, ensure_ascii=True) -> None:
        _input_json: Union[dict, list] = json.loads(pathlib.Path(sys.argv[1]).read_text())
        _secrets: dict = json.loads(pathlib.Path(sys.argv[2]).read_text())

        self.ensure_ascii = ensure_ascii

        if isinstance(_input_json, list):
            self.input_json = _input_json
            self.secrets = _secrets['secrets']
            self._print_output()
        elif isinstance(_input_json, dict):
            if 'default_input' in _input_json:
                input_json = _input_json.pop('default_input')
                self.meta_input_json = _input_json
                self.input_json = pp.assign_input(
                    meta_input_json=self.meta_input_json,
                    input_=input_json['input'])
                self.secrets = pp.assign_secrets(
                    meta_input_json=self.meta_input_json,
                    input_=_secrets['secrets'])
                self._print_output(self.meta_input_json)
            else:
                self.input_json = _input_json
                self.secrets = _secrets['secrets']
                self._print_output()

    def function(self) -> None:
        '''
        В этом методе необходимо реализовать функцию по обогащению
        или реагированию.

        Методу доступны переменные ``input_json`` и ``secrets``.
        '''
        raise NotImplementedError('Метод function не реализован')

    def _print_output(
            self,
            meta_input_json: dict = None,
            ) -> None:
        result = self.function().__dict__
        self.input_json.update(result)
        if meta_input_json:
            print(
                json.dumps(
                    pp.format_output(
                        meta_input_json=meta_input_json,
                        input_json=self.input_json
                    ),
                    ensure_ascii=self.ensure_ascii
                )
            )
        else:
            print(
                json.dumps(
                    self.input_json,
                    ensure_ascii=self.ensure_ascii
                )
            )
