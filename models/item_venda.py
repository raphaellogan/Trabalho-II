from config.db import conectar


# ==========================================
# ATUALIZAR ESTOQUE
# ==========================================

def atualizar_estoque_produto(id_produto, quantidade, operacao):
    if quantidade <= 0:
        raise ValueError("Quantidade inválida")

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        if operacao == "saida":
            cursor.execute(
                """
                    UPDATE produto
                    SET estoque = estoque - %s
                    WHERE id_produto = %s AND estoque >= %s
                """,
                (quantidade, id_produto, quantidade)
            )

            if cursor.rowcount == 0:
                raise ValueError("Estoque insuficiente para essa venda")

        elif operacao == "entrada":
            cursor.execute(
                """
                    UPDATE produto
                    SET estoque = estoque + %s
                    WHERE id_produto = %s
                """,
                (quantidade, id_produto)
            )

        else:
            raise ValueError("Operação de estoque inválida")

        conexao.commit()
        return cursor.rowcount

    except Exception:
        conexao.rollback()
        raise

    finally:
        cursor.close()
        conexao.close()


# ==========================================
# RENOVAR ESTOQUE (somar itens já existentes)
# ==========================================

def renovar_estoque(id_produto, quantidade):
    if quantidade <= 0:
        raise ValueError("Quantidade inválida")

    return atualizar_estoque_produto(id_produto, quantidade, "entrada")


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

    try:
        cursor.execute(
            "SELECT estoque FROM produto WHERE id_produto = %s",
            (id_produto,)
        )
        produto = cursor.fetchone()

        if not produto:
            raise ValueError("Produto não encontrado")

        estoque_atual = int(produto[0])
        if estoque_atual < int(quantidade):
            raise ValueError("Estoque insuficiente para essa venda")

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

        cursor.execute(
            "UPDATE produto SET estoque = estoque - %s WHERE id_produto = %s",
            (quantidade, id_produto)
        )

        conexao.commit()
        id_item = cursor.lastrowid
        return id_item

    except Exception:
        conexao.rollback()
        raise

    finally:
        cursor.close()
        conexao.close()


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

    try:
        cursor.execute(
            "SELECT id_produto, quantidade FROM item_venda WHERE id_item = %s",
            (id_item,)
        )
        item_antigo = cursor.fetchone()

        if not item_antigo:
            return 0

        produto_antigo_id = item_antigo[0]
        quantidade_antiga = int(item_antigo[1])

        if produto_antigo_id != id_produto:
            cursor.execute(
                "SELECT estoque FROM produto WHERE id_produto = %s",
                (id_produto,)
            )
            estoque = cursor.fetchone()
            if not estoque or int(estoque[0]) < int(quantidade):
                raise ValueError("Estoque insuficiente para a nova quantidade")

            cursor.execute(
                "UPDATE produto SET estoque = estoque + %s WHERE id_produto = %s",
                (quantidade_antiga, produto_antigo_id)
            )
            cursor.execute(
                "UPDATE produto SET estoque = estoque - %s WHERE id_produto = %s",
                (quantidade, id_produto)
            )
        elif quantidade != quantidade_antiga:
            diferenca = quantidade - quantidade_antiga
            if diferenca > 0:
                cursor.execute(
                    "SELECT estoque FROM produto WHERE id_produto = %s",
                    (id_produto,)
                )
                estoque = cursor.fetchone()
                if not estoque or int(estoque[0]) < int(diferenca):
                    raise ValueError("Estoque insuficiente para ajustar a venda")
                cursor.execute(
                    "UPDATE produto SET estoque = estoque - %s WHERE id_produto = %s",
                    (diferenca, id_produto)
                )
            else:
                cursor.execute(
                    "UPDATE produto SET estoque = estoque + %s WHERE id_produto = %s",
                    (abs(diferenca), id_produto)
                )

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

        return cursor.rowcount

    except Exception:
        conexao.rollback()
        raise

    finally:
        cursor.close()
        conexao.close()


# ==========================================
# EXCLUIR ITEM DA VENDA
# ==========================================

def excluir_item_venda(id_item):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            "SELECT id_produto, quantidade FROM item_venda WHERE id_item = %s",
            (id_item,)
        )
        item = cursor.fetchone()

        if not item:
            return 0

        id_produto = item[0]
        quantidade = int(item[1])

        sql = """
            DELETE FROM item_venda
            WHERE id_item = %s
        """

        cursor.execute(sql, (id_item,))
        cursor.execute(
            "UPDATE produto SET estoque = estoque + %s WHERE id_produto = %s",
            (quantidade, id_produto)
        )
        conexao.commit()

        return cursor.rowcount

    except Exception:
        conexao.rollback()
        raise

    finally:
        cursor.close()
        conexao.close()