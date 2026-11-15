import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="password135",
    port="5432"
)


cur = conn.cursor() 
#A cursor is an object that acts 
# like a communication tool between 
# your Python program and the database.

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
