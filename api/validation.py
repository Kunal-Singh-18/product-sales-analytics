from fastapi import HTTPException
from api.constants import MAX_TOP_N
def validate_pagination(page,page_size):
    if page<1:
        raise HTTPException(
            status_code=400,
            detail="Page number must atleast be 1"
        )
    if page_size<1:
        raise HTTPException(
            status_code=400,
            detail="Page size must atleast be 1"
        )
    
    if page_size>100:
        raise HTTPException(
            status_code=400,
            detail="Page size cannot exceed 100"
        )
    
def validate_sorting(sort_by,order,allowed_sort_fields):
    if sort_by is not None and sort_by not in allowed_sort_fields :
        raise HTTPException(
            status_code=400,
            detail=" invalid field for sorting "
        )
    
    if order and order.lower() not in ["asc","desc"]:
        raise HTTPException(
            status_code=400,
            detail="order must be either asc(ascending) or desc(descending)"
        )

from fastapi import HTTPException


def validate_filter_values(
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
    month,
):

    if min_amount is not None and min_amount < 0:
        raise HTTPException(
            status_code=400,
            detail="Minimum amount cannot be negative."
        )

    if max_amount is not None and max_amount < 0:
        raise HTTPException(
            status_code=400,
            detail="Maximum amount cannot be negative."
        )

    if min_quantity is not None and min_quantity < 0:
        raise HTTPException(
            status_code=400,
            detail="Minimum quantity cannot be negative."
        )

    if max_quantity is not None and max_quantity < 0:
        raise HTTPException(
            status_code=400,
            detail="Maximum quantity cannot be negative."
        )

    if min_age is not None and min_age < 0:
        raise HTTPException(
            status_code=400,
            detail="Minimum age cannot be negative."
        )

    if max_age is not None and max_age < 0:
        raise HTTPException(
            status_code=400,
            detail="Maximum age cannot be negative."
        )

    if min_rating is not None and not (1 <= min_rating <= 5):
        raise HTTPException(
            status_code=400,
            detail="Minimum rating must be between 1 and 5."
        )

    if max_rating is not None and not (1 <= max_rating <= 5):
        raise HTTPException(
            status_code=400,
            detail="Maximum rating must be between 1 and 5."
        )

    if month is not None and not (1 <= month <= 12):
        raise HTTPException(
            status_code=400,
            detail="Month must be between 1 and 12."
        )

    if year is not None and year < 1:
        raise HTTPException(
            status_code=400,
            detail="Year must be positive."
        )

    if (
        min_amount is not None
        and max_amount is not None
        and min_amount > max_amount
    ):
        raise HTTPException(
            status_code=400,
            detail="Minimum amount cannot be greater than maximum amount."
        )

    if (
        min_quantity is not None
        and max_quantity is not None
        and min_quantity > max_quantity
    ):
        raise HTTPException(
            status_code=400,
            detail="Minimum quantity cannot be greater than maximum quantity."
        )

    if (
        min_age is not None
        and max_age is not None
        and min_age > max_age
    ):
        raise HTTPException(
            status_code=400,
            detail="Minimum age cannot be greater than maximum age."
        )

    if (
        min_rating is not None
        and max_rating is not None
        and min_rating > max_rating
    ):
        raise HTTPException(
            status_code=400,
            detail="Minimum rating cannot be greater than maximum rating."
        )

    if (
        start_date is not None
        and end_date is not None
        and start_date > end_date
    ):
        raise HTTPException(
            status_code=400,
            detail="Start date cannot be after end date."
        )
    
def validate_metric(metric,allowed_metrics):
    if metric not in allowed_metrics:
        raise HTTPException(
            status_code=400,
            detail="Invalid metric specified."
        )

def validate_group_by(group_by, allowed_group_by_fields):
    if (
        group_by is not None
        and group_by not in allowed_group_by_fields
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid group by field."
        )
    
def validate_metric_parameters(
    metric,
    based_on,
    direction,
    n,
    metrics,
    ranking_bases
):
    provided_parameters = {
    "based_on": based_on,
    "direction": direction,
    "n": n
    }

    required_parameters = metrics[metric]["required_parameters"]

    for parameter in required_parameters:
        if provided_parameters[parameter] is None:
            raise HTTPException(
                status_code=400,
                detail=f"{parameter} is required for metric '{metric}'."
            )

    if based_on is not None and based_on not in ranking_bases:
        raise HTTPException(
            status_code=400,
            detail="Invalid ranking basis."
        )

    if direction.lower() not in ("top", "bottom"):
        raise HTTPException(
            status_code=400,
            detail="Direction must be either 'top' or 'bottom'."
        )

    if n is not None and (n < 1 or n > MAX_TOP_N):
        raise HTTPException(
            status_code=400,
            detail=f"n must be between 1 and {MAX_TOP_N}."
        )
    
def validate_group_by_compatibility(metric, group_by, metrics):

    if group_by is None:
        return

    invalid_group_by = metrics[metric]["invalid_group_by"]

    if group_by in invalid_group_by:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Metric '{metric}' cannot be grouped by '{group_by}'."
            )
        )