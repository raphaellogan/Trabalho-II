from config.db import conectar


def criar_fornecedor(nome, cnpj, telefone, email):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO fornecedor
        (nome, cnpj, telefone, email)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(sql, (
        nome,
        cnpj,
        telefone,
        email
    ))

    conexao.commit()
    cursor.close()
    conexao.close()


def listar_fornecedores():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    sql = "SELECT * FROM fornecedor ORDER BY nome ASC"
    cursor.execute(sql)
    fornecedores = cursor.fetchall()

    cursor.close()
    conexao.close()

    return fornecedores


def buscar_fornecedor_por_id(id_fornecedor):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * FROM fornecedor WHERE id_fornecedor = %s", (id_fornecedor,))
    fornecedor = cursor.fetchone()

    cursor.close()
    conexao.close()

    return fornecedor


def alterar_fornecedor(id_fornecedor, dados):
    conexao = conectar()
    cursor = conexao.cursor()

    campos_permitidos = ["nome", "cnpj", "telefone", "email"]
    campos = []
    valores = []

    for campo in campos_permitidos:
        if campo in dados:
            campos.append(f"{campo} = %s")
            valores.append(dados[campo])

    if not campos:
        cursor.close()
        conexao.close()
        return 0

    sql = f"UPDATE fornecedor SET {', '.join(campos)} WHERE id_fornecedor = %s"
    valores.append(id_fornecedor)
    cursor.execute(sql, valores)

    linhas_afetadas = cursor.rowcount
    conexao.commit()
    cursor.close()
    conexao.close()

    return linhas_afetadas


def deletar_fornecedor(id_fornecedor):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "DELETE FROM fornecedor WHERE id_fornecedor = %s"
    cursor.execute(sql, (id_fornecedor,))

    linhas_afetadas = cursor.rowcount
    conexao.commit()
    cursor.close()
    conexao.close()

    return linhas_afetadas