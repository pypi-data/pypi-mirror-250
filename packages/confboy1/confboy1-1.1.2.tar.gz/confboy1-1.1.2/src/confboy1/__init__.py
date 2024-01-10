import typing

import toml


ConfigDict = typing.Dict[str, typing.Any]
CallableDict = typing.Dict[str, typing.Callable]


class InvalidConfigFileError(Exception):
    """Raised on passing invalid TOML config file path."""


class Config(object):

    def __init__(
        self,
        base_config: ConfigDict = {},
        toml_config_path: typing.Optional[str] = None,
        _parent=None,
    ):
        self._config: ConfigDict = {}
        self._callables: CallableDict = {}
        self._parent = _parent

        self.merge_config(base_config)

        if toml_config_path:
            try:
                with open(toml_config_path, 'r') as config_file:
                    patch = toml.loads(config_file.read())
                    self.merge_config(patch)
            except toml.TomlDecodeError as e:
                raise InvalidConfigFileError from e
            except FileNotFoundError:
                pass

    def merge_config(self, patch: ConfigDict) -> None:
        for key, value in patch.items():
            if isinstance(value, dict):
                try:
                    if isinstance(self._config[key], Config):
                        self._config[key].merge_config(value)
                        continue
                    else:
                        value = Config(value, _parent=self)
                except KeyError:
                    value = Config(value, _parent=self)

            self._config[key] = value

    def register_callable(self, callable_: typing.Callable) -> None:
        self._callables[callable_.__name__] = callable_

    def _call(self, key: str) -> typing.Any:
        if self._parent is None:
            return self._callables[key]()

        return self._parent._call(key)

    def __getattr__(self, key: str) -> typing.Any:
        value = self._config[key]

        if isinstance(value, str):
            parts = value.split(':')

            if len(parts) == 2 and parts[0] == 'callable':
                return self._call(parts[1])

        return value

    def __setattr__(self, key: str, value: typing.Any) -> None:
        if key in ['_config', '_callables', '_parent', '_call']:
            return super().__setattr__(key, value)

        if isinstance(value, dict):
            value = Config(value, _parent=self)

        self._config[key] = value

    def __delattr__(self, key: str) -> None:
        del self._config[key]
