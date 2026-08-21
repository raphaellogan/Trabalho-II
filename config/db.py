import mysql.connector
from mysql.connector import Error


def conectar():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="936565",
            database="banco_motos"
        )

        return conexao

    except Error as erro:
        print(f"Erro ao conectar ao banco: {erro}")
        return None