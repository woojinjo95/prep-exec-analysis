from __future__ import annotations
import math

from typing import Generic, Sequence, TypeVar, Optional

from fastapi import Query
from pydantic import BaseModel

from .bases import AbstractParams, BasePage, RawParams

T = TypeVar("T")


class Params(BaseModel, AbstractParams):
    page: int = Query(1, ge=1, description="Page number")
    size: int = Query(15, ge=1, le=100, description="Page size")

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.size,
            offset=self.size * (self.page - 1),
        )


class Page(BasePage[T], Generic[T]):
    page: Optional[int]
    size: Optional[int]
    pages: Optional[int]
    prev: Optional[int]
    next: Optional[int]
    jump_prev: Optional[int]
    jump_next: Optional[int]

    __params_type__ = Params

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        total: int,
        params: AbstractParams,
    ) -> Page[T]:
        if not isinstance(params, Params):
            raise ValueError("Page should be used with Params")

        btn_cnt = 10
        page = params.page
        page_size = params.size
        pages = math.ceil(total / page_size)
        blocks = math.ceil(pages / btn_cnt)
        block = math.ceil(params.page / btn_cnt)
        prev_block = (block - 1)

        return cls(
            total=total,
            items=items,
            page=page,
            size=page_size,
            pages=pages,
            prev=None if page == 1 or page > pages else page - 1,
            next=None if page >= pages else page + 1,
            jump_prev=None if prev_block == 0 else prev_block * btn_cnt,
            jump_next=None if blocks == block or total == 0 else (block * btn_cnt) + 1
        )


__all__ = [
    "Params",
    "Page",
]
