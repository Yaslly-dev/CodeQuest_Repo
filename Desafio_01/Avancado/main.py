import sqlite3
import os
from flask import Flask, render_template, request, jsonify

# Garante que o banco seja criado na pasta do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

app = Flask(
    __name__,
    static_folder='static',    # Sintaxe: Nome da pasta de arquivos estáticos
    template_folder='templates' # Sintaxe: Nome da pasta de HTMLs
)

def get_db_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conteudo TEXT,
            coluna TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_notes', methods=['GET'])
def get_notes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, conteudo, coluna FROM notas")
    notas = cursor.fetchall()
    conn.close()
    return jsonify(notas)

@app.route('/save_note', methods=['POST'])
def save_note():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notas (conteudo, coluna) VALUES (?, ?)",
                   (data['conteudo'], data['coluna']))
    novo_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jsonify({"id": novo_id})

@app.route('/update_note', methods=['POST'])
def update_note():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE notas SET conteudo = ?, coluna = ? WHERE id = ?",
                   (data['conteudo'], data['coluna'], data['id']))
    conn.commit()
    conn.close()
    return jsonify({"status": "sucesso"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
