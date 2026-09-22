from config.db import conectar


def criar_categoria(nome, descricao):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO categoria
        (nome, descricao)
        VALUES (%s, %s)
    """

    cursor.execute(sql, (nome, descricao))
    conexao.commit()
    cursor.close()
    conexao.close()


def listar_categorias():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * FROM categoria ORDER BY nome ASC")
    categorias = cursor.fetchall()

    cursor.close()
    conexao.close()

    return categorias


def buscar_categoria_por_id(id_categoria):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * FROM categoria WHERE id_categoria = %s", (id_categoria,))
    categoria = cursor.fetchone()

    cursor.close()
    conexao.close()

    return categoria


def alterar_categoria(id_categoria, dados):
    conexao = conectar()
    cursor = conexao.cursor()

    campos_permitidos = ["nome", "descricao"]
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

    sql = f"UPDATE categoria SET {', '.join(campos)} WHERE id_categoria = %s"
    valores.append(id_categoria)
    cursor.execute(sql, valores)

    linhas_afetadas = cursor.rowcount
    conexao.commit()
    cursor.close()
    conexao.close()

    return linhas_afetadas


def excluir_categoria(id_categoria):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "DELETE FROM categoria WHERE id_categoria = %s"
    cursor.execute(sql, (id_categoria,))

    linhas_afetadas = cursor.rowcount
    conexao.commit()
    cursor.close()
    conexao.close()

    return linhas_afetadas