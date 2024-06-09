import psycopg

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
    finally:
        northwind.close()


import datetime
from model import *



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


def search_customers(name: str) -> Customers:
    # buscar um cliente
    try:
        db = next(get_db())
        return db.query(Customers).filter(Customers.contactname.like(f"{name}%")).all()
    except Exception as e:
        print(e)


def search_products(productname: str) -> Products:
    # buscar um produto
    try:
        db = next(get_db())
        return (
            db.query(Products)
            .filter(Products.productname.like(f"{productname}%"))
            .all()
        )
    except Exception as e:
        print(e)


def search_employee(name: str) -> Employees:
    # inserir um novo funcionário
    try:
        db = next(get_db())
        return list(
            set(
                db.query(Employees).filter(Employees.lastname.like(f"{name}%")).all()
                + db.query(Employees).filter(Employees.firstname.like(f"{name}%")).all()
            )
        )
    except Exception as e:
        print(e)


def search_employee_by_id(id: int) -> Employees:
    # inserir um novo funcionário
    try:
        db = next(get_db())
        return db.query(Employees).filter(Employees.employeeid == id).first()
    except Exception as e:
        print(e)


def search_order_by_id(order_id: int):
    # buscar um pedido pelo id
    try:
        db = next(get_db())
        return db.query(Orders).filter(Orders.orderid == order_id).first()
    except Exception as e:
        print(e)


def select_count_orders_by_employee(
    data_inicial: datetime.datetime, data_final: datetime.datetime
) -> Orders:
    # buscar todos os funcionários
    try:
        db = next(get_db())
        return (
            db.query(
                Orders.employeeid,
                func.count(Orders.employeeid),
                func.sum(OrderDetails.unitprice * OrderDetails.quantity),
            )
            .join(OrderDetails, Orders.orderid == OrderDetails.orderid)
            .filter(Orders.orderdate.between(data_inicial, data_final))
            .group_by(Orders.employeeid)
            .all()
        )
    except Exception as e:
        print(e)
