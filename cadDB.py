from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Escola(db.Model):
    __tablename__ = 'escola'
    
    id_escola = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_escola = db.Column(db.String(150), nullable=False)
    categoria_escola = db.Column(db.Enum('publica', 'privada'), nullable=False)
    uf_escola = db.Column(db.String(2), nullable=False)
    bairro_escola = db.Column(db.String(100), nullable=False)
    
    usuarios = db.relationship('Usuario', backref='escola', lazy=True)
    publicacoes = db.relationship('Publicacao', backref='escola', lazy=True)

class Usuario(db.Model):
    __tablename__ = 'usuario'
    
    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_escola = db.Column(db.Integer, db.ForeignKey('escola.id_escola'), nullable=False)
    nome_user = db.Column(db.String(100), nullable=False)
    username_user = db.Column(db.String(20), unique=True, nullable=False)
    email_user = db.Column(db.String(100), unique=True, nullable=False)
    criado_user = db.Column(db.DateTime, default=datetime.utcnow)
    
    publicacoes = db.relationship('Publicacao', backref='usuario', lazy=True)
    comentarios = db.relationship('Comentario', backref='usuario', lazy=True)

class Publicacao(db.Model):
    __tablename__ = 'publicacao'
    
    id_publi = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey('usuario.id_user'), nullable=False)
    id_escola = db.Column(db.Integer, db.ForeignKey('escola.id_escola'), nullable=False)
    titulo_publi = db.Column(db.String(200), nullable=False)
    texto_publi = db.Column(db.Text, nullable=False)
    data_publi = db.Column(db.DateTime, default=datetime.utcnow)
    resolvido_publi = db.Column(db.Boolean, default=False)
    
    comentarios = db.relationship('Comentario', backref='publicacao', lazy=True)

class Comentario(db.Model):
    __tablename__ = 'comentario'
    
    id_coment = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_publi = db.Column(db.Integer, db.ForeignKey('publicacao.id_publi'), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('usuario.id_user'), nullable=False)
    texto_coment = db.Column(db.Text, nullable=False)
    data_coment = db.Column(db.DateTime, default=datetime.utcnow)

def init_db(app):
    """Inicializa o banco de dados com o app Flask"""
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        popular_escolas()

def popular_escolas():
    """Popula a tabela de escolas com dados iniciais"""
    if Escola.query.count() == 0:
        escolas_sp = [
            ('Escola Estadual Professor Doutor José Augusto Lopes Borges', 'publica', 'SP', 'Butantã'),
            ('Colégio Bandeirantes', 'privada', 'SP', 'Morumbi'),
            ('Escola Estadual Professor Carlos Alberto de Oliveira', 'publica', 'SP', 'Ipiranga'),
            ('Colégio Dante Alighieri', 'privada', 'SP', 'Cerqueira César'),
            ('Escola Municipal Professor Lourenço Filho', 'publica', 'SP', 'Tatuapé'),
            ('Colégio Santa Cruz', 'privada', 'SP', 'Alto de Pinheiros'),
            ('Escola Estadual Professor Antônio Maria Moura', 'publica', 'SP', 'Vila Mariana'),
            ('Colégio Vértice', 'privada', 'SP', 'Campo Belo'),
            ('Escola Municipal Professor Anísio Teixeira', 'publica', 'SP', 'Jardim Ângela'),
            ('Colégio Magno', 'privada', 'SP', 'Jardim Marajoara'),
            ('Fundação Escola de Comércio Álvares Penteado', 'privada', 'SP', 'Liberdade')
        ]
        
        escolas_rj = [
            ('Colégio Santo Inácio', 'privada', 'RJ', 'Botafogo'),
            ('Escola Municipal Francis Hime', 'publica', 'RJ', 'Jacarepaguá'),
            ('Colégio pH', 'privada', 'RJ', 'Leblon'),
            ('Escola Estadual Orsina da Fonseca', 'publica', 'RJ', 'Tijuca'),
            ('Colégio Cruzeiro', 'privada', 'RJ', 'Centro'),
            ('Escola Municipal Pernambuco', 'publica', 'RJ', 'Higienópolis'),
            ('Colégio São Bento', 'privada', 'RJ', 'Centro'),
            ('Escola Estadual Professor Augusto Ruschi', 'publica', 'RJ', 'Tijuca'),
            ('Colégio Mopi', 'privada', 'RJ', 'Tijuca'),
            ('Escola Municipal Chile', 'publica', 'RJ', 'Copacabana')
        ]
        
        for escola in escolas_sp + escolas_rj:
            nova_escola = Escola(
                nome_escola=escola[0],
                categoria_escola=escola[1],
                uf_escola=escola[2],
                bairro_escola=escola[3]
            )
            db.session.add(nova_escola)
        
        db.session.commit()
        print("Tabela de escolas populada com dados iniciais!")