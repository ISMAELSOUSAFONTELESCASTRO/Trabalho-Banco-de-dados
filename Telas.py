import psycopg2

def cadastroCliente(cur, conn):
    nome = input('Nome: ')
    cpf = int(input("Cpf: "))
    senha = input("Senha: ")

    cur.execute("""
        SELECT * FROM Cliente WHERE Cpf = %s
    """, (cpf,))

    cliente = cur.fetchone()
    if cliente:
        print("Cliente já cadastrado!")
        return

    cur.execute(f"""
        INSERT INTO Cliente (Cpf, nome, senha)
        VALUES ({cpf}, '{nome}', '{senha}')
""")
    conn.commit()
    print("Cadastro Realizado!")

def telaCompra(cur, conn):
    print("Lista de Produtos:")
    cur.execute("SELECT Id_Produto, Nome FROM Produto;")
    produtos = cur.fetchall()
    for codigo, nome in produtos:
        print(f"Código: {codigo}, Nome: {nome}")

def telaExcluirCadastro(cur, conn, cpf):
    escolha = int(input("Tem certeza que deseja excluir seu cadastro? (0 para não 1 para sim): "))
    if(escolha == 1):
        senha = input("Digite sua senha: ")
        cur.execute("DELETE FROM Cliente WHERE Cpf = %s AND senha = %s;", (cpf, senha))
        conn.commit()
        print("Cadastro excluido com sucesso")
    else:
        return

def acessar(cur, conn):
    
    cpf = int(input("Digite o CPF: "))
    senha = input("Digite a Senha: ")

    cur.execute("""
        SELECT * FROM Cliente WHERE Cpf = %s
    """, (cpf,))

    cliente = cur.fetchone()  

    if cliente:
        if cliente[2] == senha:  
            telaClienteAcesso(cur, conn, cpf)
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
            break  
        else:
            print("\nOpção inválida! Tente novamente.\n")

def telaAlterarDados(cur, conn, cpf):
    novo_nome = input("Digite o novo nome do cliente: ")
    nova_senha = input("Digite a nova senha do cliente: ")

    # Atualiza os dados do cliente no banco
    cur.execute("""
        UPDATE Cliente
        SET nome = %s, senha = %s
        WHERE Cpf = %s;
    """, (novo_nome, nova_senha, cpf))

    conn.commit()

def telaClienteAcesso(cur, conn, cpf):
    while True:  
        print("\n=== Bem-vindo Cliente ===")
        print("1. Comprar")
        print("2. Histórico")
        print("3. Alterar dados")
        print("4. Excluir cadastro")
        print("5. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            telaCompra(cur, conn)
        elif escolha == "2":
            print("...")
            #telaHistorico()
        elif escolha == "3":
            telaAlterarDados(cur, conn, cpf)
        elif escolha == "4":
            telaExcluirCadastro(cur, conn, cpf)
        elif escolha == "5":
            break  
        else:
            print("\nOpção inválida! Tente novamente.\n")