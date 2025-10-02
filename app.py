# app.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    """Página inicial"""
    return render_template('estatico/index.html')

@app.route('/formulario')
def formulario():
    """Formulário"""
    return render_template('variavel/formulario/formulario.html')

@app.route('/definicao')
def definicao():
    """Definição"""
    return render_template('estatico/definicao.html')

@app.route('/identificar')
def identificar():
    """Como identificar"""
    return render_template('estatico/identificar.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)