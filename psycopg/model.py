from typing import List

from sqlalchemy import Column, DateTime, ForeignKeyConstraint, Integer, Numeric, PrimaryKeyConstraint, SmallInteger, String, Text
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class Categories(Base):
    __tablename__ = 'categories'
    __table_args__ = (
        PrimaryKeyConstraint('categoryid', name='categories_pkey'),
        {'schema': 'northwind'}
    )

    categoryid = mapped_column(Integer)
    categoryname = mapped_column(String(50))
    description = mapped_column(String(100))


class Customers(Base):
    __tablename__ = 'customers'
    __table_args__ = (
        PrimaryKeyConstraint('customerid', name='customers_pkey'),
        {'schema': 'northwind'}
    )

    customerid = mapped_column(String(5))
    companyname = mapped_column(String(50))
    contactname = mapped_column(String(30))
    contacttitle = mapped_column(String(30))
    address = mapped_column(String(50))
    city = mapped_column(String(20))
    region = mapped_column(String(15))
    postalcode = mapped_column(String(9))
    country = mapped_column(String(15))
    phone = mapped_column(String(17))
    fax = mapped_column(String(17))

    orders: Mapped[List['Orders']] = relationship('Orders', uselist=True, back_populates='customers')


class Employees(Base):
    __tablename__ = 'employees'
    __table_args__ = (
        PrimaryKeyConstraint('employeeid', name='employees_pkey'),
        {'schema': 'northwind'}
    )

    employeeid = mapped_column(Integer)
    lastname = mapped_column(String(10))
    firstname = mapped_column(String(10))
    title = mapped_column(String(25))
    titleofcourtesy = mapped_column(String(5))
    birthdate = mapped_column(DateTime)
    hiredate = mapped_column(DateTime)
    address = mapped_column(String(50))
    city = mapped_column(String(20))
    region = mapped_column(String(2))
    postalcode = mapped_column(String(9))
    country = mapped_column(String(15))
    homephone = mapped_column(String(14))
    extension = mapped_column(String(4))
    reportsto = mapped_column(Integer)
    notes = mapped_column(Text)

    orders: Mapped[List['Orders']] = relationship('Orders', uselist=True, back_populates='employees')


class Products(Base):
    __tablename__ = 'products'
    __table_args__ = (
        PrimaryKeyConstraint('productid', name='products_pkey'),
        {'schema': 'northwind'}
    )

    productid = mapped_column(Integer)
    supplierid = mapped_column(Integer, nullable=False)
    categoryid = mapped_column(Integer, nullable=False)
    productname = mapped_column(String(35))
    quantityperunit = mapped_column(String(20))
    unitprice = mapped_column(Numeric(13, 4))
    unitsinstock = mapped_column(SmallInteger)
    unitsonorder = mapped_column(SmallInteger)
    reorderlevel = mapped_column(SmallInteger)
    discontinued = mapped_column(String(1))

    order_details: Mapped[List['OrderDetails']] = relationship('OrderDetails', uselist=True, back_populates='products')


class Shippers(Base):
    __tablename__ = 'shippers'
    __table_args__ = (
        PrimaryKeyConstraint('shipperid', name='shippers_pkey'),
        {'schema': 'northwind'}
    )

    shipperid = mapped_column(Integer)
    companyname = mapped_column(String(20))
    phone = mapped_column(String(14))


class Suppliers(Base):
    __tablename__ = 'suppliers'
    __table_args__ = (
        PrimaryKeyConstraint('supplierid', name='supplier_pk'),
        {'schema': 'northwind'}
    )

    supplierid = mapped_column(Integer)
    companyname = mapped_column(String(50))
    contactname = mapped_column(String(30))
    contacttitle = mapped_column(String(30))
    address = mapped_column(String(50))
    city = mapped_column(String(20))
    region = mapped_column(String(15))
    postalcode = mapped_column(String(8))
    country = mapped_column(String(15))
    phone = mapped_column(String(15))
    fax = mapped_column(String(15))
    homepage = mapped_column(String(100))


class Orders(Base):
    __tablename__ = 'orders'
    __table_args__ = (
        ForeignKeyConstraint(['customerid'], ['northwind.customers.customerid'], ondelete='RESTRICT', onupdate='CASCADE', name='orders_customerid_fkey'),
        ForeignKeyConstraint(['employeeid'], ['northwind.employees.employeeid'], ondelete='RESTRICT', onupdate='CASCADE', name='employee_id'),
        PrimaryKeyConstraint('orderid', name='orders_pkey'),
        {'schema': 'northwind'}
    )

    orderid = mapped_column(Integer)
    customerid = mapped_column(String(5), nullable=False)
    employeeid = mapped_column(Integer, nullable=False)
    orderdate = mapped_column(DateTime)
    requireddate = mapped_column(DateTime)
    shippeddate = mapped_column(DateTime)
    freight = mapped_column(Numeric(15, 4))
    shipname = mapped_column(String(35))
    shipaddress = mapped_column(String(50))
    shipcity = mapped_column(String(15))
    shipregion = mapped_column(String(15))
    shippostalcode = mapped_column(String(9))
    shipcountry = mapped_column(String(15))
    shipperid = mapped_column(Integer)

    customers: Mapped['Customers'] = relationship('Customers', back_populates='orders')
    employees: Mapped['Employees'] = relationship('Employees', back_populates='orders')
    order_details: Mapped[List['OrderDetails']] = relationship('OrderDetails', uselist=True, back_populates='orders')


class OrderDetails(Base):
    __tablename__ = 'order_details'
    __table_args__ = (
        ForeignKeyConstraint(['orderid'], ['northwind.orders.orderid'], ondelete='RESTRICT', onupdate='CASCADE', name='order_details_orderid_fkey'),
        ForeignKeyConstraint(['productid'], ['northwind.products.productid'], ondelete='RESTRICT', onupdate='CASCADE', name='order_details_productid_fkey'),
        PrimaryKeyConstraint('orderid', 'productid', name='order_details_pkey'),
        {'schema': 'northwind'}
    )

    orderid = mapped_column(Integer, nullable=False)
    productid = mapped_column(Integer, nullable=False)
    unitprice = mapped_column(Numeric(13, 4))
    quantity = mapped_column(SmallInteger)
    discount = mapped_column(Numeric(10, 4))

    orders: Mapped['Orders'] = relationship('Orders', back_populates='order_details')
    products: Mapped['Products'] = relationship('Products', back_populates='order_details')
