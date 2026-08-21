CREATE DATABASE IF NOT EXISTS banco_motos;
USE banco_motos;

-- =========================================
-- TABELA CLIENTE
-- =========================================

CREATE TABLE IF NOT EXISTS cliente (
    id_cliente INT AUTO_INCREMENT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL,
    endereco VARCHAR(150) NOT NULL,
    aceite_lgpd BOOLEAN NOT NULL default 0 ,
    data_consentimento DATETIME NULL,

    PRIMARY KEY (id_cliente),
    UNIQUE (cpf)
);

-- =========================================
-- TABELA CATEGORIA
-- =========================================

CREATE TABLE IF NOT EXISTS categoria (
    id_categoria INT AUTO_INCREMENT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(255) NOT NULL,

    PRIMARY KEY (id_categoria)
);

-- =========================================
-- TABELA FORNECEDOR
-- =========================================

CREATE TABLE IF NOT EXISTS fornecedor (
    id_fornecedor INT AUTO_INCREMENT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    cnpj VARCHAR(18) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL,

    PRIMARY KEY (id_fornecedor),
    UNIQUE (cnpj)
);

-- =========================================
-- TABELA PRODUTO
-- =========================================

CREATE TABLE IF NOT EXISTS produto (
    id_produto INT AUTO_INCREMENT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    estoque INT NOT NULL,
    id_categoria INT NOT NULL,
    id_fornecedor INT NOT NULL,
    cor VARCHAR(50),
    tamanho VARCHAR(20),
    codigo_de_barra VARCHAR(50) NOT NULL,

    PRIMARY KEY (id_produto),
    UNIQUE (codigo_de_barra),

    CONSTRAINT fk_produto_categoria
        FOREIGN KEY (id_categoria)
        REFERENCES categoria(id_categoria),

    CONSTRAINT fk_produto_fornecedor
        FOREIGN KEY (id_fornecedor)
        REFERENCES fornecedor(id_fornecedor)
);

-- =========================================
-- TABELA VENDA
-- =========================================

CREATE TABLE IF NOT EXISTS venda (
    id_venda INT AUTO_INCREMENT NOT NULL,
    data_venda DATE NOT NULL,
    valor_total DECIMAL(10,2) NOT NULL,
    id_cliente INT NOT NULL,

    PRIMARY KEY (id_venda),

    CONSTRAINT fk_venda_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES cliente(id_cliente)
);

-- =========================================
-- TABELA ITEM_VENDA
-- =========================================

CREATE TABLE IF NOT EXISTS item_venda (
    id_item INT AUTO_INCREMENT NOT NULL,
    id_venda INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,

    PRIMARY KEY (id_item),

    CONSTRAINT fk_item_venda
        FOREIGN KEY (id_venda)
        REFERENCES venda(id_venda),

    CONSTRAINT fk_item_produto
        FOREIGN KEY (id_produto)
        REFERENCES produto(id_produto)
);






