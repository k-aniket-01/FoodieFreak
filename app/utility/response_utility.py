from typing import Optional
from pydantic import BaseModel
from app.models.common_models import *


class PaginationRequestSchema(BaseModel):
    page : Optional[int] = 1
    per_page : Optional[int] = 10
    
# class PaginationResponseSchema(PaginationRequestSchema):
#     total = Optional[int] = 0

    
def apply_pagination(body:PaginationRequestSchema,
                     query):
    ost = (body.page - 1) * body.per_page 
    lmt = body.per_page
    return query.offset(ost).limit(lmt)


def apply_filters(body, model, query):
    filters = []
    for k,v in body.model_dump().items():
        if v is not None and hasattr(model, k):
            field = getattr(model, k)
            filters.append(field == v)
    if filters:
        query = query.filter(*filters)
    return query
