# coding:utf-8
"""
Name : __init__.py.py
Author : lvyunze
Time : 2023/1/10 21:12
Desc : 
"""
from decimal import Decimal
from typing import Type, Container, Optional, overload

from pydantic import BaseModel, create_model, BaseConfig
from sqlalchemy import inspect
from sqlalchemy.orm import ColumnProperty


def dump(cls, objs, many=False, **kwargs):
    if not objs:
        return [] if many is True else {}
    if many is True:
        return [cls.from_orm(obj).dict(**kwargs) for obj in objs]
    return cls.from_orm(objs).dict(**kwargs)


class Serializer(BaseModel):
    """
    序列化器基类

    >>> class ExampleSerializer(Serializer):
    >>>     id: int
    >>>     name: str
    >>> from collections import namedtuple
    >>> model = namedtuple("Account", ["id", "name"])
    >>> instance = model(id=1, name="demo")
    >>> ExampleSerializer.dump(instance)
    {'id': 1, 'name': 'demo'}
    >>> ExampleSerializer.dump([instance], many=True)
    [{'id': 1, 'name': 'demo'}]
    """

    dump = classmethod(dump)

    class Config:
        orm_mode = True


class OrmConfig(BaseConfig):
    orm_mode = True


def model2schema(
    db_model: Type,
    *,
    config: Type = OrmConfig,
    include: Container[str] = None,
    exclude: Container[str] = None,
) -> Type[BaseModel]:
    """
    用sqlalchemy model生成BaseModel子类，默认注册所有字段，可以用include、exclude控制字段
    :param db_model:
    :param config:
    :param include:
    :param exclude:
    :return:
    """
    exclude = exclude or []
    include = include or []
    mapper = inspect(db_model)
    fields = {}
    for attr in mapper.attrs:
        if isinstance(attr, ColumnProperty):
            if attr.columns:
                name = attr.key
                if (include and name not in include) or (name in exclude):
                    continue
                column = attr.columns[0]
                python_type: Optional[type] = None
                if hasattr(column.type, "impl"):
                    if hasattr(column.type.impl, "python_type"):
                        python_type = column.type.impl.python_type
                elif hasattr(column.type, "python_type"):
                    python_type = column.type.python_type
                assert python_type, f"Could not infer python_type for {column}"
                python_type = python_type if not issubclass(python_type, Decimal) else float
                default = None
                if column.default is None and not column.nullable:
                    default = ...
                fields[name] = (python_type, default)
    model = create_model(db_model.__name__, __config__=config, **fields)  # type: ignore
    model.dump = classmethod(dump)
    return model
