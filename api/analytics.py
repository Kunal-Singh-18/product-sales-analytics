from fastapi import APIRouter,HTTPException,Depends
from datetime import date
from api.query_builder import METRIC_SQL
from api.security import require_role

from api.database import get_connection
from api.query_builder import (
    build_where_clause,
    build_analytics_query
)
from api.validation import (
    validate_metric,
    validate_group_by,
    validate_metric_parameters,
    validate_group_by_compatibility,
    validate_filter_values
)
from api.constants import (
    METRICS,
    ALLOWED_GROUP_BY_FIELDS,
    RANKING_BASES
)

router = APIRouter()


@router.get("/analytics")
def get_analytics(
      
    metric: str,

    group_by: str = None,

    based_on: str = None,
    direction: str = "top",
    n: int = 1,

    customer_id: int = None,
    customer_name: str = None,
    city: str = None,
    product: str = None,
    category: str = None,
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
    current_user : dict = Depends(require_role(["analyst"]))
    ):

    if (
    metric not in METRIC_SQL
    and not metric.startswith("top_")
    ):
        raise HTTPException(
            status_code=501,
            detail="invalid metric."
        )
    
    validate_metric(metric, METRICS)

    validate_group_by(group_by, ALLOWED_GROUP_BY_FIELDS)

    validate_metric_parameters(
            metric,
            based_on,
            direction,
            n,
            METRICS,
            RANKING_BASES
        )

    validate_group_by_compatibility(
            metric,
            group_by,
            METRICS
        )

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
        end_date=end_date)

    query, parameters = build_analytics_query(
        metric,
        group_by,
        where_clause,
        parameters,
        based_on,
        direction,
        n
        )

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
            cursor.execute(query, parameters)
            results = cursor.fetchall()

    finally:
            cursor.close()
            connection.close()
        
    return {
        "metric": metric,
        "group_by": group_by,
        "results": results
        }
        

