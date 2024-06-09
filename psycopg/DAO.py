import psycopg
import datetime
from model import *


def get_db():
    try:
        yield psycopg.connect(
            host="localhost",
            dbname="northwind_2018_1",
            user="postgres",
            password="postgres",
        )
    except Exception as e:
        print(e)
        exit()


def insert_orders(customer: str, employee: int, orderdate: datetime.datetime):
    try:
        db = next(get_db())
        sessao = db.cursor()
        id = sessao.execute(
            "SELECT orderid FROM northwind.orders ORDER BY orderid DESC LIMIT 1"
        ).fetchone()[0]
        sessao.execute(
            "INSERT INTO northwind.orders (orderid, customerid, employeeid, orderdate) VALUES (%s, %s, %s, %s)",
            (id + 1, customer, employee, orderdate),
        )
        db.commit()
        return id + 1
    except Exception as e:
        print(e)
        exit()


def insert_order_details(order: int, product: int, unitprice: float, quantity: int):
    try:
        db = next(get_db())
        sessao = db.cursor()
        sessao.execute(
            "INSERT INTO northwind.order_details (orderid, productid, unitprice, quantity) VALUES (%s, %s, %s, %s)",
            (order, product, unitprice, quantity),
        )
        db.commit()
    except Exception as e:
        print(e)
        exit()


def search_customers(name: str):
    # buscar um cliente
    try:
        db = next(get_db()).cursor()
        return db.execute(
            "SELECT * FROM northwind.customers WHERE contactname LIKE %(name)s",
            {"name": "{}%".format(name)},
        ).fetchall()
    except Exception as e:
        print(e)
        exit()


def search_products(productname: str):
    # buscar um produto
    try:
        db = next(get_db()).cursor()
        return db.execute(
            "SELECT * FROM northwind.products WHERE productname LIKE %(name)s",
            {"name": "{}%".format(productname)},
        ).fetchall()
    except Exception as e:
        print(e)
        exit()


def search_employee(name: str):
    # inserir um novo funcionário
    try:
        db = next(get_db()).cursor()
        return db.execute(
            "SELECT * FROM northwind.employees WHERE lastname LIKE %(firstname)s OR firstname LIKE %(firstname)s",
            {"firstname": "{}%".format(name), "lastname": "{}%".format(name)},
        ).fetchall()
    except Exception as e:
        print(e)
        exit()


def search_employee_by_id(id: int):
    # inserir um novo funcionário
    try:
        db = next(get_db()).cursor()
        return db.execute(
            "SELECT * FROM northwind.employees WHERE employeeid = %s", (id,)
        ).fetchone()
    except Exception as e:
        print(e)
        exit()


def search_order_by_id(order_id: int):
    # buscar um pedido pelo id
    try:
        db = next(get_db()).cursor()
        return db.execute(
            "SELECT * FROM northwind.orders WHERE orderid = %s", (order_id,)
        ).fetchone()
    except Exception as e:
        print(e)
        exit()


def search_products_by_id(product_id: int):
    # buscar um produto pelo id
    try:
        db = next(get_db()).cursor()
        return db.execute(
            "SELECT * FROM northwind.products WHERE productid = %s", (product_id,)
        ).fetchone()
    except Exception as e:
        print(e)
        exit()


def search_customer_by_id(customer_id: str):
    # buscar um cliente pelo id
    try:
        db = next(get_db()).cursor()
        return db.execute(
            "SELECT * FROM northwind.customers WHERE customerid = %s", (customer_id,)
        ).fetchone()
    except Exception as e:
        print(e)
        exit()


def select_order_details_by_order_id(order_id: int):
    # buscar os detalhes de um pedido
    try:
        db = next(get_db()).cursor()
        return db.execute(
            "SELECT * FROM northwind.order_details WHERE orderid = %s", (order_id,)
        ).fetchall()
    except Exception as e:
        print(e)
        exit()


def select_count_orders_by_employee(
    data_inicial: datetime.datetime, data_final: datetime.datetime
):
    # buscar todos os funcionários
    try:
        db = next(get_db()).cursor()
        return db.execute(
            """select o.employeeid, count(o.employeeid), sum(od.unitprice * od.quantity)
                                from northwind.orders o
                                left join northwind.order_details od 
                                on od.orderid = o.orderid 
                                where o.orderdate between %s and %s 
                                group by o.employeeid""",
            (data_inicial, data_final),
        ).fetchall()
    except Exception as e:
        print(e)
        exit()
