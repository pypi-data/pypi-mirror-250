# (generated with --quick)

import database.base
from typing import Any, Type

MySQLdb: Any
RegularDB: Type[database.base.RegularDB]

class MysqlDB(database.base.RegularDB):
    _creator: Any
    _section: str
