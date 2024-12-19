from pymongo import MongoClient
from fastapi import FastAPI
import uvicorn

app = FastAPI()

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['ecommerce']
orders_collection = db["Orders"]

# Pipeline de base
base_pipeline = [
    {"$lookup": {"from": "Products", "localField": "Product ID", "foreignField": "Product ID", "as": "Product_details"}},
    {"$lookup": {"from": "Location", "localField": "Postal Code", "foreignField": "Postal Code", "as": "Location_details"}},
    {"$unwind": {"path": "$Product_details", "preserveNullAndEmptyArrays": True}},
    {"$unwind": {"path": "$Location_details", "preserveNullAndEmptyArrays": True}}
]

@app.get("/kpi/total-sales")
async def total_sales():
    pipeline = base_pipeline + [{"$group": {"_id": None, "total_sales": {"$sum": "$Sales"}}}]
    result = list(orders_collection.aggregate(pipeline))
    return {"data": result if result else [{"total_sales": 0}]}

@app.get("/kpi/sales-by-state")
async def sales_by_state():
    pipeline = base_pipeline + [
        {"$group": {"_id": "$Location_details.State", "total_sales": {"$sum": "$Sales"}}},
        {"$sort": {"total_sales": -1}}
    ]
    result = list(orders_collection.aggregate(pipeline))
    return {"data": result}

@app.get("/kpi/sales-by-category")
async def sales_by_category():
    pipeline = base_pipeline + [
        {"$group": {"_id": "$Product_details.Category", "total_sales": {"$sum": "$Sales"}}},
        {"$sort": {"total_sales": -1}}
    ]
    result = list(orders_collection.aggregate(pipeline))
    return {"data": result}

@app.get("/kpi/sales-by-period")
async def sales_by_period():
    pipeline = base_pipeline + [
        {"$addFields": {"month": {"$month": "$Order Date"}, "year": {"$year": "$Order Date"}}},
        {"$group": {"_id": {"year": "$year", "month": "$month"}, "total_sales": {"$sum": "$Sales"}}},
        {"$sort": {"_id.year": 1, "_id.month": 1}}
    ]
    result = list(orders_collection.aggregate(pipeline))
    return {"data": result}

@app.get("/kpi/top-5-quantity-products")
async def top_5_quantity_products():
    pipeline = base_pipeline + [
        {"$group": {"_id": "$Product_details.Product Name", "total_quantity": {"$sum": "$Quantity"}}},
        {"$sort": {"total_quantity": -1}},
        {"$limit": 5}
    ]
    result = list(orders_collection.aggregate(pipeline))
    return {"data": result}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
