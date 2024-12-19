from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import uvicorn

app = FastAPI()

# Configurer CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['ecommerce']

@app.get("/")
async def root():
    return {"message": "API en cours d'exécution"}

@app.get("/kpi/orders-per-customer")
async def orders_per_customer():
    pipeline = [
        {"$group": {"_id": "$Customer Id", "total_orders": {"$sum": 1}}},
        {"$sort": {"total_orders": -1}}
    ]
    result = list(db.Orders.aggregate(pipeline))
    return {"data": result}


@app.get("/kpi/orders-detailed")
async def orders_detailed():
    pipeline = [
        {
            '$lookup': {
                'from': 'Customers', 
                'localField': 'Customer Id', 
                'foreignField': 'Customer Id', 
                'as': 'customer_details'
            }
        },
        {'$unwind': '$customer_details'},
        {
            '$lookup': {
                'from': 'Products', 
                'localField': 'Product Id', 
                'foreignField': 'Product Id', 
                'as': 'product_details'
            }
        },
        {'$unwind': '$product_details'},
        {
            '$lookup': {
                'from': 'Location', 
                'localField': 'Postal Code', 
                'foreignField': 'Postal Code', 
                'as': 'location_details'
            }
        },
        {'$unwind': '$location_details'},
        {
            '$group': {
                '_id': '$Customer Id', 
                'total_orders': {'$sum': 1}, 
                'customer_name': {'$first': '$customer_details.Customer Name'}, 
                'product_count': {'$sum': 1}, 
                'location': {'$first': '$location_details.City'}
            }
        },
        {'$sort': {'total_orders': -1}}
    ]
    
    result = list(db.Orders.aggregate(pipeline))
    return {"data": result}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
