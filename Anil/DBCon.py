import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="password135",
        port=5432
    )
    print("Database connected successfully!")

    cur = conn.cursor()

 

    cur.close()
    conn.close()

except Exception as e:
    print("Database connection failed:", e)