
from api.security import require_role
from fastapi import APIRouter,Depends
from api.database import get_connection
from api.query_builder import build_where_clause,build_order_by_clause
from datetime import date
from api.validation import validate_pagination,validate_sorting,validate_filter_values
from api.constants import ALLOWED_SORT_FIELDS
router = APIRouter()

@router.get('/sales')
def get_sales(  customer_id: int = None,
                customer_name: str = None,
                city:str=None,
                product:str=None,
                category:str=None,
                payment_mode: str = None,
                order_status: str = None,
                customer_type: str = None,
                gender: str = None,
                sales_channel: str = None,
                min_amount: float = None,
                max_amount: float = None,
                min_quantity: int = None,
                max_quantity: int = None,
                min_age: int = None,
                max_age: int = None,
                min_rating: int = None,
                max_rating: int = None,
                year: int = None,
                month: int = None,
                start_date: date = None,
                end_date: date = None,
                page: int=1,
                page_size:int=20,
                sort_by:str=None,
                order:str="asc",
                current_user : dict = Depends(require_role(["analyst","viewer"]))
                ):
    
    validate_pagination(page,page_size)
    
    validate_sorting(sort_by,order,ALLOWED_SORT_FIELDS)

    validate_filter_values(
    min_amount,
    max_amount,
    min_quantity,
    max_quantity,
    min_age,
    max_age,
    min_rating,
    max_rating,
    start_date,
    end_date,
    year,
    month
    )

    where_clause, parameters = build_where_clause(
        customer_id=customer_id,
        customer_name=customer_name,
        city=city,
        product=product,
        category=category,
        payment_mode=payment_mode,
        order_status=order_status,
        customer_type=customer_type,
        gender=gender,
        sales_channel=sales_channel,
        min_amount=min_amount,
        max_amount=max_amount,
        min_quantity=min_quantity,
        max_quantity=max_quantity,
        min_age=min_age,
        max_age=max_age,
        min_rating=min_rating,
        max_rating=max_rating,
        year=year,
        month=month,
        start_date=start_date,
        end_date=end_date
    )

    offset = (page - 1) * page_size
    
    order_by_clause = build_order_by_clause(sort_by,order,ALLOWED_SORT_FIELDS)

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        count_query = f"""
        SELECT COUNT(*) AS total_records
        FROM sales
        {where_clause}
        """
        cursor.execute(count_query, parameters)

        count_result = cursor.fetchone()
        total_records = count_result["total_records"]

        total_pages = (total_records + page_size - 1) // page_size

        query = f"""
        SELECT *
        FROM sales
        {where_clause}
        {order_by_clause}
        LIMIT %s OFFSET %s
        """

        query_parameters=parameters + [page_size,offset]
        
        cursor.execute(query, query_parameters)

        results = cursor.fetchall()

    finally:
        cursor.close()
        connection.close()

    return {
    "page": page,
    "page_size": page_size,
    "records_returned": len(results),
    "total_records": total_records,
    "total_pages": total_pages,
    "sales": results
    }