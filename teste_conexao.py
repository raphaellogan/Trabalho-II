from config.db import conectar

conexao = conectar()

if conexao.is_connected():
    print("CONEXÃO COM MYSQL OK!")

conexao.close()