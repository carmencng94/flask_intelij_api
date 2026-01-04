from fastapi import APIRouter, HTTPException
from db import get_connection

router = APIRouter(tags=["Rentals"])

@router.post("/rentals", status_code=201)
def create_rental(body: dict):
    required = ["inventory_id", "customer_id", "staff_id"]
    for f in required:
        if f not in body:
            raise HTTPException(status_code=400, detail=f"Falta {f}")

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO rental (rental_date, inventory_id, customer_id, staff_id)
            VALUES (NOW(), %s, %s, %s)
        """, (body["inventory_id"], body["customer_id"], body["staff_id"]))
        conn.commit()
        new_id = cursor.lastrowid
    conn.close()

    return {"message": "Alquiler creado", "rental_id": new_id}

@router.get("/rentals/{rental_id}")
def get_rental(rental_id: int):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM rental WHERE rental_id=%s", (rental_id,))
        data = cursor.fetchone()
    conn.close()

    if not data:
        raise HTTPException(status_code=404, detail="Alquiler no encontrado")

    return data

@router.put("/rentals/{rental_id}/return")
def return_rental(rental_id: int):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE rental SET return_date = NOW() WHERE rental_id=%s
        """, (rental_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Alquiler no encontrado")
    conn.close()

    return {"message": "Alquiler devuelto"}

@router.get("/customers/{customer_id}/rentals")
def rentals_by_customer(customer_id: int):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM rental WHERE customer_id=%s
        """, (customer_id,))
        data = cursor.fetchall()
    conn.close()

    return data

@router.get("/rentals")
def get_rentals(limit: int = 100, offset: int = 0):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM rental LIMIT %s OFFSET %s", (limit, offset))
        data = cursor.fetchall()
    conn.close()

    return data