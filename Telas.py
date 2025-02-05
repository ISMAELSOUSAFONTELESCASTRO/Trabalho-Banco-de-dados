import psycopg2


def cadastroCliente(cur, conn):
    nome = input('Nome: ')
    cpf = int(input("Cpf: "))
    senha = input("Senha: ")
    cur.execute(f"""
        INSERT INTO Cliente (Cpf, nome, senha)
        VALUES ({cpf}, '{nome}', '{senha}')
""")
    conn.commit()
    print("Cadastro Realizado!")


def acessar(cur, conn):
    
    cpf = int(input("Digite o CPF: "))
    senha = input("Digite a Senha: ")

    # Consulta SQL para verificar se o CPF e a senha correspondem
    cur.execute("""
        SELECT * FROM Cliente WHERE Cpf = %s
    """, (cpf,))

    # Verifica se o CPF foi encontrado
    cliente = cur.fetchone()  # Retorna a primeira linha ou None se não encontrar

    if cliente:  # Se o CPF for encontrado
        # O formato do retorno é: (Cpf, nome, senha), então compare a senha
        if cliente[2] == senha:  # cliente[2] é a senha
            print("Login realizado com sucesso!")
        else:
            print("Senha incorreta!")
    else:
        print("Cliente não encontrado!")


def telaCliente(cur, conn):
    while True:  
        print("\n=== Bem-vindo Cliente ===")
        print("1. Acessar")
        print("2. Cadastrar")
        print("3. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            acessar(cur, conn)
        elif escolha == "2":
            cadastroCliente(cur, conn)
        elif escolha == "3":
            print("\nSaindo...\n")
            break  
        else:
            print("\nOpção inválida! Tente novamente.\n")

