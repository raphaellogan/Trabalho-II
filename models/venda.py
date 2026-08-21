from config.db import conectar


# ==========================================
# CADASTRAR VENDA - POST
# ==========================================
def cadastrar_venda(data_venda, valor_total, id_cliente):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO venda
        (data_venda, valor_total, id_cliente)
        VALUES (%s, %s, %s)
    """

    valores = (
        data_venda,
        valor_total,
        id_cliente
    )

    cursor.execute(sql, valores)

    conexao.commit()

    id_venda = cursor.lastrowid

    cursor.close()
    conexao.close()

    return id_venda


# ==========================================
# LISTAR VENDAS - GET
# ==========================================
def listar_vendas():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            v.id_venda,
            v.data_venda,
            v.valor_total,
            v.id_cliente,
            c.nome AS cliente
        FROM venda v
        INNER JOIN cliente c
            ON v.id_cliente = c.id_cliente
    """)

    vendas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return vendas


# ==========================================
# BUSCAR VENDA POR ID - GET
# ==========================================
def buscar_venda_por_id(id_venda):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            v.id_venda,
            v.data_venda,
            v.valor_total,
            v.id_cliente,
            c.nome AS cliente
        FROM venda v
        INNER JOIN cliente c
            ON v.id_cliente = c.id_cliente
        WHERE v.id_venda = %s
    """, (id_venda,))

    venda = cursor.fetchone()

    cursor.close()
    conexao.close()

    return venda


# ==========================================
# ALTERAR VENDA - PUT
# ==========================================
def alterar_venda(
    id_venda,
    data_venda,
    valor_total,
    id_cliente
):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        UPDATE venda
        SET
            data_venda = %s,
            valor_total = %s,
            id_cliente = %s
        WHERE id_venda = %s
    """

    valores = (
        data_venda,
        valor_total,
        id_cliente,
        id_venda
    )

    cursor.execute(sql, valores)

    conexao.commit()

    linhas_alteradas = cursor.rowcount

    cursor.close()
    conexao.close()

    return linhas_alteradas


# ==========================================
# EXCLUIR / CANCELAR VENDA - DELETE
# ==========================================
def excluir_venda(id_venda):
    conexao = conectar()
    cursor = conexao.cursor()

    try:

        # Excluir primeiro os itens da venda
        cursor.execute("""
            DELETE FROM item_venda
            WHERE id_venda = %s
        """, (id_venda,))

        # Depois excluir a venda
        cursor.execute("""
            DELETE FROM venda
            WHERE id_venda = %s
        """, (id_venda,))

        linhas_excluidas = cursor.rowcount

        conexao.commit()

        return linhas_excluidas

    except Exception:
        conexao.rollback()
        raise

    finally:
        cursor.close()
        conexao.close()