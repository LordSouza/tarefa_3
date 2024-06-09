import psycopg

try:
    northwind = psycopg.connect(
        host="localhost",
        dbname="northwind_2018_1",
        user="postgres",
        password="postgres",
    )

except Exception as e:
    print(e)
