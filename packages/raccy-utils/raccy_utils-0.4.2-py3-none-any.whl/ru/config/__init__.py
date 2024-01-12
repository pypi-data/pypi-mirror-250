"""
Copyright 2021 Daniel Afriyie

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import abc
import json
import typing
import threading

from ru.utils import get_data
from ru.constants import constants
from ru.hints import Cast, Path, Config, T
from ru.exceptions.exceptions import ConfigKeyError, ConfigFileNotFoundError


class BaseConfig(abc.ABC):
    """"
    Base config class for all config classes
    """

    def __init__(self, config_path: Path):
        self.CONFIG_PATH = config_path
        self._config: Config = self.load()
        self._mutex: threading.RLock = threading.RLock()

    @property
    def config(self) -> Config:
        return self._config

    @abc.abstractmethod
    def save(self, filename: Path = "config.txt", encoding: typing.Optional[str] = constants.ENCODING) -> None:
        pass

    @abc.abstractmethod
    def load_config(self) -> Config:
        pass

    @staticmethod
    def _cast(item: str, cast: Cast) -> T:
        if cast is bool:
            return eval(item.strip().capitalize())
        if cast is not None:
            return cast(item.strip())
        return item

    def get(self, item: str, default: typing.Optional[typing.Any] = None, cast: typing.Optional[Cast] = None) -> typing.Any:
        with self._mutex:
            try:
                val = self._config[item]
                if cast:
                    return self._cast(val, cast)
                return val
            except KeyError:
                return default

    def get_as_tupple(self, item: str, cast: typing.Optional[Cast] = None) -> typing.Tuple[typing.Any, ...]:
        with self._mutex:
            items: typing.List[str] = self._config[item].split(",")
            if cast is None:
                return tuple(items)
            return tuple(self._cast(val, cast) for val in items)

    def load(self) -> Config:
        try:
            return self.load_config()
        except FileNotFoundError:
            raise ConfigFileNotFoundError(f"{self.__class__.__name__}: Config file '{self.CONFIG_PATH}' not found!")

    def __getitem__(self, item: typing.Union[typing.List[str], str]) -> typing.Union[str, typing.List[str]]:
        with self._mutex:
            try:
                if isinstance(item, list):
                    return [self._config[key] for key in item]
                else:
                    return self._config[item]
            except KeyError:
                raise ConfigKeyError(f"{item}")

    def __setitem__(self, key: str, value: str) -> None:
        with self._mutex:
            self._config[key] = value

    def __repr__(self) -> str:
        return str(self._config)


class JsonConfig(BaseConfig):

    def __init__(self, config_path: Path = "config.json"):
        super().__init__(config_path)

    def load_config(self) -> Config:
        with open(self.CONFIG_PATH, encoding=constants.ENCODING) as f:
            return json.load(f)

    def save(self, filename: Path = "config.txt", encoding: typing.Optional[str] = constants.ENCODING) -> None:
        with open(filename, "w", encoding=encoding) as f:
            json.dump(self._config, f, indent=4)


class TextConfig(BaseConfig):

    def __init__(self, config_path: Path = "config.txt"):
        super().__init__(config_path)

    def load_config(self) -> Config:
        config: typing.Dict[str, str] = {}
        data: typing.List[str] = get_data(self.CONFIG_PATH, split=True, split_char="\n", filter_blanks=True)
        for d in data:
            try:
                split = d.split("=")
                key = split.pop(0)
                val = "=".join(split)
                config[key] = val
            except ValueError:
                pass
        return config

    def save(self, filename: Path = "config.txt", encoding: typing.Optional[str] = constants.ENCODING) -> None:
        with open(filename, "w", encoding=encoding) as f:
            text = "\n".join([f"{key}={self._config[key]}" for key in self._config.keys()])
            f.write(text)

