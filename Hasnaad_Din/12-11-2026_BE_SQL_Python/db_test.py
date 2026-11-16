import getpass
import psycopg

# Asks for the password when you run it, so it is never saved in your code
password = getpass.getpass("postgres password: ")

with psycopg.connect(
    host="localhost",
    port=5432,
    dbname="itc_practice",
    user="postgres",
    password=password,
) as conn:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT s.name, STRING_AGG(t.name, ', ' ORDER BY t.name)
            FROM student_tutors st
            JOIN students s ON s.id = st.student_id
            JOIN tutors   t ON t.id = st.tutor_id
            GROUP BY s.name
            ORDER BY s.name;
        """)
        for student, tutors in cur.fetchall():
            print(f"{student} is taught by {tutors}")

# Leaving the 'with conn' block saves (commits) the insert automatically