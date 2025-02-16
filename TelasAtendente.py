def acessar(cur, conn):
    id = int(input("Digite seu ID: "))
    senha = input("Digite sua Senha: ")

    cur.execute("""
        SELECT * FROM Atendente WHERE id_funcionario = %s
    """, (id,))

    atendente = cur.fetchone()

    cur.execute("""
        SELECT * FROM funcionario WHERE id_funcionario = %s
    """, (id,)) 
    
    funcionario = cur.fetchone() 

    if atendente:
        if funcionario[4] == senha:
            telaAtendenteAcesso(cur, conn, id)
        else:
            print("Senha incorreta para Atendente!")     
    elif funcionario:
        print("Id não correspondente a um Atendente")            
    else:
        print("Usuário não encontrado!")


def telaAtendenteAcesso(cur, conn, id):
    while True:  
        print("\n=== Bem-vindo - Atendente ===")
        print("\n1. Analisar venda")


        escolha = input("Escolha uma opção: ")
        if(escolha == '1'):
            analisar_vendasClientes(cur,conn)


def telaAtendente(cur, conn):
    while True:  
        print("\n=== Bem-vindo - Atendente ===")
        print("1. Acessar")
        print("2. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            acessar(cur, conn)
        elif escolha == "2":
            break  
        else:
            print("\nOpção inválida! Tente novamente.\n")
