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
            telaGerenteAcesso(cur, conn, id)
        else:
            print("Senha incorreta para Gerente!")     
    elif funcionario:
        print("Id não correspondente a um gerente")            
    else:
        print("Usuário não encontrado!")

def telaAlterarDados(cur, conn, id_funcionario):
    print("\nEscolha o dado que deseja alterar:")
    print("1. Nome")
    print("2. Senha")
    print("3. Data de Contratação")
    print("4. Idade")
    print("5. Salário")
    print("6. Sair")
    
    opcao = input("Digite o número da opção que deseja alterar: ")

    if opcao == "1":
        novo_nome = input("Digite o novo nome: ")
        cur.execute("""
            UPDATE Funcionario 
            SET nome = %s
            WHERE id_funcionario = %s
        """, (novo_nome, id_funcionario))
    
    elif opcao == "2":
        nova_senha = input("Digite a nova senha: ")
        cur.execute("""
            UPDATE Funcionario 
            SET senha = %s
            WHERE id_funcionario = %s
        """, (nova_senha, id_funcionario))
    
    elif opcao == "3":
        nova_data_contr = input("Digite a nova data de contratação (AAAA-MM-DD): ")
        cur.execute("""
            UPDATE Funcionario 
            SET data_contr = %s
            WHERE id_funcionario = %s
        """, (nova_data_contr, id_funcionario))
    
    elif opcao == "4":
        nova_idade = int(input("Digite a nova idade: "))
        cur.execute("""
            UPDATE Funcionario 
            SET idade = %s
            WHERE id_funcionario = %s
        """, (nova_idade, id_funcionario))
    
    elif opcao == "5":
        novo_salario = float(input("Digite o novo salário: "))
        cur.execute("""
            UPDATE Funcionario 
            SET salario = %s
            WHERE id_funcionario = %s
        """, (novo_salario, id_funcionario))
    elif opcao == "6":
        return   
    else:
        print("Opção inválida!")

    # Confirma a atualização no banco de dados
    conn.commit()
    print("Dado alterado com sucesso!")

def telaExcluirCadastro(cur, conn, id_funcionario):
    escolha = int(input("Tem certeza que deseja excluir seu cadastro? (0 para não, 1 para sim): "))
    
    if escolha == 1:
        senha = input("Digite sua senha: ")

        cur.execute("""
            SELECT * FROM Funcionario WHERE id_funcionario = %s
        """, (id_funcionario,))
        funcionario = cur.fetchone()

        if funcionario:
            if funcionario[4] == senha:
                cur.execute("""
                    DELETE FROM Gerente WHERE id_funcionario = %s;
                """, (id_funcionario,))

                cur.execute("""
                    DELETE FROM Funcionario WHERE id_funcionario = %s AND senha = %s;
                """, (id_funcionario, senha))

                conn.commit()
                print("Cadastro excluído com sucesso")
            else:
                print("Senha incorreta!")
        else:
            print("Gerente não encontrado!")
    
    else:
        print("Exclusão cancelada.")
    
def telaContratarAtendente(cur, conn):
    nome = input("Nome do funcionário: ")
    idade = int(input("Idade do funciário: "))
    salario = float(input("Salário do funcionário: "))
    senha = input("Senha de acesso do funcionário: ")

    cur.execute("""
    INSERT INTO Funcionario (Nome, senha, Idade, Salario)
    VALUES (%s, %s, %s, %s) RETURNING Id_Funcionario;
""", (nome, senha, idade, salario))
    
    atendente = cur.fetchone()

    id_funcionario = atendente[0]
    
    cur.execute("""
        INSERT INTO Atendente (Id_Funcionario, numero_vendas_mes)
        VALUES (%s, %s);
    """, (id_funcionario, 0))

    conn.commit()
    print(f"Atendente cadastrado com sucesso! ID: {id_funcionario}")

def telaVerEstoque(cur, conn):
    # Exibe todos os itens do estoque
    cur.execute("SELECT Id_Produto, Nome, Preco, Quantidade_Estoque, Tipo_Produto FROM Produto")
    produtos = cur.fetchall()

    if produtos:
        print("\nEstoque atual:")
        for produto in produtos:
            print(f"ID: {produto[0]} | Nome: {produto[1]} | Preço: {produto[2]} | Estoque: {produto[3]} | Tipo: {produto[4]}")
    else:
        print("Nenhum produto no estoque.")

    while True:
        # Pergunta se o usuário deseja filtrar ou sair
        escolha = input("\nDeseja filtrar o estoque ou sair? (1 para filtrar, 2 para sair): ")

        if escolha == "1":
            filtro = input("\nEscolha o tipo de filtro (ID ou Tipo): ").strip().lower()  # Tornar o filtro em minúsculas
            if filtro == "id":
                try:
                    id_produto = int(input("\nDigite o ID do produto: "))
                    cur.execute("SELECT Id_Produto, Nome, Preco, Quantidade_Estoque, Tipo_Produto FROM Produto WHERE Id_Produto = %s", (id_produto,))
                    produto = cur.fetchone()

                    if produto:
                        print(f"\nProduto encontrado: ID: {produto[0]} | Nome: {produto[1]} | Preço: {produto[2]} | Estoque: {produto[3]} | Tipo: {produto[4]}")
                    else:
                        print("\nProduto não encontrado com esse ID.")

                except ValueError:
                    print("\nPor favor, insira um número válido para o ID.")

            elif filtro == "tipo":
                tipo_produto = input("\nDigite o tipo do produto: ").strip().lower()  # Remover espaços e converter para minúsculas
                cur.execute("SELECT Id_Produto, Nome, Preco, Quantidade_Estoque, Tipo_Produto FROM Produto WHERE LOWER(TRIM(Tipo_Produto)) = %s", (tipo_produto,))
                produtos = cur.fetchall()

                if produtos:
                    print("\nProdutos encontrados:")
                    for produto in produtos:
                        print(f"ID: {produto[0]} | Nome: {produto[1]} | Preço: {produto[2]} | Estoque: {produto[3]} | Tipo: {produto[4]}")
                else:
                    print("\nTipo de produto não encontrado.")
            else:
                print("\nOpção inválida. Escolha 'id' ou 'tipo'.")
        elif escolha == "2":
            print("\nSaindo...")
            break
        else:
            print("\nOpção inválida. Digite 1 para filtrar ou 2 para sair.")


def telaReporEstoque(cur, conn):
    while True:
        print("\n=== Bem-vindo - Repor estoque ===")
        print("1. Adicionar/Repor item")
        print("2. Adicionar/Repor lista de itens")
        print("3. Visualizar estoque")
        print("4. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            reporItem(cur, conn)
        elif escolha == "2":
            reporListaItens(cur, conn)
        elif escolha == '3':
            telaVerEstoque(cur, conn)
        elif escolha == "4":
            break 
        else:
            print("\nOpção inválida! Tente novamente.\n")

def reporItem(cur, conn):
    nome = input("Nome do produto: ")
    preco = float(input("Preço: "))
    quantidade_estoque = int(input("Quantidade em estoque: "))
    tipo = input("Tipo do produto (ex: higiene, alimento, etc.): ")

    cur.execute("SELECT Id_Produto, Quantidade_Estoque FROM Produto WHERE Nome = %s", (nome,))
    produto = cur.fetchone()

    if produto:
        id_produto, estoque_atual = produto
        novo_estoque = estoque_atual + quantidade_estoque
        cur.execute("""
            UPDATE Produto 
            SET Quantidade_Estoque = %s, Preco = %s, Tipo = %s
            WHERE Id_Produto = %s
        """, (novo_estoque, preco, tipo, id_produto))
    else:
        cur.execute("""
            INSERT INTO Produto (Nome, Preco, Quantidade_Estoque, Tipo_produto)
            VALUES (%s, %s, %s, %s)
        """, (nome, preco, quantidade_estoque, tipo))

    conn.commit()
    print("Produto adicionado/atualizado com sucesso!")
    
def reporListaItens(cur, conn):
    arquivo = input("Nome do arquivo: ") + ".txt"

    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            linhas = f.readlines()

        for linha in linhas:
            dados = linha.strip().split(",") 
            if len(dados) == 4:  
                nome = dados[0]
                preco = float(dados[1])
                quantidade_estoque = int(dados[2])
                tipo_produto = dados[3]  

                cur.execute("SELECT Id_Produto, Quantidade_Estoque FROM Produto WHERE Nome = %s", (nome,))
                produto = cur.fetchone()

                if produto:
                    id_produto, estoque_atual = produto
                    novo_estoque = estoque_atual + quantidade_estoque

                    cur.execute("""
                        UPDATE Produto 
                        SET Quantidade_Estoque = %s, Preco = %s, Tipo_Produto = %s
                        WHERE Id_Produto = %s
                    """, (novo_estoque, preco, tipo_produto, id_produto))
                else:
                    cur.execute("""
                        INSERT INTO Produto (Nome, Preco, Quantidade_Estoque, Tipo_Produto)
                        VALUES (%s, %s, %s, %s)
                    """, (nome, preco, quantidade_estoque, tipo_produto))

        conn.commit()
        print("Estoque atualizado com sucesso!")

    except FileNotFoundError:
        print("O nome do arquivo está errado ou o arquivo não foi encontrado.")

def telaGerenteAcesso(cur, conn, id):
    while True:  
        print("\n=== Bem-vindo - Gerente ===")
        print("1. Estoque")
        print("2. Contratar atendente")
        print("3. Alterar dados")
        print("4. Excluir cadastro")
        print("5. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            telaReporEstoque(cur, conn)
        elif escolha == "2":
            telaContratarAtendente(cur, conn)
        elif escolha == "3":
            telaAlterarDados(cur, conn, id)
        elif escolha == "4":
            telaExcluirCadastro(cur, conn, id)
            break
        elif escolha == "5":
            break  
        else:
            print("\nOpção inválida! Tente novamente.\n")

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