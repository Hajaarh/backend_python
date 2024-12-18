from pymongo import MongoClient
from fastapi import FastAPI
import uvicorn

app = FastAPI()


client = MongoClient("mongodb://localhost:27017/")
db = client['ecommerce']




@app.get("/kpi/orders-per-customer")
async def orders_per_customer():
    pipeline = [
    {"$group": {"_id": "$Customer ID", "total_orders": {"$sum": 1}}},
    {"$sort": {"total_orders": -1}}
    ]
    result = list(db.Orders.aggregate(pipeline))
    return {"data": result}

"""@app.get("/kpi/orders-per-category")
async def orders_per_category():
    pipeline = [
    {"$group": {"_id": "$Category", "total_orders": {"$sum": 1}}},
    {"$sort": {"total_orders": -1}}
    ]
    result = list(db.Orders.aggregate(pipeline))
    return {"data": result}"""

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)