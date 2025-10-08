# app.py
from flask import Flask, render_template, request, jsonify
from db import get_db

app = Flask(__name__)
db = get_db()

@app.route('/')
def index():
    """Página inicial"""
    return render_template('estatico/index.html')

@app.route('/formulario')
def formulario():
    """Formulário com perguntas do banco"""
    try:
        perguntas = db.buscar_perguntas()
        print(f"✅ Carregadas {len(perguntas)} perguntas do banco")
        return render_template('variavel/formulario/formulario.html', perguntas=perguntas)
    except Exception as e:
        print(f"❌ Erro ao carregar perguntas: {e}")
        return "Erro ao carregar o formulário", 500

@app.route('/definicao')
def definicao():
    """Definição"""
    return render_template('estatico/definicao.html')

@app.route('/identificar')
def identificar():
    """Como identificar"""
    return render_template('estatico/identificar.html')

@app.route('/resultado')
def resultado():
    """Página de resultado do questionário"""
    perfil = request.args.get('perfil', '')
    pontuacao = request.args.get('pontuacao', '')
    descricao = request.args.get('descricao', '')
    
    return render_template('variavel/formulario/resultado.html', 
                         perfil=perfil, 
                         pontuacao=pontuacao, 
                         descricao=descricao)

@app.route('/salvar-resposta', methods=['POST'])
def salvar_resposta():
    """Salva as respostas do questionário no banco"""
    try:
        dados = request.get_json()
        respostas = dados.get('respostas', [])
        
        print(f"📝 Respostas recebidas: {respostas}")
        
        # Calcular soma total
        soma_total = sum(respostas)
        print(f"🧮 Soma total: {soma_total}")
        
        # Determinar perfil baseado na nova classificação
        if 10 <= soma_total <= 16:
            perfil = 'Alheio à Problemática'
            descricao = 'Você talvez não tenha vivenciado ou percebido o bullying de forma próxima. É importante se informar mais sobre o tema para ajudar a criar ambientes mais seguros.'
        elif 17 <= soma_total <= 23:
            perfil = 'Consciente mas Cauteloso'
            descricao = 'Você reconhece o bullying como um problema, mas pode hesitar em agir. Sua experiência é moderada, e há potencial para se tornar um aliado ativo.'
        elif 24 <= soma_total <= 30:
            perfil = 'Atuante na Causa'
            descricao = 'Você já vivenciou ou testemunhou bullying e tem uma postura proativa contra isso. Sua empatia e engajamento são fundamentais para mudanças.'
        else:
            perfil = 'Fora da faixa'
            descricao = 'Sua pontuação está fora da faixa esperada. Por favor, revise suas respostas.'
        
        print(f"🎯 Perfil determinado: {perfil}")
        
        # Salvar no banco
        if db.salvar_resposta_usuario(soma_total, perfil):
            print("✅ Resposta salva no banco com sucesso!")
            return jsonify({
                'success': True,
                'perfil': perfil,
                'pontuacao': soma_total,
                'descricao': descricao
            })
        else:
            print("❌ Erro ao salvar no banco")
            return jsonify({'success': False, 'error': 'Erro ao salvar no banco de dados'})
            
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)