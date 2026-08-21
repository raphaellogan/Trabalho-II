from Banco_motos.config.database import conectar


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

    cursor.execute("SELECT * FROM categoria")

    categorias = cursor.fetchall()

    cursor.close()
    conexao.close()

    return categorias