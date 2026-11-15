import psycopg2
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="password135",
    port="5432"
)
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(150) UNIQUE NOT NULL,
        salary NUMERIC(10, 2),
        department VARCHAR(100)
    )
""")
conn.commit()
print("Employees table is ready!")
name = input("Enter employee name: ")
email = input("Enter employee email: ")
salary = float(input("Enter employee salary: "))
department = input("Enter department: ")

cur.execute(
    """
    INSERT INTO employees (name, email, salary, department)
    VALUES (%s, %s, %s, %s)
    """,
    (name, email, salary, department)
)
conn.commit()
print("Employee inserted successfully!")
cur.execute("SELECT * FROM employees")
rows = cur.fetchall()
print("\nEmployee Records:")
for row in rows:
    print(row)
cur.close()
conn.close()
print("Database connection closed!")
