from DAO import *
import os
import datetime
from tabulate import tabulate


def inserir_pedido():
    """insere um pedido com seus detalhes no banco de dados recebendo informações do usuario quando necessário"""
    customer = buscar_cliente()
    vendedor = buscar_vendedor()
    pedido = inserir_order(customer, vendedor)
    while True:
        # escolher inserir um produto no pedido ou terminar o pedido
        os.system("cls" if os.name == "nt" else "clear")
        print("1 - Inserir um produto no pedido")
        print("2 - Finalizar o pedido")
        opcao_usuario = input("\nDigite a opção desejada: ")
        match opcao_usuario:
            case "1":
                produto = buscar_produto()
                quantidade = int(input("Digite a quantidade do produto: "))
                unit_price = produto.unitprice
                inserir_order_details(pedido, produto, quantidade, unit_price)
            case "2":
                break
            case _:
                print("\nOpção inválida!\n")
        os.system("cls" if os.name == "nt" else "clear")
    print("\nProduto inserido com sucesso!\n")


def buscar_cliente() -> Customers:
    """busca um cliente no banco de dados

    Returns:
        Customers: cliente selecionado pelo usuario
    """
    custumers = []
    while custumers == []:
        os.system("cls" if os.name == "nt" else "clear")
        name_string = input(
            "Digite o nome do consumidor que você deseja selecionar (pode inserir o nome incompleto): \n"
        )
        custumers = search_customers(name_string)
        if custumers == []:
            name_string = input(
                "Nenhum consumidor possui esse nome, digite novamente: \n"
            )
    for i in range(len(custumers)):
        print(f"{i} - {custumers[i].companyname}")
    customer_ordem = int(input("\nEscolha um consumidor: "))
    customer = custumers[customer_ordem]
    return customer


def buscar_vendedor() -> Employees:
    """busca um vendedor no banco de dados

    Returns:
        Employees: vendedor selecionado pelo usuario
    """
    vendedores = []
    while vendedores == []:
        os.system("cls" if os.name == "nt" else "clear")
        name_string = input(
            "Digite o nome do vendedor que você deseja selecionar (pode inserir o nome incompleto): \n"
        )
        vendedores = search_employee(name_string)
        if vendedores == []:
            name_string = input(
                "Nenhum vendedor possui esse nome, digite novamente: \n"
            )
    for i in range(len(vendedores)):
        print(f"{i} - {vendedores[i].firstname} {vendedores[i].lastname}")
    vendedor_ordem = int(input("\nEscolha um vendedor: "))
    vendedor = vendedores[vendedor_ordem]
    return vendedor


def inserir_order(customer: Customers, vendedor: Employees) -> Orders:
    """insere um Order no banco de dados

    Args:
        customer (Customers): Customers que o usuário selecionou
        vendedor (Employees): Vendedor que foi selecionado

    Returns:
        Orders: A order criada
    """
    data_do_pedido = datetime.datetime.now().__str__()
    ordem = Orders(
        orderdate=data_do_pedido,
        customerid=customer.customerid,
        employeeid=vendedor.employeeid,
    )
    insert_orders(ordem)
    return ordem


def inserir_order_details(
    order: Orders, produto: Products, quantidade: int, unit_price: float
) -> None:
    """insere um OrderDetails no banco de dados

    Args:
        order (Orders): order criado anteriormente
        produto (Products): produto selecionado pelo usuario
        quantidade (int): quantidade de produtos
        unit_price (float): valor do produto
    """
    order_details = OrderDetails(
        orderid=order.orderid,
        productid=produto.productid,
        quantity=quantidade,
        unitprice=unit_price,
    )
    insert_order_details(order_details)


def buscar_produto() -> Products:
    """recebe uma string e retorna uma lista de produtos que possuem essa string no nome

    Returns:
        Products: um unico produto selecionado pelo usuario
    """
    produtos = []
    while produtos == []:
        os.system("cls" if os.name == "nt" else "clear")
        name_string = input(
            "Digite o nome do produto que você deseja selecionar (pode inserir o nome incompleto): \n"
        )
        produtos = search_products(name_string)
        if produtos == []:
            name_string = input("Nenhum produto possui esse nome, digite novamente: \n")
    for i in range(len(produtos)):
        print(f"{i} - {produtos[i].productname}")
    produto_ordem = int(input("\nEscolha um produto: "))
    produto = produtos[produto_ordem]
    return produto


def map_products(order_details):
    return [
        order_details.products.productname,
        order_details.products.unitprice,
        order_details.quantity,
    ]


def gerar_relatorio_pedidos():
    os.system("cls" if os.name == "nt" else "clear")
    numero_pedido = int(input("Digite o número do pedido: "))
    os.system("cls" if os.name == "nt" else "clear")
    order = search_order_by_id(numero_pedido)
    print(
        f"Número do pedido: {order.orderid}\nData do pedido: {order.orderdate}\nCliente: {order.customers.companyname}\nVendedor: {order.employees.firstname} {order.employees.lastname}\n"
    )
    print("Produtos:")
    lista_produtos = map(map_products, order.order_details)
    print(
        tabulate(
            lista_produtos,
            headers=["Produto", "Preço", "Quantidade"],
            tablefmt="orgtbl",
        )
    )
    input("\nPressione enter para continuar...")


def gerar_ranking_funcionarios():
    pass
