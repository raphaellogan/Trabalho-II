import mysql.connector


def conectar():
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="936565",
        database="banco_motos",
        port=3306
    )

    return conexao