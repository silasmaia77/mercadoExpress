import sqlite3
from datetime import datetime
import os

DB_PATH = "data/mercado.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabela de Pedidos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_nome TEXT,
            cliente_telefone TEXT,
            endereco TEXT,
            itens TEXT,
            total REAL,
            metodo_pagamento TEXT,
            data_pedido DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def salvar_pedido_db(nome, telefone, endereco, itens, total, metodo):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO pedidos (cliente_nome, cliente_telefone, endereco, itens, total, metodo_pagamento)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nome, telefone, endereco, itens, total, metodo))
    pedido_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return pedido_id

def buscar_pedidos_quinzena():
    # Lógica simplificada para pegar tudo (pode ser filtrado por data)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pedidos")
    dados = cursor.fetchall()
    conn.close()
    return dados
