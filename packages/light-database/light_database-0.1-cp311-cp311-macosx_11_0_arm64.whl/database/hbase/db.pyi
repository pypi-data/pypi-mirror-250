# (generated with --quick)

import database.base
import database.hbase.thrift_hbase
import datetime
import hashlib
import pandas as pd
from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport
from typing import Any, Dict, List, Optional, Type, Union

BaseDB: Type[database.base.BaseDB]
Client: Type[database.hbase.thrift_hbase.THBaseService.Client]
Console: Any
TColumn: Type[database.hbase.thrift_hbase.ttypes.TColumn]
TColumnValue: Type[database.hbase.thrift_hbase.ttypes.TColumnValue]
TDelete: Type[database.hbase.thrift_hbase.ttypes.TDelete]
TGet: Type[database.hbase.thrift_hbase.ttypes.TGet]
TPut: Type[database.hbase.thrift_hbase.ttypes.TPut]
TResult: Type[database.hbase.thrift_hbase.ttypes.TResult]
TScan: Type[database.hbase.thrift_hbase.ttypes.TScan]
Table: Any

class HBaseDB(database.base.BaseDB):
    _section: str
    @staticmethod
    def _column2fq(column: str) -> Dict[str, bytes]: ...
    @classmethod
    def _columns4get(cls, columns: List[str]) -> List[database.hbase.thrift_hbase.ttypes.TColumn]: ...
    @staticmethod
    def _fq2column(family: bytes, qualifier: bytes) -> str: ...
    @classmethod
    def _reset_client(cls) -> None: ...
    @classmethod
    def _result2df(cls, result: database.hbase.thrift_hbase.ttypes.TResult) -> pd.DataFrame: ...
    @classmethod
    def _results2df(cls, results: List[database.hbase.thrift_hbase.ttypes.TResult], columns: Optional[List[str]] = ...) -> pd.DataFrame: ...
    @classmethod
    def client(cls) -> database.hbase.thrift_hbase.THBaseService.Client: ...
    @classmethod
    def create(cls, table: str, row: str, columns: List[str], values: list) -> None: ...
    @classmethod
    def delete(cls, table: str, rows: Union[str, List[str]], columns: List[str]) -> None: ...
    @classmethod
    def select(cls, table: str, rows: Union[str, List[str]], columns: List[str]) -> pd.DataFrame: ...
    @classmethod
    def select_range(cls, table: str, columns: Optional[List[str]] = ..., row_start: Optional[str] = ..., row_stop: Optional[str] = ..., batch_size: int = ..., num_rows: Optional[int] = ...) -> pd.DataFrame: ...
    @classmethod
    def show(cls, table: str, row: str, columns: List[str]) -> None: ...
    @classmethod
    def transport_close(cls) -> None: ...
