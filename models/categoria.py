from config.db import conectar


# ==========================================
# CRIAR CATEGORIA
# ==========================================
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


# ==========================================
# LISTAR CATEGORIAS
# ==========================================
def listar_categorias():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * FROM categoria")

    categorias = cursor.fetchall()

    cursor.close()
    conexao.close()

    return categorias


# ==========================================
# BUSCAR CATEGORIA POR NOME
# ==========================================
def buscar_categoria_por_nome(nome):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM categoria WHERE nome = %s",
        (nome,)
    )

    categoria = cursor.fetchone()

    cursor.close()
    conexao.close()

    return categoria


# ==========================================
# BUSCAR CATEGORIA POR ID
# ==========================================
def buscar_categoria_por_id(id_categoria):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM categoria WHERE id_categoria = %s",
        (id_categoria,)
    )

    categoria = cursor.fetchone()

    cursor.close()
    conexao.close()

    return categoria


# ==========================================
# ALTERAR CATEGORIA
# ==========================================
def alterar_categoria(id_categoria, nome, descricao):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        UPDATE categoria
        SET nome = %s,
            descricao = %s
        WHERE id_categoria = %s
    """

    cursor.execute(
        sql,
        (nome, descricao, id_categoria)
    )

    conexao.commit()

    linhas_alteradas = cursor.rowcount

    cursor.close()
    conexao.close()

    return linhas_alteradas


# ==========================================
# EXCLUIR CATEGORIA
# ==========================================
def excluir_categoria(id_categoria):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        DELETE FROM categoria
        WHERE id_categoria = %s
    """

    cursor.execute(
        sql,
        (id_categoria,)
    )

    conexao.commit()

    linhas_excluidas = cursor.rowcount

    cursor.close()
    conexao.close()

    return linhas_excluidas