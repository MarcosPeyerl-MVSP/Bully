# app.py
from flask import Flask, render_template, request, jsonify
from formDB import get_db as get_form_db
from cadDB import get_db as get_cad_db

app = Flask(__name__)

# Inicializa ambos os bancos de dados
form_db = get_form_db()  # Sistema de bullying
cad_db = get_cad_db()    # Sistema de escolas

@app.route('/')
def index():
    """Página inicial"""
    try:
        # Estatísticas do sistema de escolas
        escolas = cad_db.buscar_escolas()
        usuarios = cad_db.buscar_usuarios()
        publicacoes = cad_db.buscar_publicacoes()
        
        # Estatísticas do sistema de bullying
        stats_bullying = form_db.buscar_estatisticas()
        
        # Últimas publicações
        ultimas_publicacoes = publicacoes[:5] if publicacoes else []
        
        return render_template('estatico/index.html', 
                             total_escolas=len(escolas),
                             total_usuarios=len(usuarios),
                             total_publicacoes=len(publicacoes),
                             ultimas_publicacoes=ultimas_publicacoes,
                             stats_bullying=stats_bullying)
    except Exception as e:
        print(f"❌ Erro na página inicial: {e}")
        return render_template('estatico/index.html')

# ========== ROTAS DO SISTEMA DE BULLYING (formDB) ==========

@app.route('/formulario')
def formulario():
    """Formulário com perguntas do banco"""
    try:
        perguntas = form_db.buscar_perguntas()
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
        if form_db.salvar_resposta_usuario(soma_total, perfil):
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

@app.route('/estatisticas-bullying')
def estatisticas_bullying():
    """Página de estatísticas do sistema de bullying"""
    try:
        stats = form_db.buscar_estatisticas()
        return render_template('variavel/formulario/estatisticas.html', stats=stats)
    except Exception as e:
        print(f"❌ Erro ao carregar estatísticas: {e}")
        return "Erro ao carregar estatísticas", 500

# ========== ROTAS DO SISTEMA DE ESCOLAS (cadDB) ==========

@app.route('/escolas')
def listar_escolas():
    """Lista todas as escolas"""
    try:
        escolas = cad_db.buscar_escolas()
        return render_template('variavel/escolas/escolas.html', escolas=escolas)
    except Exception as e:
        print(f"❌ Erro ao carregar escolas: {e}")
        return "Erro ao carregar escolas", 500

@app.route('/escola/<int:id>')
def detalhes_escola(id):
    """Detalhes de uma escola específica"""
    try:
        escola = cad_db.buscar_escola_por_id(id)
        if not escola:
            return "Escola não encontrada", 404
            
        publicacoes = cad_db.buscar_publicacoes_por_escola(id)
        usuarios = cad_db.buscar_usuarios()  # Filtraremos por escola no template ou criaremos método específico
        
        # Filtrar usuários por escola
        usuarios_escola = [u for u in usuarios if u['id_escola'] == id]
        
        return render_template('variavel/escolas/detalhes_escola.html', 
                             escola=escola, 
                             publicacoes=publicacoes,
                             usuarios=usuarios_escola)
    except Exception as e:
        print(f"❌ Erro ao carregar escola: {e}")
        return "Escola não encontrada", 404

@app.route('/usuarios')
def listar_usuarios():
    """Lista todos os usuários"""
    try:
        usuarios = cad_db.buscar_usuarios()
        return render_template('variavel/usuarios/usuarios.html', usuarios=usuarios)
    except Exception as e:
        print(f"❌ Erro ao carregar usuários: {e}")
        return "Erro ao carregar usuários", 500

@app.route('/usuario/novo', methods=['GET', 'POST'])
def novo_usuario():
    """Cria um novo usuário"""
    if request.method == 'POST':
        try:
            id_user = cad_db.criar_usuario(
                id_escola=request.form['id_escola'],
                nome_user=request.form['nome_user'],
                username_user=request.form['username_user'],
                email_user=request.form['email_user']
            )
            if id_user:
                print(f"✅ Novo usuário criado com ID: {id_user}")
                return jsonify({'success': True, 'message': 'Usuário criado com sucesso!'})
            else:
                return jsonify({'success': False, 'error': 'Erro ao criar usuário'})
        except Exception as e:
            print(f"❌ Erro ao criar usuário: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    try:
        escolas = cad_db.buscar_escolas()
        return render_template('variavel/usuarios/novo_usuario.html', escolas=escolas)
    except Exception as e:
        print(f"❌ Erro ao carregar formulário de usuário: {e}")
        return "Erro ao carregar formulário", 500

@app.route('/publicacoes')
def listar_publicacoes():
    """Lista todas as publicações"""
    try:
        publicacoes = cad_db.buscar_publicacoes()
        return render_template('variavel/publicacoes/publicacoes.html', publicacoes=publicacoes)
    except Exception as e:
        print(f"❌ Erro ao carregar publicações: {e}")
        return "Erro ao carregar publicações", 500

@app.route('/publicacao/nova', methods=['GET', 'POST'])
def nova_publicacao():
    """Cria uma nova publicação"""
    if request.method == 'POST':
        try:
            id_publi = cad_db.criar_publicacao(
                id_user=request.form['id_user'],
                id_escola=request.form['id_escola'],
                titulo_publi=request.form['titulo_publi'],
                texto_publi=request.form['texto_publi']
            )
            if id_publi:
                print(f"✅ Nova publicação criada com ID: {id_publi}")
                return jsonify({'success': True, 'message': 'Publicação criada com sucesso!'})
            else:
                return jsonify({'success': False, 'error': 'Erro ao criar publicação'})
        except Exception as e:
            print(f"❌ Erro ao criar publicação: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    try:
        usuarios = cad_db.buscar_usuarios()
        escolas = cad_db.buscar_escolas()
        return render_template('variavel/publicacoes/nova_publicacao.html', 
                             usuarios=usuarios, 
                             escolas=escolas)
    except Exception as e:
        print(f"❌ Erro ao carregar formulário de publicação: {e}")
        return "Erro ao carregar formulário", 500

@app.route('/publicacao/<int:id>')
def detalhes_publicacao(id):
    """Detalhes de uma publicação específica"""
    try:
        publicacao = cad_db.buscar_publicacao_por_id(id)
        if not publicacao:
            return "Publicação não encontrada", 404
            
        comentarios = cad_db.buscar_comentarios_por_publicacao(id)
        
        return render_template('variavel/publicacoes/detalhes_publicacao.html', 
                             publicacao=publicacao, 
                             comentarios=comentarios)
    except Exception as e:
        print(f"❌ Erro ao carregar publicação: {e}")
        return "Publicação não encontrada", 404

@app.route('/comentario/novo', methods=['POST'])
def novo_comentario():
    """Cria um novo comentário"""
    try:
        id_coment = cad_db.criar_comentario(
            id_publi=request.form['id_publi'],
            id_user=request.form['id_user'],
            texto_coment=request.form['texto_coment']
        )
        if id_coment:
            print(f"✅ Novo comentário criado com ID: {id_coment}")
            return jsonify({'success': True, 'message': 'Comentário criado com sucesso!'})
        else:
            return jsonify({'success': False, 'error': 'Erro ao criar comentário'})
    except Exception as e:
        print(f"❌ Erro ao criar comentário: {e}")
        return jsonify({'success': False, 'error': str(e)})

# ========== API REST ENDPOINTS ==========

@app.route('/api/escolas')
def api_escolas():
    """API para listar escolas"""
    try:
        escolas = cad_db.buscar_escolas()
        return jsonify(escolas)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/usuarios')
def api_usuarios():
    """API para listar usuários"""
    try:
        usuarios = cad_db.buscar_usuarios()
        return jsonify(usuarios)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/publicacoes')
def api_publicacoes():
    """API para listar publicações"""
    try:
        publicacoes = cad_db.buscar_publicacoes()
        return jsonify(publicacoes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/estatisticas-bullying')
def api_estatisticas_bullying():
    """API para estatísticas do sistema de bullying"""
    try:
        stats = form_db.buscar_estatisticas()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/comentarios/<int:id_publicacao>')
def api_comentarios(id_publicacao):
    """API para listar comentários de uma publicação"""
    try:
        comentarios = cad_db.buscar_comentarios_por_publicacao(id_publicacao)
        return jsonify(comentarios)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/escola/<int:id>/publicacoes')
def api_publicacoes_escola(id):
    """API para listar publicações de uma escola específica"""
    try:
        publicacoes = cad_db.buscar_publicacoes_por_escola(id)
        return jsonify(publicacoes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)