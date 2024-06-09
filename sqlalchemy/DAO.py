from model import *
from engine import get_db



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


def search_customers(name: String) -> Customers:
    # buscar um cliente
    try:
        db = next(get_db())
        return db.query(Customers).filter(Customers.contactname.like(f"{name}%")).all()
    except Exception as e:
        print(e)


def search_products(productname: String) -> Products:
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


def search_employee(name: String) -> Employees:
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
