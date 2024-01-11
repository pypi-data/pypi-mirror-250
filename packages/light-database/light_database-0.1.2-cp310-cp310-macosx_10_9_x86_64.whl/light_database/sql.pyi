# (generated with --quick)

from typing import Any, Callable, Dict, List, Optional, Union
from pandas import DataFrame


class DataFrameModel(SQLModel):
    _executor: Callable
    _sql: str
    _values: List[Any]
    @property
    def df(self) -> DataFrameModel: ...
    def __getitem__(self, key: slice) -> DataFrame: ...
    def __call__(self) -> DataFrame: ...

class DeleteSqlModel(ExecuteWhereSqlModel):
    _executor: Callable
    _sql: str
    _values: List[Any]

class ExecuteWhereSqlModel(RunModel):
    _executor: Callable
    _sql: str
    _values: List[Any]
    def where(self, **kwargs: Any) -> None: ...

class FilterSqlModel(SelectSqlModel, WhereSqlModel):
    _executor: Callable
    _sql: str
    _values: List[Any]

class GroupBySqlModel(DataFrameModel):
    _executor: Callable
    _sql: str
    _values: List[Any]
    def group_by(self, *columns: str) -> DataFrameModel: ...

class InsertSqlModel(SQLModel):
    _executor: Callable
    _sql: str
    _values: List[Any]
    def create(self, **kwargs: Any) -> None: ...
    def _columns_v_position(self, **kwargs) -> Dict[str, str]: ...
    @staticmethod
    def _parentheses(data: List[str]) -> str: ...

class RunModel(SQLModel):
    _executor: Callable
    _sql: str
    _values: List[Any]
    def run(self) -> None: ...

class SQLModel:
    _executor: Callable
    _operator_mapping: Dict[str, str]
    _sql: str
    _values: List[Any]
    def __init__(self, sql: str, executor: Callable, values: Optional[list] = ...) -> None: ...
    def __str__(self) -> str: ...
    @property
    def _kwargs(self) -> Dict[str, Union[str, List[Any], Callable]]: ...
    def _add_condition(self, key: str, value) -> str: ...
    def _col_val_position(self, **kwargs) -> List[str]: ...
    @staticmethod
    def _execute(func) -> Callable: ...

class SelectSqlModel(GroupBySqlModel):
    _executor: Callable
    _sql: str
    _values: List[Any]
    def where(self, **kwargs) -> Union[GroupBySqlModel, WhereSqlModel]: ...

class UpdateSqlModel(SQLModel):
    _executor: Callable
    _sql: str
    _values: List[Any]
    def modify(self, **kwargs) -> ExecuteWhereSqlModel: ...

class WhereSqlModel(GroupBySqlModel):
    _executor: Callable
    _sql: str
    _values: List[Any]
    def select(self, *columns: str) -> Union[GroupBySqlModel, SelectSqlModel]: ...
