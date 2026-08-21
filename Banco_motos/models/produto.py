from Banco_motos.config.database import conectar


def cadastrar_produto(nome, descricao, preco, estoque, id_categoria, id_fornecedor, cor, tamanho, codigo_de_barra):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO produto
        (nome, descricao, preco, estoque, id_categoria, id_fornecedor, cor, tamanho, codigo_de_barra)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    valores = (
        nome,
        descricao,
        preco,
        estoque,
        id_categoria,
        id_fornecedor,
        cor,
        tamanho,
        codigo_de_barra
    )

    cursor.execute(sql, valores)
    conexao.commit()

    cursor.close()
    conexao.close()


def listar_produtos():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * FROM produto")

    produtos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return produtos