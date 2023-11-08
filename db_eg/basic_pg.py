import psycopg

conn = psycopg.connect("dbname=university user=postgres")
cur = conn.cursor()
cur.execute("select * from instructors")
cur.fetchall()

# conn.commit()
