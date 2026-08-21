from config.db import conectar
from datetime import datetime


# ==========================================
# CADASTRAR CLIENTE
# ==========================================
def criar_cliente(
    nome,
    cpf,
    telefone,
    email,
    endereco,
    aceite_lgpd
):
    conexao = conectar()
    cursor = conexao.cursor()

    # Gera automaticamente a data do consentimento
    if aceite_lgpd:
        data_consentimento = datetime.now()
    else:
        data_consentimento = None

    sql = """
        INSERT INTO cliente
        (
            nome,
            cpf,
            telefone,
            email,
            endereco,
            aceite_lgpd,
            data_consentimento
        )
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


# ==========================================
# LISTAR CLIENTES
# ==========================================
def listar_clientes():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * FROM cliente")

    clientes = cursor.fetchall()

    cursor.close()
    conexao.close()

    return clientes


# ==========================================
# BUSCAR CLIENTE POR ID
# ==========================================
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


# ==========================================
# BUSCAR CLIENTE POR CPF
# ==========================================
def buscar_cliente_por_cpf(cpf):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM cliente WHERE cpf = %s",
        (cpf,)
    )

    cliente = cursor.fetchone()

    cursor.close()
    conexao.close()

    return cliente


# ==========================================
# ALTERAR CLIENTE
# ==========================================
def atualizar_cliente(
    id_cliente,
    nome,
    cpf,
    telefone,
    email,
    endereco,
    aceite_lgpd
):
    conexao = conectar()
    cursor = conexao.cursor()

    # Atualiza automaticamente a data do consentimento
    if aceite_lgpd:
        data_consentimento = datetime.now()
    else:
        data_consentimento = None

    sql = """
        UPDATE cliente
        SET
            nome = %s,
            cpf = %s,
            telefone = %s,
            email = %s,
            endereco = %s,
            aceite_lgpd = %s,
            data_consentimento = %s
        WHERE id_cliente = %s
    """

    cursor.execute(sql, (
        nome,
        cpf,
        telefone,
        email,
        endereco,
        aceite_lgpd,
        data_consentimento,
        id_cliente
    ))

    conexao.commit()

    cursor.close()
    conexao.close()


# ==========================================
# CANCELAR CLIENTE
# ==========================================
def cancelar_cliente(id_cliente):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM cliente WHERE id_cliente = %s",
        (id_cliente,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()