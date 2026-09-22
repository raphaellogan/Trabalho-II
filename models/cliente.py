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
        bool(aceite_lgpd),
        data_consentimento
    ))

    conexao.commit()
    cursor.close()
    conexao.close()


def listar_clientes():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * FROM cliente ORDER BY nome ASC")
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


def atualizar_cliente(id_cliente, dados):
    conexao = conectar()
    cursor = conexao.cursor()

    campos_permitidos = [
        "nome",
        "cpf",
        "telefone",
        "email",
        "endereco",
        "aceite_lgpd",
        "data_consentimento"
    ]

    campos = []
    valores = []

    for campo in campos_permitidos:
        if campo in dados:
            campos.append(f"{campo} = %s")
            valores.append(bool(dados[campo]) if campo == "aceite_lgpd" else dados[campo])

    if not campos:
        cursor.close()
        conexao.close()
        return 0

    sql = f"UPDATE cliente SET {', '.join(campos)} WHERE id_cliente = %s"
    valores.append(id_cliente)
    cursor.execute(sql, valores)

    linhas_afetadas = cursor.rowcount
    conexao.commit()
    cursor.close()
    conexao.close()

    return linhas_afetadas


def cancelar_cliente(id_cliente):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "DELETE FROM cliente WHERE id_cliente = %s"
    cursor.execute(sql, (id_cliente,))

    linhas_afetadas = cursor.rowcount
    conexao.commit()
    cursor.close()
    conexao.close()

    return linhas_afetadas


