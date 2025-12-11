from fastapi import APIRouter, HTTPException
from db import get_connection
from pydantic import BaseModel

router = APIRouter(tags=["Customers"])

# Modelos Pydantic para validar JSON
class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    store_id: int
    address_id: int
    active: int = 1  # valor por defecto

class CustomerUpdate(BaseModel):
    email: str
    active: int

# GET /api/v1/customers
@router.get("/customers")
def get_customers():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT customer_id, first_name, last_name, email, active 
            FROM customer LIMIT 50
        """)
        data = cursor.fetchall()
    conn.close()
    return data

# GET /api/v1/customers/{customer_id}
@router.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM customer WHERE customer_id=%s", (customer_id,))
        data = cursor.fetchone()
    conn.close()

    if not data:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    return data

# POST /api/v1/customers
@router.post("/customers", status_code=201)
def create_customer(cliente: CustomerCreate):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO customer (store_id, first_name, last_name, email, create_date, address_id, active)
            VALUES (%s,%s,%s,%s,NOW(),%s,%s)
        """, (
            cliente.store_id, cliente.first_name, cliente.last_name, 
            cliente.email, cliente.address_id, cliente.active
        ))
        conn.commit()
        new_id = cursor.lastrowid
    conn.close()
    return {"message": "Cliente creado", "customer_id": new_id}

# PUT /api/v1/customers/{customer_id}
@router.put("/customers/{customer_id}")
def update_customer(customer_id: int, body: CustomerUpdate):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE customer SET email=%s, active=%s WHERE customer_id=%s
        """, (body.email, body.active, customer_id))
        conn.commit()
    conn.close()
    return {"message": "Cliente actualizado"}

# DELETE /api/v1/customers/{customer_id}
@router.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    conn = get_connection()
    with conn.cursor() as cursor:
        try:
            cursor.execute("DELETE FROM payment WHERE customer_id=%s", (customer_id,))
            cursor.execute("DELETE FROM rental WHERE customer_id=%s", (customer_id,))
            cursor.execute("DELETE FROM customer WHERE customer_id=%s", (customer_id,))
            conn.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    conn.close()
    return {"message": "Cliente eliminado"}
