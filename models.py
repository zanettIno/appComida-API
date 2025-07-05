import sqlite3

def iniciar_bd():
    conn = sqlite3.connect('appComida.db')
    c = conn.cursor()

    # CRIACAO DE TABELA DE USUARIO  
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
            id_usuario      INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_usuario    TEXT NOT NULL,
            email_usuario   TEXT NOT NULL UNIQUE,
            senha_usuario   TEXT NOT NULL)
    ''')

    # CRIACAO DE TABELA DAS COMIDAS
    c.execute('''
        CREATE TABLE IF NOT EXISTS comida (
            id_comida       INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_comida     TEXT NOT NULL,
            preco_comida    REAL NOT NULL)
    ''')

    # CRIACAO DE TABELA DE CARRINHO
    c.execute('''
        CREATE TABLE IF NOT EXISTS carrinho (
            id_carrinho     INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario      INTEGER NOT NULL,
            id_comida       INTEGER NOT NULL,
            quantidade      INTEGER NOT NULL,
            FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
            FOREIGN KEY (id_comida) REFERENCES comida(id_comida))
    ''')

    # CRIACAO DE TABELA DE PEDIDOS
    c.execute('''
        CREATE TABLE IF NOT EXISTS pedido (
            id_pedido       INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario      INTEGER NOT NULL,
            total_pedido    REAL NOT NULL,
            FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario))
    ''')

    conn.commit()
    conn.close()