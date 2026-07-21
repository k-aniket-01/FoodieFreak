from typing import Optional
from pydantic import BaseModel
from app.models.common_models import *


class PaginationRequestSchema(BaseModel):
    page : Optional[int] = 1
    per_page : Optional[int] = 10
    
class PaginationResponseSchema(PaginationRequestSchema):
    total_records : Optional[int] = None
    total_pages : Optional[int] = None
    
def apply_pagination(body:PaginationRequestSchema,
                     query
                     ):
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
    if filters:
        query = query.filter(*filters)
    return query

