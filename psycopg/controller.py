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
    product = search_products_by_id(order_details[1])
    return [
        product[1],
        order_details[2],
        order_details[3],
    ]


def gerar_relatorio_pedidos():
    os.system("cls" if os.name == "nt" else "clear")
    numero_pedido = int(input("Digite o número do pedido: "))
    os.system("cls" if os.name == "nt" else "clear")
    order = search_order_by_id(numero_pedido)
    if order is None:
        print("Pedido não encontrado")
        input("\nPressione enter para continuar...")
        return
    cliente = search_customer_by_id(order[1])
    vendedor = search_employee_by_id(order[2])
    print(
        f"Número do pedido: {order[0]}\nData do pedido: {order[3].__str__()}\nCliente: {cliente[1]}\nVendedor: {vendedor[2]} {vendedor[1]}\n"
    )
    print("Produtos:")
    order_details = select_order_details_by_order_id(order[0])
    lista_produtos = map(map_products, order_details)
    print(tabulate(lista_produtos, headers=["Produto", "Preço", "Quantidade"]))
    input("\nPressione enter para continuar...")


def gerar_ranking_funcionarios():
    os.system("cls" if os.name == "nt" else "clear")
    while True:
        try:
            data_inicial = input("digite a data inicial no formato aaaa-mm-dd: ").split(
                "-"
            )
            data_inicial = datetime.datetime(
                int(data_inicial[0]), int(data_inicial[1]), int(data_inicial[2])
            )
            break
        except:
            print("Data inicial inválida")
            continue
    while True:
        try:
            data_final = input("digite a data final no formato aaaa-mm-dd: ").split("-")
            data_final = datetime.datetime(
                int(data_final[0]), int(data_final[1]), int(data_final[2])
            )
            break
        except:
            print("Data final inválida")
            continue
    os.system("cls" if os.name == "nt" else "clear")
    count_by_employee = select_count_orders_by_employee(data_inicial, data_final)
    lista = []
    for i in count_by_employee:
        employee = search_employee_by_id(i[0])
        lista.append([f"{employee.firstname} {employee.lastname}", i[1], i[2]])
    lista = sorted(lista, key=lambda x: x[2], reverse=True)
    print(
        tabulate(
            lista,
            headers=[
                "Funcionário",
                "Quantidade de pedidos",
                "Soma dos valores vendidos",
            ],
        )
    )
    input("\nPressione enter para continuar...")
