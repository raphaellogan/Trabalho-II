from Banco_motos.config.database import conectar


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

    sql = "SELECT * FROM fornecedor"

    cursor.execute(sql)
    fornecedores = cursor.fetchall()

    cursor.close()
    conexao.close()

    return fornecedores