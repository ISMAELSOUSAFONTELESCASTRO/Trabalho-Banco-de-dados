import TelasCliente
import TelasGerente
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
            TelasCliente.telaCliente(cur, conn)
        elif escolha == "2":
            TelasGerente.telaGerente(cur, conn)
        elif escolha == "3":
            print("\nVocê entrou como Atendente.\n")
        elif escolha == "4":
            print("\nSaindo...\n")
            break  
        else:
            print("\nOpção inválida! Tente novamente.\n")