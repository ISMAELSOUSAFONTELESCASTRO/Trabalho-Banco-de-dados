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



def analisar_vendasClientes(cur, conn):
    try:
        
       
        # Primeira consulta com INNER JOIN e GROUP BY
        cur.execute("""
            SELECT p.tipo, SUM(v.valor_total) as total_vendas 
            FROM vendas v
            INNER JOIN produtos p ON v.id_produto = p.nome
            GROUP BY p.tipo
            ORDER BY total_vendas DESC;
        """)
        
        print("Vendas por tipo de produto:")
        for registro in cur.fetchall():
            print(f"Tipo: {registro[0]}, Total Vendido: R${registro[1]:.2f}")

        # Segunda consulta com LEFT JOIN e GROUP BY
        cur.execute("""
            SELECT c.cpf, c.nome, COUNT(v.id_compra) as total_compras
            FROM clientes c
            LEFT JOIN vendas v ON c.cpf = v.cpf_cliente
            GROUP BY c.cpf, c.nome
            HAVING COUNT(v.id_compra) = 0;
        """)
        
        print("\nClientes sem compras realizadas:")
        for registro in cur.fetchall():
            print(f"CPF: {registro[0]}, Nome: {registro[1]}")

    

    except Exception as e:
        print(f"Erro durante a execução: {e}")
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()

        
