import sys
import json
from typing import Union
import warnings

import pathlib
import ussl.postprocessing as pp

from Libraries.USSL.ussl.utils.exceptions import ValidationError

warnings.filterwarnings("ignore")


class BaseFunction:
    """
    Является базовым классом для всех скриптов, участвующих в обогащении и реагировании.

    При использовании класса необходимо реализовать метод ``function``.

    Автоматически принимаемые значения:

        ``input_json``: Первым аргументом принимает информацию, переданную на вход плейбука;

        ``secrets``: Вторым аргументом приниает секреты.
    """

    def __init__(self, ensure_ascii: bool = False) -> None:
        """
        Инициализирует экземпляр класса.

        Args:
            ensure_ascii (bool): Указывает, должны ли символы не из набора ASCII быть экранированы. По умолчанию True.

        Returns:
            None
        """
        self._input_json: Union[dict, list] = json.loads(pathlib.Path(sys.argv[1]).read_text())
        self._secrets: dict = json.loads(pathlib.Path(sys.argv[2]).read_text())

        self.ensure_ascii = ensure_ascii

        try:
            self.input_json = self.validate_input(self._input_json)
            self.secrets = self.validate_secrets(self._secrets)
        except ValidationError as e:
            self.output(e.__str__(), e.return_code)
        except NotImplementedError:
            self.input_json = self._input_json.copy()
            self.secrets = self._secrets.copy()

        self.function()

    def validate_input(self, input_json: dict) -> dict:
        raise NotImplementedError # TODO

    def validate_secrets(self, secrets: dict) -> dict:
        raise NotImplementedError

    def function(self) -> None:
        '''
        В этом методе необходимо реализовать функцию по обогащению
        или реагированию.

        Методу доступны переменные ``input_json`` и ``secrets``.

        Для вывода результата используйте метод ``output``.
        '''
        raise NotImplementedError('Метод function не реализован')


    def output(self,
               message: str,
               return_code: int = 0,
               **kwargs) -> None:
        """
        Выводит результат работы скрипта в формате JSON.

        Args:
            message (str): Сообщение, которое будет выведено.
            input_json (dict): Входной JSON.
            return_code (int): Код возврата, указывающий на успешное выполнение (0) или ошибку (ненулевое значение).
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            None
        """
        # Обновляем входной JSON с результатом или сообщением об ошибке
        self._input_json['error' if return_code else 'result'] = message

        # Обновляем входной JSON с дополнительными аргументами
        self._input_json.update(kwargs)

        # Выводим входной JSON в форматированном виде
        print(json.dumps(self._input_json, ensure_ascii=self.ensure_ascii))

        # Завершаем выполнение скрипта с кодом 0 для успешного выполнения или ненулевым для ошибки
        exit(return_code)

