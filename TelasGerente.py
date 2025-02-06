def acessar(cur, conn):
    id = int(input("Digite seu ID: "))
    senha = input("Digite sua Senha: ")

    cur.execute("""
        SELECT * FROM Gerente WHERE id_funcionario = %s
    """, (id,))

    gerente = cur.fetchone()

    cur.execute("""
        SELECT * FROM funcionario WHERE id_funcionario = %s
    """, (id,)) 
    
    funcionario = cur.fetchone() 

    if gerente:
        if funcionario[4] == senha: 
            print("Acesso concedido como Gerente.")
            #telaGerenteAcesso(cur, conn, id)
        else:
            print("Senha incorreta para Gerente!")     
    elif funcionario:
        print("Id não correspondente a um gerente")            
    else:
        print("Usuário não encontrado!")

def cadastroGerente(cur, conn):
    nome = input('Nome: ')
    senha = input("Senha: ")
    idade = int(input('Idade: '))
    salario = float(input("Salário: "))
    id_mercearia = int(input("ID da Mercearia: "))

    cur.execute("""
    INSERT INTO Funcionario (Nome, senha, Idade, Salario)
    VALUES (%s, %s, %s, %s) RETURNING Id_Funcionario;
""", (nome, senha, idade, salario))

    gerente = cur.fetchone()

    id_funcionario = gerente[0]

    cur.execute("""
        INSERT INTO Gerente (Id_Funcionario, Id_Mercearia)
        VALUES (%s, %s);
    """, (id_funcionario, id_mercearia))

    conn.commit()
    print(f"Gerente cadastrado com sucesso! ID: {id_funcionario}")

def telaGerente(cur, conn):
    while True:  
        print("\n=== Bem-vindo - Gerente ===")
        print("1. Acessar")
        print("2. Cadastrar")
        print("3. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            acessar(cur, conn)
        elif escolha == "2":
            cadastroGerente(cur, conn)
        elif escolha == "3":
            break  
        else:
            print("\nOpção inválida! Tente novamente.\n")