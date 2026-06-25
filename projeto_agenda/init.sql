USE agenda_contatos;
CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    descricao VARCHAR(255)
);
CREATE TABLE contatos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    notificacoes BOOLEAN DEFAULT FALSE,
    categoria_id INT NOT NULL,

    FOREIGN KEY (categoria_id)
        REFERENCES categorias(id)
);
CREATE TABLE enderecos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rua VARCHAR(150) NOT NULL,
    numero VARCHAR(20) NOT NULL,
    bairro VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado VARCHAR(50) NOT NULL,
    cep VARCHAR(20) NOT NULL
);
CREATE TABLE telefones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(30) NOT NULL,
    contato_id INT NOT NULL,

    FOREIGN KEY (contato_id)
        REFERENCES contatos(id)
        ON DELETE CASCADE
);
CREATE TABLE emails (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) NOT NULL,
    contato_id INT NOT NULL,

    FOREIGN KEY (contato_id)
        REFERENCES contatos(id)
        ON DELETE CASCADE
);
CREATE TABLE contato_endereco (
    contato_id INT NOT NULL,
    endereco_id INT NOT NULL,

    PRIMARY KEY (contato_id, endereco_id),

    FOREIGN KEY (contato_id)
        REFERENCES contatos(id)
        ON DELETE CASCADE,

    FOREIGN KEY (endereco_id)
        REFERENCES enderecos(id)
        ON DELETE CASCADE
);CREATE TABLE categorias (     id INT AUTO_INCREMENT PRIMARY KEY,     nome VARCHAR(100) NOT NULL UNIQUE,     descricao VARCHAR(255) )
