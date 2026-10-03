from fastapi import FastAPI
from api.sales import router as sales_router
from api.analytics import router as analytics_router
from api.auth import router as auth_router

app = FastAPI(title="Product Sales Analytics API",description="API for searching sales records and generating business analytics",version="1.0")

@app.get('/')
def home():
    return {
        "message":"Welcome to the Product Sales Analytics API"
    }

app.include_router(sales_router)
app.include_router(analytics_router)
app.include_router(auth_router)