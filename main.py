import Telas
import psycopg2

conn = psycopg2.connect(
    dbname="TrabalhoBD",
    user="postgres",
    password="senha"
)

cur = conn.cursor()


while True:  
        print("\n=== Bem-vindo ao Sistema ===")
        print("1. Cliente")
        print("2. Gerente")
        print("3. Atendente")
        print("4. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            Telas.telaCliente(cur, conn)
        elif escolha == "2":
            print("\nVocê entrou como Gerente.\n")
        elif escolha == "3":
            print("\nVocê entrou como Atendente.\n")
        elif escolha == "4":
            print("\nSaindo...\n")
            break  
        else:
            print("\nOpção inválida! Tente novamente.\n")