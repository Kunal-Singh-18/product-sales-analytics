MAX_TOP_N=20

ALLOWED_SORT_FIELDS = {
    "amount": "amount",
    "order_date": "order_date",
    "quantity": "quantity",
    "customer_age": "customer_age",
    "rating": "rating",
    "product": "product"
}

RANKING_BASES = (
    "revenue",
    "quantity",
    "orders",
    "average_rating"
)

ALLOWED_GROUP_BY_FIELDS = (
    "product",
    "category",
    "city",
    "payment_mode",
    "customer_type",
    "gender",
    "sales_channel",
    "year",
    "month",
    "rating"
)

METRICS = {

    # Financial Metrics
   
    "total_revenue": {
        "required_parameters": (),
        "invalid_group_by": (),
        "show_in_summary": True
    },

    "average_order_value": {
        "required_parameters": (),
        "invalid_group_by": (),
        "show_in_summary": True
    },

    "highest_sale": {
        "required_parameters": (),
        "invalid_group_by": (),
        "show_in_summary": True
    },

    "lowest_sale": {
        "required_parameters": (),
        "invalid_group_by": (),
        "show_in_summary": True
    },

    # Order Metrics

    "total_orders": {
        "required_parameters": (),
        "invalid_group_by": (),
        "show_in_summary": True
    },

    "total_quantity_sold": {
        "required_parameters": (),
        "invalid_group_by": (),
        "show_in_summary": True
    },

    "average_quantity": {
        "required_parameters": (),
        "invalid_group_by": (),
        "show_in_summary": False
    },

    # Customer Metrics

    "distinct_customers": {
        "required_parameters": (),
        "invalid_group_by": (),
        "show_in_summary": True
    },

    "average_customer_age": {
        "required_parameters": (),
        "invalid_group_by": (),
        "show_in_summary": True
    },

    # Rating Metrics

    "average_rating": {
        "required_parameters": (),
        "invalid_group_by": (),
        "show_in_summary": True
    },

    "highest_rating": {
        "required_parameters": (),
        "invalid_group_by": (),
        "show_in_summary": False
    },

    "lowest_rating": {
        "required_parameters": (),
        "invalid_group_by": (),
        "show_in_summary": False
    },

    # Ranking Metrics

    "top_product": {
        "required_parameters": ("based_on",),
        "invalid_group_by": ("product",),
        "show_in_summary": False
    },

    "top_category": {
        "required_parameters": ("based_on",),
        "invalid_group_by": ("category",),
        "show_in_summary": False
    },

    "top_city": {
        "required_parameters": ("based_on",),
        "invalid_group_by": ("city",),
        "show_in_summary": False
    },

    "top_payment_mode": {
        "required_parameters": ("based_on",),
        "invalid_group_by": ("payment_mode",),
        "show_in_summary": False
    },

    "top_sales_channel": {
        "required_parameters": ("based_on",),
        "invalid_group_by": ("sales_channel",),
        "show_in_summary": False
    },

    "top_customer_type": {
        "required_parameters": ("based_on",),
        "invalid_group_by": ("customer_type",),
        "show_in_summary": False
    }
}

CHART_TYPES = {

    "product": "bar",
    "category": "bar",
    "city": "bar",
    "rating": "bar",

    "month": "line",
    "year": "line",

    "payment_mode": "pie",
    "customer_type": "pie",
    "gender": "pie",
    "sales_channel": "pie"

}