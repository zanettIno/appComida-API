from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from models import iniciar_bd

app = Flask(__name__)
CORS(app)
iniciar_bd()

def conectar_bd():
    conn = sqlite3.connect('appComida.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return 'API rodando suavee'

# CADASTRO DE USUARIO
@app.route('/cadastro', methods=['POST'])
def cadastro_usuario():
    data = request.get_json()
    conn = conectar_bd()
    try:
        conn.execute('INSERT INTO usuario (nome_usuario, email_usuario, senha_usuario) VALUES (?, ?, ?)', (data['email'], data['nome'], data['senha']))
        conn.commit()
        return jsonify({'message': 'Usuário cadastrado com sucesso!'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email já cadastrado!'}), 400
    
# LOGIN DE USUARIO
@app.route('/login', methods=['POST'])
def login_usuario():
    data = request.get_json()
    conn = conectar_bd()
    user = conn.execute('SELECT * FROM usuario WHERE email_usuario = ? AND senha_usuario = ?', (data['email'], data['senha']))
    if user:
        return jsonify({'message': 'Login realizado com sucesso!'}), 200
    return jsonify({'error': 'Email ou senha incorretos!'}), 401

# LISTA DE COMIDAS
@app.route('/comidas', methods=['GET'])
def listar_comidas():
    conn = conectar_bd()
    comidas = conn.execute('SELECT * FROM comida').fetchall()
    return jsonify([dict(comida) for comida in comidas]), 200

# ADICIONAR COMIDA AO CARRINHO
@app.route('/carrinho', methods=['POST'])
def adicionar_carrinho():
    data = request.get_json()
    conn = conectar_bd()
    conn.execute('INSERT INTO carrinho (id_usuario, id_comida, quantidade) VALUES (?, ?, ?)', (data['id_usuario'], data['id_comida'], data['quantidade']))
    conn.commit()
    return jsonify({'message': 'Comida adicionada ao carrinho!'}), 201

# VER CARRINHO
@app.route('/carrinho/<int:id_usuario>', methods=['GET'])
def ver_carrinho(id_usuario):
    conn = conectar_bd()
    comidas = conn.execute('''
        SELECT c.id_carrinho, co.nome_comida, co.preco_comida, ca.quantidade
        FROM carrinho ca
        JOIN comida co ON ca.id_comida = co.id_comida
        WHERE ca.id_usuario = ?
    ''', (id_usuario,)).fetchall()
    
    carrinho = []
    for comida in comidas:
        subtotal = comida['preco_comida'] * comida['quantidade']
        total += subtotal
        carrinho.append({
            'id_carrinho': comida['id_carrinho'],
            'nome_comida': comida['nome_comida'],
            'preco_comida': comida['preco_comida'],
            'quantidade': comida['quantidade'],
            'subtotal': subtotal
        })

    return jsonify({'carrinho': carrinho, 'total': total}), 200

# FINALIZAR PEDIDO
@app.route('/pedido', methods=['POST'])
def realizar_pedido():
    data = request.get_json()
    id_usuario = data['id_usuario']

    conn = conectar_bd()
    carrinho = conn.execute('SELECT * FROM carrinho WHERE id_usuario = ?', 
    (id_usuario,)).fetchall()
    
    if not carrinho:
        return jsonify({'error': 'Carrinho vazio!'}), 400   

    total = sum(item['preco_comida'] * item['quantidade'] for item in carrinho)

    conn.execute('INSERT INTO pedido (id_usuario, total_pedido) VALUES (?, ?)', 
                 (id_usuario, total))
    conn.execute('DELETE FROM carrinho WHERE id_usuario = ?', (id_usuario,))
    conn.commit()      

    return jsonify({'message': 'Pedido realizado com sucesso!', 'total': total}), 201

if __name__ == '__main__':
    app.run(debug=True)