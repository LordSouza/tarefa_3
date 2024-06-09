import datetime
class Categories():
    categoryid:int
    categoryname:str
    description:str


class Customers():
    customerid :str
    companyname :str
    contactname :str
    contacttitle :str
    address :str
    city :str
    region :str
    postalcode :str
    country :str
    phone :str
    fax :str

class Employees():
    employeeid:int
    lastname:str
    firstname:str
    title:str
    titleofcourtesy:str
    birthdate:datetime.datetime
    hiredate:datetime.datetime
    address:str
    city:str
    region:str
    postalcode:str
    country:str
    homephone:str
    extension:str
    reportsto:int
    notes:str


class Products():
    productid:int
    supplierid:int
    categoryid:int
    productname:str
    quantityperunit:str
    unitprice:float
    unitsinstock:int
    unitsonorder:int
    reorderlevel:int
    discontinued:str


class Shippers():
    shipperid:int
    companyname:str
    phone:str


class Suppliers():
    supplierid:int
    companyname:str
    contactname:str
    contacttitle:str
    address:str
    city:str
    region:str
    postalcode:str
    country:str
    phone:str
    fax:str
    homepage:str


class Orders():
    orderid:int
    customerid:str
    employeeid:int
    orderdate:datetime.datetime
    requireddate:datetime.datetime
    shippeddate:datetime.datetime
    freight:float
    shipname:str
    shipaddress:str
    shipcity:str
    shipregion:str
    shippostalcode:str
    shipcountry:str
    shipperid:int


class OrderDetails():
    orderid:int
    productid:int
    unitprice:float
    quantity:int
    discount:float
