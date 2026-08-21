from Banco_motos.config.database import conectar


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
    """)

    vendas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return vendas