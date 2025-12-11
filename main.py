from fastapi import FastAPI
from routers.customers import router as customers_router
from routers.rentals import router as rentals_router

app = FastAPI(title="Sakila API REST")

@app.get("/")
def root():
    return {"message": "API Sakila funcionando"}

app.include_router(customers_router, prefix="/api/v1")
app.include_router(rentals_router, prefix="/api/v1")
