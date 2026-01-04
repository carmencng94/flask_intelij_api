from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.customers import router as customers_router
from routers.rentals import router as rentals_router

app = FastAPI(title="Sakila API REST")

#  CORS para permitir que Flask (localhost:5000) llame a FastAPI (localhost:8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API Sakila funcionando"}

app.include_router(customers_router, prefix="/api/v1")
app.include_router(rentals_router, prefix="/api/v1")