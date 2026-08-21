from config.db import conectar


# ==========================================
# CADASTRAR ITEM DA VENDA
# ==========================================

def cadastrar_item_venda(
    id_venda,
    id_produto,
    quantidade,
    preco_unitario
):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO item_venda
        (id_venda, id_produto, quantidade, preco_unitario)
        VALUES (%s, %s, %s, %s)
    """

    valores = (
        id_venda,
        id_produto,
        quantidade,
        preco_unitario
    )

    cursor.execute(sql, valores)
    conexao.commit()

    id_item = cursor.lastrowid

    cursor.close()
    conexao.close()

    return id_item


# ==========================================
# LISTAR ITENS DA VENDA
# ==========================================

def listar_itens_venda():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT
            id_item,
            id_venda,
            id_produto,
            quantidade,
            preco_unitario
        FROM item_venda
    """

    cursor.execute(sql)

    itens = cursor.fetchall()

    cursor.close()
    conexao.close()

    return itens


# ==========================================
# BUSCAR ITEM DA VENDA POR ID
# ==========================================

def buscar_item_venda(id_item):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT
            id_item,
            id_venda,
            id_produto,
            quantidade,
            preco_unitario
        FROM item_venda
        WHERE id_item = %s
    """

    cursor.execute(sql, (id_item,))

    item = cursor.fetchone()

    cursor.close()
    conexao.close()

    return item


# ==========================================
# ALTERAR ITEM DA VENDA
# ==========================================

def alterar_item_venda(
    id_item,
    id_produto,
    quantidade,
    preco_unitario
):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        UPDATE item_venda
        SET
            id_produto = %s,
            quantidade = %s,
            preco_unitario = %s
        WHERE id_item = %s
    """

    valores = (
        id_produto,
        quantidade,
        preco_unitario,
        id_item
    )

    cursor.execute(sql, valores)
    conexao.commit()

    linhas_alteradas = cursor.rowcount

    cursor.close()
    conexao.close()

    return linhas_alteradas


# ==========================================
# EXCLUIR ITEM DA VENDA
# ==========================================

def excluir_item_venda(id_item):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        DELETE FROM item_venda
        WHERE id_item = %s
    """

    cursor.execute(sql, (id_item,))
    conexao.commit()

    linhas_excluidas = cursor.rowcount

    cursor.close()
    conexao.close()

    return linhas_excluidas