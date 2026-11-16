from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "password135",
    "host": "localhost",
    "port": "5432",
}


def init_db():
  try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL
            )
        """)
    conn.commit()
    cursor.close()
    conn.close()
  except Exception as e:
    print(f"Database error: {e}")


init_db()

# Login / Signup Page
@app.route("/")
def index():
  return render_template("index.html")


# === NEW: Home Page Route ===
@app.route("/home")
def home():
  return render_template("home.html")


# Signup Route
@app.route("/api/signup", methods=["POST"])
def signup():
  data = request.json
  name = data.get("name")
  email = data.get("email")
  password = data.get("password")

  try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
        (name, email, password),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"success": True, "message": "Signup successful! Please login."})
  except psycopg2.errors.UniqueViolation:
    return jsonify(
        {"success": False, "message": "Email already registered"}
    ), 400
  except Exception as e:
    return jsonify({"success": False, "message": str(e)}), 500


# Login Route
@app.route("/api/login", methods=["POST"])
def login():
  data = request.json
  email = data.get("email")
  password = data.get("password")

  try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM users WHERE email = %s AND password = %s",
        (email, password),
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
      return jsonify({
          "success": True,
          "message": f"Welcome {user[0]}! Login successful.",
          "name": user[0],  # <-- Send the user's name back to JavaScript
      })
    else:
      return jsonify(
          {"success": False, "message": "Invalid email or password"}
      ), 401
  except Exception as e:
    return jsonify({"success": False, "message": str(e)}), 500


if __name__ == "__main__":
  app.run(debug=True, port=5000)