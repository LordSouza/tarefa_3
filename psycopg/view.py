import os
from controller import *

while True:
    os.system("cls" if os.name == "nt" else "clear")
    print("Bem vindo ao sistema Northwind!")
    print("1 - Inserir um pedido")
    print("2 - Gerar relatório dos pedidos")
    print("3 - Ranking de funcionários por intervalo de tempo")
    print("0 - Sair")

    opcao = input("Digite a opção desejada: ")
    match opcao:
        case "1":
            inserir_pedido()
        case "2":
            gerar_relatorio_pedidos()
        case "3":
            gerar_ranking_funcionarios()
        case "0":
            break
        case _:
            print("\nOpção inválida!\n")
