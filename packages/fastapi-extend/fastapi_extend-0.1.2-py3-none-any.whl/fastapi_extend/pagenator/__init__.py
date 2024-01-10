# coding:utf-8
"""
Name : __init__.py.py
Author : lvyunze
Time : 2023/1/10 21:17
Desc : 
"""
import typing
from typing import Iterable, Optional

from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select


class PageNumberPagination:
    page_param = "page"  # 默认页码的参数名
    page_size_param = "pageSize"  # 默认页大小的参数名
    default_page = 1  # 默认页码
    default_page_size = 50  # 默认页大小

    sort_field_param = "sort_field"  # 排序字段的参数名
    order_by_param = "order_by"  # 排序方式的字段名

    total_field = "total"  # response的total key
    data_field = "list"  # response的数据 key
    page_field = "current_page"  # response的当前页 key
    size_field = "pageSize"  # response的页大小 key

    def __init__(self, query_model: BaseModel, model, serializer_class, include: set = None, exclude: set = None):
        """

        :param query_model:
        """
        self.model = model
        self.serializer_class = serializer_class
        self.query_model = query_model
        params = self.query_model.dict(include=include, exclude=exclude)
        self.page_number = params.pop(self.page_param, self.default_page)
        self.page_size = params.pop(self.page_size_param, self.default_page_size)
        if self.sort_field_param in params:
            self.sort_field = params.pop("sort_field")
        else:
            self.sort_field = None
        if self.order_by_param in params:
            self.order_by = params.pop("order_by")
        else:
            self.order_by = "asc"
        self.query_params = params

    async def paginate_query(
        self, query: Select, session: AsyncSession
    ) -> Optional[Iterable]:
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        if not self.page_size:
            return None
        # query total length for the condition
        count_statement = select(func.count()).select_from(self.model)
        if query.whereclause is not None:
            count_statement = count_statement.where(query.whereclause)
        count_result = await session.execute(count_statement)
        count = count_result.scalar()

        query_result = await session.execute(
            query.limit(self.page_size).offset((self.page_number - 1) * self.page_size)
        )
        objects = query_result.scalars()

        return {
            self.total_field: count,
            self.page_field: self.page_number,
            self.size_field: self.page_size,
            self.data_field: self.serializer_class.dump(objects, many=True),
        }

    def get_queryset(self):
        """
        通过类实例化参数query_model生成sql语句，如果简单生成不能满足业务需要，可以自己生成sql语句
        如果query_model的字段对应的值为非字符串的可迭代对象，则这个条件使用in_
        :return:
        """
        query = select(self.model)
        for field, condition in self.query_params.items():
            if condition is not None:
                """条件为下列可迭代对象的，使用in条件查询"""
                if isinstance(condition, (list, tuple, set, typing.Iterator)):
                    query = query.where(getattr(getattr(self.model, field), "in_")(condition))
                else:
                    query = query.where(getattr(self.model, field) == condition)
        if self.sort_field:
            query = query.order_by(
                getattr(getattr(self.model, self.sort_field), self.order_by)()
            )
        return query

    async def page(self, session: AsyncSession):
        """
        分页器的最顶层方法，不自定义sql语句，可以直接调用page获取页面数据
        :param session:
        :return: dict 包含页数，页大小，总数和数据的字典
        """
        query = self.get_queryset()

        return await self.paginate_query(query, session)