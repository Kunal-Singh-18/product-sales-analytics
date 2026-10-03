

def build_where_clause(city=None,
                       product=None,
                       category=None,
                       customer_id=None,
                       payment_mode=None,
                       order_status=None,
                       customer_type=None,
                       gender=None,
                       sales_channel=None,
                       customer_name=None,
                       min_amount=None,
                       max_amount=None,
                       min_quantity=None,
                       max_quantity=None,
                       min_age=None,
                       max_age=None,
                       min_rating=None,
                       max_rating=None,
                       year=None,
                       month=None,
                       start_date=None,
                       end_date=None):
    conditions=[]
    parameters=[]

    if city is not None:
        conditions.append("LOWER(city) = LOWER(%s)")
        parameters.append(city)

    if product is not None:
        conditions.append("LOWER(product) = LOWER(%s)")
        parameters.append(product)

    if category is not None:
        conditions.append("LOWER(category) = LOWER(%s)")
        parameters.append(category)

    if customer_id is not None:
        conditions.append("customer_id = %s")
        parameters.append(customer_id)
    
    if  payment_mode is not None:
        conditions.append("LOWER(payment_mode) = LOWER(%s)")
        parameters.append(payment_mode)
 
    if order_status is not None:
        conditions.append("LOWER(order_status) = LOWER(%s)")
        parameters.append(order_status)

    if customer_type is not None:
        conditions.append("LOWER(customer_type) = LOWER(%s)")
        parameters.append(customer_type)
    
    if gender is not None:
        conditions.append("LOWER(gender) = LOWER(%s)")
        parameters.append(gender)
    
    if sales_channel is not None:
        conditions.append("LOWER(sales_channel) = LOWER(%s)")
        parameters.append(sales_channel)

    if customer_name is not None:
        conditions.append("LOWER(customer_name) LIKE LOWER(%s)")
        parameters.append(f"%{customer_name}%")
    
    if min_amount is not None:
        conditions.append("amount >= %s")
        parameters.append(min_amount)

    if max_amount is not None:
        conditions.append("amount <= %s")
        parameters.append(max_amount)
    
    if min_quantity is not None:
        conditions.append("quantity >= %s")
        parameters.append(min_quantity)

    if max_quantity is not None:
        conditions.append("quantity <= %s")
        parameters.append(max_quantity)

    if min_age is not None:
        conditions.append("customer_age >= %s")
        parameters.append(min_age)

    if max_age is not None:
        conditions.append("customer_age <= %s")
        parameters.append(max_age)

    if min_rating is not None:
        conditions.append("rating >= %s")
        parameters.append(min_rating)

    if max_rating is not None:
        conditions.append("rating <= %s")
        parameters.append(max_rating)
    
    if year is not None:
        conditions.append("YEAR(order_date) = %s")
        parameters.append(year)

    if month is not None:
        conditions.append("MONTH(order_date) = %s")
        parameters.append(month)

    if start_date is not None:
        conditions.append("order_date >= %s")
        parameters.append(start_date)

    if end_date is not None:
        conditions.append("order_date <= %s")
        parameters.append(end_date)

    if conditions:
        where_clause= "WHERE " + " AND ".join(conditions)
    else:
        where_clause= ""
    
    return where_clause,parameters

def build_order_by_clause(sort_by, order, allowed_sort_fields):
    if sort_by in allowed_sort_fields:
        column_name = allowed_sort_fields[sort_by]
        sort_order = order.upper()
        return f"ORDER BY {column_name} {sort_order}"

    return ""

METRIC_SQL = {

    # Financial Metrics

    "total_revenue":
        "COALESCE(SUM(amount), 0) AS total_revenue",

    "average_order_value":
        "COALESCE(AVG(amount), 0) AS average_order_value",

    "highest_sale":
        "COALESCE(MAX(amount), 0) AS highest_sale",

    "lowest_sale":
        "COALESCE(MIN(amount), 0) AS lowest_sale",

    # Order Metrics

    "total_orders":
        "COUNT(*) AS total_orders",

    "total_quantity_sold":
        "COALESCE(SUM(quantity), 0) AS total_quantity_sold",

    "average_quantity":
        "COALESCE(AVG(quantity), 0) AS average_quantity",

    # Customer Metrics

    "distinct_customers":
        "COUNT(DISTINCT customer_id) AS distinct_customers",

    "average_customer_age":
        "COALESCE(AVG(customer_age), 0) AS average_customer_age",

    # Rating Metrics

    "average_rating":
        "COALESCE(AVG(rating), 0) AS average_rating",

    "highest_rating":
        "COALESCE(MAX(rating), 0) AS highest_rating",

    "lowest_rating":
        "COALESCE(MIN(rating), 0) AS lowest_rating"
}

RANKING_SQL = {
    "revenue": "SUM(amount)",
    "quantity": "SUM(quantity)",
    "orders": "COUNT(*)",
    "average_rating": "AVG(rating)"
}

GROUP_BY_SQL = {

    "product": "product",
    "category": "category",
    "city": "city",
    "payment_mode": "payment_mode",
    "customer_type": "customer_type",
    "gender": "gender",
    "sales_channel": "sales_channel",
    "rating": "rating",

    "month": "MONTH(order_date)",
    "year": "YEAR(order_date)"
}

def build_group_by_clause(group_by):

    if group_by is not None:

        group_expression = GROUP_BY_SQL[group_by]

        return f"GROUP BY {group_expression}"

    return ""

def build_select_clause(metric, group_by):

    expression = METRIC_SQL[metric]

    if group_by is not None:

        group_expression = GROUP_BY_SQL[group_by]

        return f"SELECT {group_expression} AS {group_by}, {expression}"

    return f"SELECT {expression}"

def build_ranking_query(
    metric,
    based_on,
    direction,
    n,
    group_by,
    where_clause,
    parameters
):
    ranking_field = metric.replace("top_", "")
    aggregate_expression = RANKING_SQL[based_on]
    order_direction = "DESC" if direction == "top" else "ASC"

    if group_by is None:

        query = f"""
        SELECT
            {ranking_field},
            {aggregate_expression} AS {based_on}
        FROM sales
        {where_clause}
        GROUP BY {ranking_field}
        ORDER BY {based_on} {order_direction}
        LIMIT %s
        """

        return query, parameters + [n]

    group_expression = GROUP_BY_SQL[group_by]

    query = f"""
    WITH grouped AS (

        SELECT
            {group_expression} AS {group_by},
            {ranking_field},
            {aggregate_expression} AS {based_on}

        FROM sales

        {where_clause}

        GROUP BY
            {group_expression},
            {ranking_field}

    ),

    ranked AS (

        SELECT
            *,
            ROW_NUMBER() OVER(

                PARTITION BY {group_by}

                ORDER BY {based_on} {order_direction}

            ) AS rn

        FROM grouped

    )

    SELECT
        {group_by},
        {ranking_field},
        {based_on}

    FROM ranked

    WHERE rn = 1
    ORDER BY {group_by}
    """

    return query, parameters

def build_analytics_query(
    metric,
    group_by,
    where_clause,
    parameters,
    based_on=None,
    direction="top",
    n=1
):
    if metric in METRIC_SQL:
        select_clause = build_select_clause(metric, group_by)

    elif metric.startswith("top_"):

        return build_ranking_query(
            metric,
            based_on,
            direction,
            n,
            group_by,
            where_clause,
            parameters
        )
    
    group_by_clause = build_group_by_clause(group_by)

    query = f"""
    {select_clause}
    FROM sales
    {where_clause}
    {group_by_clause}
    """

    return query, parameters