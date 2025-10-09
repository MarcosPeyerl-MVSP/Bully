# app.py
from flask import Flask, render_template, request, jsonify
from formDB import get_db as get_form_db
from cadDB import db, init_db, Escola, Usuario, Publicacao, Comentario

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sistema_escolas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'

# Inicializa ambos os bancos de dados
form_db = get_form_db()
init_db(app)

@app.route('/')
def index():
    """Página inicial"""
    try:
        # Estatísticas do sistema de escolas
        total_escolas = Escola.query.count()
        total_usuarios = Usuario.query.count()
        total_publicacoes = Publicacao.query.count()
        
        # Estatísticas do sistema de bullying
        stats_bullying = form_db.buscar_estatisticas()
        
        # Últimas publicações
        ultimas_publicacoes = Publicacao.query.order_by(Publicacao.data_publi.desc()).limit(5).all()
        
        return render_template('estatico/index.html', 
                             total_escolas=total_escolas,
                             total_usuarios=total_usuarios,
                             total_publicacoes=total_publicacoes,
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

@app.route('/estatisticas')
def estatisticas():
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
        escolas = Escola.query.all()
        return render_template('variavel/escolas/escolas.html', escolas=escolas)
    except Exception as e:
        print(f"❌ Erro ao carregar escolas: {e}")
        return "Erro ao carregar escolas", 500

@app.route('/escola/<int:id>')
def detalhes_escola(id):
    """Detalhes de uma escola específica"""
    try:
        escola = Escola.query.get_or_404(id)
        publicacoes = Publicacao.query.filter_by(id_escola=id).order_by(Publicacao.data_publi.desc()).all()
        usuarios = Usuario.query.filter_by(id_escola=id).all()
        
        return render_template('variavel/escolas/detalhes_escola.html', 
                             escola=escola, 
                             publicacoes=publicacoes,
                             usuarios=usuarios)
    except Exception as e:
        print(f"❌ Erro ao carregar escola: {e}")
        return "Escola não encontrada", 404

@app.route('/usuarios')
def listar_usuarios():
    """Lista todos os usuários"""
    try:
        usuarios = Usuario.query.all()
        return render_template('variavel/usuarios/usuarios.html', usuarios=usuarios)
    except Exception as e:
        print(f"❌ Erro ao carregar usuários: {e}")
        return "Erro ao carregar usuários", 500

@app.route('/usuario/novo', methods=['GET', 'POST'])
def novo_usuario():
    """Cria um novo usuário"""
    if request.method == 'POST':
        try:
            usuario = Usuario(
                id_escola=request.form['id_escola'],
                nome_user=request.form['nome_user'],
                username_user=request.form['username_user'],
                email_user=request.form['email_user']
            )
            db.session.add(usuario)
            db.session.commit()
            print(f"✅ Novo usuário criado: {usuario.nome_user}")
            return jsonify({'success': True, 'message': 'Usuário criado com sucesso!'})
        except Exception as e:
            print(f"❌ Erro ao criar usuário: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    try:
        escolas = Escola.query.all()
        return render_template('variavel/usuarios/novo_usuario.html', escolas=escolas)
    except Exception as e:
        print(f"❌ Erro ao carregar formulário de usuário: {e}")
        return "Erro ao carregar formulário", 500

@app.route('/publicacoes')
def listar_publicacoes():
    """Lista todas as publicações"""
    try:
        publicacoes = Publicacao.query.order_by(Publicacao.data_publi.desc()).all()
        return render_template('variavel/publicacoes/publicacoes.html', publicacoes=publicacoes)
    except Exception as e:
        print(f"❌ Erro ao carregar publicações: {e}")
        return "Erro ao carregar publicações", 500

@app.route('/publicacao/nova', methods=['GET', 'POST'])
def nova_publicacao():
    """Cria uma nova publicação"""
    if request.method == 'POST':
        try:
            publicacao = Publicacao(
                id_user=request.form['id_user'],
                id_escola=request.form['id_escola'],
                titulo_publi=request.form['titulo_publi'],
                texto_publi=request.form['texto_publi']
            )
            db.session.add(publicacao)
            db.session.commit()
            print(f"✅ Nova publicação criada: {publicacao.titulo_publi}")
            return jsonify({'success': True, 'message': 'Publicação criada com sucesso!'})
        except Exception as e:
            print(f"❌ Erro ao criar publicação: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    try:
        usuarios = Usuario.query.all()
        escolas = Escola.query.all()
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
        publicacao = Publicacao.query.get_or_404(id)
        comentarios = Comentario.query.filter_by(id_publi=id).order_by(Comentario.data_coment.desc()).all()
        
        return render_template('variavel/publicacoes/detalhes_publicacao.html', 
                             publicacao=publicacao, 
                             comentarios=comentarios)
    except Exception as e:
        print(f"❌ Erro ao carregar publicação: {e}")
        return "Publicação não encontrada", 404

# ========== API REST ENDPOINTS ==========

@app.route('/api/escolas')
def api_escolas():
    """API para listar escolas"""
    try:
        escolas = Escola.query.all()
        return jsonify([{
            'id_escola': e.id_escola,
            'nome_escola': e.nome_escola,
            'categoria_escola': e.categoria_escola,
            'uf_escola': e.uf_escola,
            'bairro_escola': e.bairro_escola
        } for e in escolas])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/usuarios')
def api_usuarios():
    """API para listar usuários"""
    try:
        usuarios = Usuario.query.all()
        return jsonify([{
            'id_user': u.id_user,
            'nome_user': u.nome_user,
            'username_user': u.username_user,
            'email_user': u.email_user,
            'escola': u.escola.nome_escola if u.escola else 'N/A'
        } for u in usuarios])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/publicacoes')
def api_publicacoes():
    """API para listar publicações"""
    try:
        publicacoes = Publicacao.query.all()
        return jsonify([{
            'id_publi': p.id_publi,
            'titulo_publi': p.titulo_publi,
            'texto_publi': p.texto_publi,
            'data_publi': p.data_publi.isoformat(),
            'resolvido_publi': p.resolvido_publi,
            'usuario': p.usuario.nome_user,
            'escola': p.escola.nome_escola
        } for p in publicacoes])
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
        comentarios = Comentario.query.filter_by(id_publi=id_publicacao).all()
        return jsonify([{
            'id_coment': c.id_coment,
            'texto_coment': c.texto_coment,
            'data_coment': c.data_coment.isoformat(),
            'usuario': c.usuario.nome_user
        } for c in comentarios])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)