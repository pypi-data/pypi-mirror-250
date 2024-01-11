# (generated with --quick)

import configparser
import pathlib
import portalocker
import threading
from typing import List, Optional, Union

lock: threading._RLock

class EnvConfig:
    _config_path: pathlib.Path
    @classmethod
    def delete(cls, section: str) -> None: ...
    @classmethod
    def init_configer(cls) -> configparser.ConfigParser: ...
    @classmethod
    def read(cls, sections: Optional[Union[str, List[str]]] = ...) -> str: ...
    @classmethod
    def sections(cls) -> str: ...
    @classmethod
    def write(cls, section: str, force: bool = ..., **kwargs) -> None: ...
