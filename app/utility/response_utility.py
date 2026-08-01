from typing import Optional
from pydantic import BaseModel
from fastapi import HTTPException, status
from app.utility.enums import SortEnum
from datetime import time
from app.models.common_models import *


class PaginationRequestSchema(BaseModel):
    page : Optional[int] = 1
    per_page : Optional[int] = 10
    
class PaginationResponseSchema(PaginationRequestSchema):
    total_records : Optional[int] = None
    total_pages : Optional[int] = None
    
    
def apply_pagination(body:PaginationRequestSchema, query):
    ost = (body.page - 1) * body.per_page 
    lmt = body.per_page
    total_records = query.count()
    total_pages = (total_records + body.per_page - 1) // body.per_page if total_records > 0 else 0
    query = query.offset(ost).limit(lmt)
    pagination = {
        "page":body.page,
        "per_page":body.per_page,
        "total_records":total_records,
        "total_pages":total_pages
                  }
    return query, pagination


def apply_filters(body, model, query):
    filters = []
    for k,v in body.model_dump().items():
        if v is not None and hasattr(model, k):
            field = getattr(model, k)
            filters.append(field == v)
            
    if body.start_date:
        filters.append(model.created_at >= datetime.combine(body.start_date, time.min))
    if body.end_date:
        filters.append(model.created_at <= datetime.combine(body.end_date, time.max))
    if filters:
        query = query.filter(*filters)
    return query


def apply_sorting(body, model, query):
    sort_column = getattr(model, body.sort_by, None)
    if sort_column is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid sort_by")
    
    query = query.order_by(
        sort_column.asc() 
        if body.sort_order == SortEnum.ASC 
        else sort_column.desc()
        )
    return query