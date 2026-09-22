CREATE DATABASE IF NOT EXISTS banco_motos;
USE banco_motos;

-- =========================================
-- CLIENTE
-- =========================================
CREATE TABLE IF NOT EXISTS cliente (
    id_cliente INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) NOT NULL,
    telefone VARCHAR(20) NULL,
    email VARCHAR(100) NULL,
    endereco VARCHAR(150) NULL,
    aceite_lgpd BOOLEAN NOT NULL DEFAULT 0,
    data_consentimento DATETIME NULL,

    PRIMARY KEY (id_cliente),
    UNIQUE KEY uq_cliente_cpf (cpf)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =========================================
-- CATEGORIA
-- =========================================
CREATE TABLE IF NOT EXISTS categoria (
    id_categoria INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(255) NOT NULL,

    PRIMARY KEY (id_categoria)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =========================================
-- FORNECEDOR
-- =========================================
CREATE TABLE IF NOT EXISTS fornecedor (
    id_fornecedor INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    cnpj VARCHAR(18) NOT NULL,
    telefone VARCHAR(20) NULL,
    email VARCHAR(100) NULL,

    PRIMARY KEY (id_fornecedor),
    UNIQUE KEY uq_fornecedor_cnpj (cnpj)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =========================================
-- PRODUTO
-- =========================================
CREATE TABLE IF NOT EXISTS produto (
    id_produto INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    estoque INT NOT NULL DEFAULT 0,
    id_categoria INT NOT NULL,
    id_fornecedor INT NOT NULL,
    cor VARCHAR(50) NULL,
    tamanho VARCHAR(20) NULL,
    codigo_de_barra VARCHAR(50) NOT NULL,

    PRIMARY KEY (id_produto),
    UNIQUE KEY uq_produto_codigo_barras (codigo_de_barra),

    CONSTRAINT fk_produto_categoria
        FOREIGN KEY (id_categoria)
        REFERENCES categoria (id_categoria),

    CONSTRAINT fk_produto_fornecedor
        FOREIGN KEY (id_fornecedor)
        REFERENCES fornecedor (id_fornecedor)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =========================================
-- VENDA
-- =========================================
CREATE TABLE IF NOT EXISTS venda (
    id_venda INT NOT NULL AUTO_INCREMENT,
    data_venda DATE NOT NULL,
    valor_total DECIMAL(10,2) NOT NULL,
    id_cliente INT NOT NULL,

    PRIMARY KEY (id_venda),

    CONSTRAINT fk_venda_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES cliente (id_cliente)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =========================================
-- ITEM_VENDA
-- =========================================
CREATE TABLE IF NOT EXISTS item_venda (
    id_item INT NOT NULL AUTO_INCREMENT,
    id_venda INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,

    PRIMARY KEY (id_item),

    CONSTRAINT fk_item_venda_venda
        FOREIGN KEY (id_venda)
        REFERENCES venda (id_venda)
        ON DELETE CASCADE,

    CONSTRAINT fk_item_venda_produto
        FOREIGN KEY (id_produto)
        REFERENCES produto (id_produto)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =========================================
-- ÍNDICES ÚTEIS
-- =========================================
CREATE INDEX idx_produto_categoria ON produto (id_categoria);
CREATE INDEX idx_produto_fornecedor ON produto (id_fornecedor);
CREATE INDEX idx_venda_cliente ON venda (id_cliente);
CREATE INDEX idx_item_venda_venda ON item_venda (id_venda);
CREATE INDEX idx_item_venda_produto ON item_venda (id_produto);

