from config.db import conectar


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
        ORDER BY v.data_venda DESC
    """)

    vendas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return vendas


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


def alterar_venda(id_venda, data_venda, valor_total, id_cliente):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        UPDATE venda
        SET data_venda = %s,
            valor_total = %s,
            id_cliente = %s
        WHERE id_venda = %s
    """

    cursor.execute(sql, (data_venda, valor_total, id_cliente, id_venda))
    linhas_afetadas = cursor.rowcount

    conexao.commit()
    cursor.close()
    conexao.close()

    return linhas_afetadas


def excluir_venda(id_venda):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM item_venda WHERE id_venda = %s", (id_venda,))
    cursor.execute("DELETE FROM venda WHERE id_venda = %s", (id_venda,))

    linhas_afetadas = cursor.rowcount
    conexao.commit()
    cursor.close()
    conexao.close()

    return linhas_afetadas