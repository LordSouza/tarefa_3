import psycopg
import datetime
from model import *


def get_db():
    northwind = psycopg.connect(
        host="localhost",
        dbname="northwind_2018_1",
        user="postgres",
        password="postgres",
    )
    try:
        yield northwind.cursor()
    except Exception as e:
        print(e)


def insert_orders(order: Orders):
    try:
        db = next(get_db())
        id = db.query(Orders).order_by(Orders.orderid.desc()).first().orderid + 1
        order.orderid = id
        db.add(order)
        db.commit()
        db.refresh(order)
    except Exception as e:
        print(e)


def insert_order_details(order_details: OrderDetails):
    try:
        db = next(get_db())
        db.add(order_details)
        db.commit()
        db.refresh(order_details)
    except Exception as e:
        print(e)


def search_customers(name: str):
    # buscar um cliente
    try:
        db = next(get_db())
        return db.execute("SELECT * FROM northwind.customers WHERE contactname LIKE %s", (name,)).fetchall()
    except Exception as e:
        print(e)


def search_products(productname: str):
    # buscar um produto
    try:
        db = next(get_db())
        return db.execute("SELECT * FROM northwind.products WHERE productname LIKE %s", (productname,)).fetchall()
    except Exception as e:
        print(e)


def search_employee(name: str):
    # inserir um novo funcionário
    try:
        db = next(get_db())
        return db.execute("SELECT * FROM northwind.employees WHERE lastname LIKE %s OR firstname LIKE %s", (name,name)).fetchall()
    except Exception as e:
        print(e)


def search_employee_by_id(id: int):
    # inserir um novo funcionário
    try:
        db = next(get_db())
        return db.execute("SELECT * FROM northwind.employees WHERE employeeid = %s", (id,)).fetchone()
    except Exception as e:
        print(e)


def search_order_by_id(order_id: int):
    # buscar um pedido pelo id
    try:
        db = next(get_db())
        return db.execute("SELECT * FROM northwind.orders WHERE orderid = %s", (order_id,)).fetchone()
    except Exception as e:
        print(e)

def search_products_by_id(product_id: int):
    # buscar um produto pelo id
    try:
        db = next(get_db())
        return db.execute("SELECT * FROM northwind.products WHERE productid = %s", (product_id,)).fetchone()
    except Exception as e:
        print(e)

def search_customer_by_id(customer_id: str):
    # buscar um cliente pelo id
    try:
        db = next(get_db())
        return db.execute("SELECT * FROM northwind.customers WHERE customerid = %s", (customer_id,)).fetchone()
    except Exception as e:
        print(e)

def select_order_details_by_order_id(order_id: int):
    # buscar os detalhes de um pedido
    try:
        db = next(get_db())
        return db.execute("SELECT * FROM northwind.order_details WHERE orderid = %s", (order_id,)).fetchall()
    except Exception as e:
        print(e)

def select_count_orders_by_employee(
    data_inicial: datetime.datetime, data_final: datetime.datetime
):
    # buscar todos os funcionários
    try:
        db = next(get_db())
        return db.execute("""select o.employeeid, count(o.employeeid), sum(od.unitprice * od.quantity)
                                from northwind.orders o
                                left join northwind.order_details od 
                                on od.orderid = o.orderid 
                                where o.orderdate between %s and %s 
                                group by o.employeeid""", 
                                (data_inicial, data_final)).fetchall()
    except Exception as e:
        print(e)
