from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from datetime import date

app = Flask(__name__)
CORS(app)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return "Vehicle Rental Management System Running!"


# ---------------- DATABASE CONNECTION ----------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",   # change if needed
        database="vehicle_rental"
    )


# ---------------- VEHICLES ----------------
@app.route("/add_vehicle", methods=["POST"])
def add_vehicle():

    data = request.json

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="vehicle_rental"
    )

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO vehicles(vehicle_name, vehicle_type, rent_per_day, availability)
        VALUES (%s, %s, %s, 1)
    """, (
        data["vehicle_name"],
        data["vehicle_type"],
        data["rent_per_day"]
    ))

    conn.commit()   # 🔴 THIS IS CRITICAL
    conn.close()

    return jsonify({"message": "Vehicle Added Successfully"})
# ---------------- CUSTOMERS ----------------
@app.route("/customers")
def get_customers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM customers")
    data = cursor.fetchall()

    conn.close()
    return jsonify(data)


@app.route("/add_customer", methods=["POST"])
def add_customer():
    data = request.json

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO customers(customer_name, phone, email)
        VALUES (%s, %s, %s)
    """, (
        data["customer_name"],
        data["phone"],
        data["email"]
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Customer Added Successfully"})


# ---------------- RENT VEHICLE ----------------
@app.route("/rent_vehicle", methods=["POST"])
def rent_vehicle():
    data = request.json

    conn = get_db_connection()
    cursor = conn.cursor()

    # insert rental
    cursor.execute("""
        INSERT INTO rentals(customer_id, vehicle_id, rent_date)
        VALUES (%s, %s, %s)
    """, (
        data["customer_id"],
        data["vehicle_id"],
        date.today()
    ))

    # update availability
    cursor.execute("""
        UPDATE vehicles
        SET availability = 0
        WHERE vehicle_id = %s
    """, (data["vehicle_id"],))

    conn.commit()
    conn.close()

    return jsonify({"message": "Vehicle Rented Successfully"})


# ---------------- RETURN VEHICLE ----------------
@app.route("/return_vehicle/<int:rental_id>", methods=["PUT"])
def return_vehicle(rental_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    # get vehicle id
    cursor.execute("""
        SELECT vehicle_id FROM rentals WHERE rental_id = %s
    """, (rental_id,))

    result = cursor.fetchone()

    if result:
        vehicle_id = result[0]

        # update rental
        cursor.execute("""
            UPDATE rentals
            SET return_date = %s
            WHERE rental_id = %s
        """, (date.today(), rental_id))

        # update vehicle availability
        cursor.execute("""
            UPDATE vehicles
            SET availability = 1
            WHERE vehicle_id = %s
        """, (vehicle_id,))

        conn.commit()

    conn.close()

    return jsonify({"message": "Vehicle Returned Successfully"})


# ---------------- RENTALS ----------------
@app.route("/rentals")
def get_rentals():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM rentals
    """)

    data = cursor.fetchall()

    conn.close()
    return jsonify(data)


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)