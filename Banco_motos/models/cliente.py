from config.db import conectar


def criar_cliente(nome, cpf, telefone, email, endereco, aceite_lgpd, data_consentimento):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO cliente
        (nome, cpf, telefone, email, endereco, aceite_lgpd, data_consentimento)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(sql, (
        nome,
        cpf,
        telefone,
        email,
        endereco,
        aceite_lgpd,
        data_consentimento
    ))

    conexao.commit()
    cursor.close()
    conexao.close()


def listar_clientes():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * FROM cliente")

    clientes = cursor.fetchall()

    cursor.close()
    conexao.close()

    return clientes
def buscar_cliente_por_id(id_cliente):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM cliente WHERE id_cliente = %s",
        (id_cliente,)
    )

    cliente = cursor.fetchone()

    cursor.close()
    conexao.close()

    return cliente


