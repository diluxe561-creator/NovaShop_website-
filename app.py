from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)


# ================= DATABASE ==================

def connect_db():
    return sqlite3.connect("shop.db")


def create_tables():
    db = connect_db()
    c = db.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY,
        name TEXT,
        price REAL,
        image TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY,
        customer TEXT,
        email TEXT,
        total REAL
    )
    """)

    db.commit()
    db.close()


# ================ SEED DATA ===================

def seed_products():
    db = connect_db()
    c = db.cursor()

    c.execute("SELECT COUNT(*) FROM products")

    if c.fetchone()[0] == 0:
        products = [
            ("Smartphone X", 299, "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9"),
            ("Camera Pro", 450, "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f"),
            ("Headphones", 99, "https://images.unsplash.com/photo-1526178613948-2dce12ec41d9"),
            ("Running Shoes", 120, "https://images.unsplash.com/photo-1542291026-7eec264c27ff")
        ]

        c.executemany("INSERT INTO products VALUES(NULL,?,?,?)", products)

    db.commit()
    db.close()


# ================= API =======================

@app.route("/api/products", methods=["GET"])
def get_products():
    db = connect_db()
    c = db.cursor()

    c.execute("SELECT * FROM products")
    rows = c.fetchall()

    products = []

    for row in rows:
        products.append({
            "id": row[0],
            "name": row[1],
            "price": row[2],
            "image": row[3]
        })

    db.close()

    return jsonify(products)


@app.route("/api/orders", methods=["POST"])
def create_order():
    data = request.json

    customer = data["customer"]
    email = data["email"]
    total = data["total"]

    db = connect_db()
    c = db.cursor()

    c.execute(
        "INSERT INTO orders VALUES(NULL,?,?,?)",
        (customer, email, total)
    )

    db.commit()
    db.close()

    return jsonify({"message": "Order placed successfully!"})


# ================ START ======================

if __name__ == "__main__":
    create_tables()
    seed_products()

    app.run(debug=True)