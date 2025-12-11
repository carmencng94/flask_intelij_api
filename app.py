from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_connection

app = Flask(__name__)
CORS(app)


# GET /api/v1/customers
# 
@app.get("/api/v1/customers")
def get_customers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT customer_id, first_name, last_name, email, active
        FROM customer
        LIMIT 50
    """)
    data = cursor.fetchall()
    conn.close()
    return jsonify(data), 200


# GET /api/v1/customers/<id>
@app.get("/api/v1/customers/<int:customer_id>")
def get_customer(customer_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customer WHERE customer_id = %s", (customer_id,))
    data = cursor.fetchone()
    conn.close()

    if data is None:
        return jsonify({"error": "Cliente no encontrado"}), 404

    return jsonify(data), 200


# 
# POST /api/v1/customers
# 
@app.post("/api/v1/customers")
def create_customer():
    datos = request.json

    # Campos obligatorios
    required = ["first_name", "last_name", "email", "address_id", "store_id"]
    for field in required:
        if field not in datos:
            return jsonify({"error": f"Falta el campo obligatorio '{field}'"}), 400

    first_name = datos["first_name"]
    last_name = datos["last_name"]
    email = datos["email"]
    store_id = datos["store_id"]
    address_id = datos["address_id"]
    active = datos.get("active", 1)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO customer (store_id, first_name, last_name, email, create_date, address_id, active)
        VALUES (%s, %s, %s, %s, NOW(), %s, %s)
    """, (store_id, first_name, last_name, email, address_id, active))

    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "message": "Cliente creado correctamente",
        "customer_id": new_id
    }), 201


#
# PUT /api/v1/customers/<id>
@app.put("/api/v1/customers/<int:customer_id>")
def update_customer(customer_id):
    datos = request.json

    email = datos.get("email")
    active = datos.get("active")

    if email is None or active is None:
        return jsonify({"error": "email y active son campos obligatorios"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE customer SET email = %s, active = %s
        WHERE customer_id = %s
    """, (email, active, customer_id))

    conn.commit()
    conn.close()

    return jsonify({"message": "Cliente actualizado correctamente"}), 200

# DELETE /api/v1/customers/<id>
# (Elimina primero payments y rentals)
@app.delete("/api/v1/customers/<int:customer_id>")
def delete_customer(customer_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Borrar pagos
        cursor.execute("DELETE FROM payment WHERE customer_id = %s", (customer_id,))
        # Borrar alquileres
        cursor.execute("DELETE FROM rental WHERE customer_id = %s", (customer_id,))
        # Borrar cliente
        cursor.execute("DELETE FROM customer WHERE customer_id = %s", (customer_id,))
        conn.commit()

        return jsonify({"message": "Cliente eliminado correctamente"}), 200

    except Exception as ex:
        return jsonify({"error": str(ex)}), 400

    finally:
        conn.close()


# Servidor
if __name__ == "__main__":
    app.run(debug=True, port=5000)
