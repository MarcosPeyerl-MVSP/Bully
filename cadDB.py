import sqlite3
import os

class Database:
    def __init__(self, db_name='cad.db'):
        self.db_name = db_name
        self.connection = None
        self.connect()
        self.create_tables()
        self.insert_initial_data()
    
    def connect(self):
        """Conecta ao banco de dados SQLite"""
        try:
            self.connection = sqlite3.connect(self.db_name, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
            print("✅ Conectado ao SQLite (cadDB) com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao conectar ao SQLite (cadDB): {e}")
    
    def create_tables(self):
        """Cria todas as tabelas necessárias para o sistema de escolas"""
        try:
            cursor = self.connection.cursor()
            
            # Tabela Escola
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS escola (
                    id_escola INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_escola TEXT NOT NULL,
                    categoria_escola TEXT NOT NULL CHECK(categoria_escola IN ('publica', 'privada')),
                    uf_escola TEXT NOT NULL,
                    bairro_escola TEXT NOT NULL
                )
            ''')
            
            # Tabela Usuario
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuario (
                    id_user INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_escola INTEGER NOT NULL,
                    nome_user TEXT NOT NULL,
                    username_user TEXT UNIQUE NOT NULL,
                    email_user TEXT UNIQUE NOT NULL,
                    criado_user TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_escola) REFERENCES escola(id_escola)
                )
            ''')
            
            # Tabela Publicacao
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS publicacao (
                    id_publi INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_user INTEGER NOT NULL,
                    id_escola INTEGER NOT NULL,
                    titulo_publi TEXT NOT NULL,
                    texto_publi TEXT NOT NULL,
                    data_publi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    resolvido_publi BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (id_user) REFERENCES usuario(id_user),
                    FOREIGN KEY (id_escola) REFERENCES escola(id_escola)
                )
            ''')
            
            # Tabela Comentario
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS comentario (
                    id_coment INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_publi INTEGER NOT NULL,
                    id_user INTEGER NOT NULL,
                    texto_coment TEXT NOT NULL,
                    data_coment TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_publi) REFERENCES publicacao(id_publi) ON DELETE CASCADE,
                    FOREIGN KEY (id_user) REFERENCES usuario(id_user)
                )
            ''')
            
            # Criar índices para melhor performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_usuario_escola ON usuario(id_escola)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_publicacao_usuario ON publicacao(id_user)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_publicacao_escola ON publicacao(id_escola)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_comentario_publicacao ON comentario(id_publi)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_comentario_usuario ON comentario(id_user)')
            
            self.connection.commit()
            print("✅ Tabelas do sistema de escolas criadas/verificadas com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao criar tabelas do sistema de escolas: {e}")
    
    def insert_initial_data(self):
        """Insere escolas iniciais"""
        try:
            cursor = self.connection.cursor()
            
            # Verificar se já existem escolas para não duplicar
            cursor.execute("SELECT COUNT(*) FROM escola")
            count = cursor.fetchone()[0]
            print(f"📊 Escolas no banco: {count}")
            
            if count == 0:
                print("📥 Inserindo escolas iniciais...")
                
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
                
                cursor.executemany(
                    "INSERT INTO escola (nome_escola, categoria_escola, uf_escola, bairro_escola) VALUES (?, ?, ?, ?)",
                    escolas_sp + escolas_rj
                )
                
                self.connection.commit()
                print("✅ Escolas iniciais inseridas com sucesso!")
            else:
                print("✅ Escolas já existem no banco.")
            
        except Exception as e:
            print(f"❌ Erro ao inserir escolas iniciais: {e}")
    
    # ========== MÉTODOS PARA ESCOLAS ==========
    
    def buscar_escolas(self):
        """Busca todas as escolas"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM escola ORDER BY nome_escola")
            escolas = [dict(row) for row in cursor.fetchall()]
            return escolas
        except Exception as e:
            print(f"❌ Erro ao buscar escolas: {e}")
            return []
    
    def buscar_escola_por_id(self, id_escola):
        """Busca uma escola específica por ID"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM escola WHERE id_escola = ?", (id_escola,))
            escola = cursor.fetchone()
            return dict(escola) if escola else None
        except Exception as e:
            print(f"❌ Erro ao buscar escola: {e}")
            return None
    
    def criar_escola(self, nome_escola, categoria_escola, uf_escola, bairro_escola):
        """Cria uma nova escola"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO escola (nome_escola, categoria_escola, uf_escola, bairro_escola) VALUES (?, ?, ?, ?)",
                (nome_escola, categoria_escola, uf_escola, bairro_escola)
            )
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"❌ Erro ao criar escola: {e}")
            return None
    
    # ========== MÉTODOS PARA USUÁRIOS ==========
    
    def buscar_usuarios(self):
        """Busca todos os usuários"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT u.*, e.nome_escola 
                FROM usuario u 
                LEFT JOIN escola e ON u.id_escola = e.id_escola 
                ORDER BY u.nome_user
            ''')
            usuarios = [dict(row) for row in cursor.fetchall()]
            return usuarios
        except Exception as e:
            print(f"❌ Erro ao buscar usuários: {e}")
            return []
    
    def buscar_usuario_por_id(self, id_user):
        """Busca um usuário específico por ID"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT u.*, e.nome_escola 
                FROM usuario u 
                LEFT JOIN escola e ON u.id_escola = e.id_escola 
                WHERE u.id_user = ?
            ''', (id_user,))
            usuario = cursor.fetchone()
            return dict(usuario) if usuario else None
        except Exception as e:
            print(f"❌ Erro ao buscar usuário: {e}")
            return None
    
    def criar_usuario(self, id_escola, nome_user, username_user, email_user):
        """Cria um novo usuário"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO usuario (id_escola, nome_user, username_user, email_user) VALUES (?, ?, ?, ?)",
                (id_escola, nome_user, username_user, email_user)
            )
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"❌ Erro ao criar usuário: {e}")
            return None
    
    # ========== MÉTODOS PARA PUBLICAÇÕES ==========
    
    def buscar_publicacoes(self):
        """Busca todas as publicações"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT p.*, u.nome_user, e.nome_escola 
                FROM publicacao p 
                LEFT JOIN usuario u ON p.id_user = u.id_user 
                LEFT JOIN escola e ON p.id_escola = e.id_escola 
                ORDER BY p.data_publi DESC
            ''')
            publicacoes = [dict(row) for row in cursor.fetchall()]
            return publicacoes
        except Exception as e:
            print(f"❌ Erro ao buscar publicações: {e}")
            return []
    
    def buscar_publicacao_por_id(self, id_publi):
        """Busca uma publicação específica por ID"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT p.*, u.nome_user, e.nome_escola 
                FROM publicacao p 
                LEFT JOIN usuario u ON p.id_user = u.id_user 
                LEFT JOIN escola e ON p.id_escola = e.id_escola 
                WHERE p.id_publi = ?
            ''', (id_publi,))
            publicacao = cursor.fetchone()
            return dict(publicacao) if publicacao else None
        except Exception as e:
            print(f"❌ Erro ao buscar publicação: {e}")
            return None
    
    def criar_publicacao(self, id_user, id_escola, titulo_publi, texto_publi):
        """Cria uma nova publicação"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO publicacao (id_user, id_escola, titulo_publi, texto_publi) VALUES (?, ?, ?, ?)",
                (id_user, id_escola, titulo_publi, texto_publi)
            )
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"❌ Erro ao criar publicação: {e}")
            return None
    
    def buscar_publicacoes_por_escola(self, id_escola):
        """Busca publicações de uma escola específica"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT p.*, u.nome_user 
                FROM publicacao p 
                LEFT JOIN usuario u ON p.id_user = u.id_user 
                WHERE p.id_escola = ? 
                ORDER BY p.data_publi DESC
            ''', (id_escola,))
            publicacoes = [dict(row) for row in cursor.fetchall()]
            return publicacoes
        except Exception as e:
            print(f"❌ Erro ao buscar publicações da escola: {e}")
            return []
    
    # ========== MÉTODOS PARA COMENTÁRIOS ==========
    
    def buscar_comentarios_por_publicacao(self, id_publi):
        """Busca comentários de uma publicação específica"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT c.*, u.nome_user 
                FROM comentario c 
                LEFT JOIN usuario u ON c.id_user = u.id_user 
                WHERE c.id_publi = ? 
                ORDER BY c.data_coment ASC
            ''', (id_publi,))
            comentarios = [dict(row) for row in cursor.fetchall()]
            return comentarios
        except Exception as e:
            print(f"❌ Erro ao buscar comentários: {e}")
            return []
    
    def criar_comentario(self, id_publi, id_user, texto_coment):
        """Cria um novo comentário"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO comentario (id_publi, id_user, texto_coment) VALUES (?, ?, ?)",
                (id_publi, id_user, texto_coment)
            )
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"❌ Erro ao criar comentário: {e}")
            return None
    
    def close(self):
        """Fecha a conexão com o banco"""
        if self.connection:
            self.connection.close()
            print("✅ Conexão com SQLite (cadDB) fechada.")

# Instância global do banco de dados do sistema de escolas
database = Database()

def get_db():
    return database