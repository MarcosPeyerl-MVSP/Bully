import sqlite3
import os

class Database:
    def __init__(self, db_name='bullying.db'):
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
            print("✅ Conectado ao SQLite com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao conectar ao SQLite: {e}")
    
    def create_tables(self):
        """Cria todas as tabelas necessárias"""
        try:
            cursor = self.connection.cursor()
            
            # Tabela Perguntas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Perguntas (
                    id_perg INTEGER PRIMARY KEY AUTOINCREMENT,
                    texto_perg TEXT NOT NULL,
                    ordem_perg INTEGER NOT NULL
                )
            ''')
            
            # Tabela UserRespostas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS UserRespostas (
                    id_resp INTEGER PRIMARY KEY AUTOINCREMENT,
                    data_resp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    somaTotal_resp INTEGER NOT NULL,
                    perfil_resp TEXT NOT NULL
                )
            ''')
            
            # Tabela Resposta
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Resposta (
                    id_opcao INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_pergunta INTEGER,
                    texto_opcao TEXT NOT NULL,
                    pontuacao INTEGER NOT NULL,
                    FOREIGN KEY (id_pergunta) REFERENCES Perguntas(id_perg)
                )
            ''')
            
            self.connection.commit()
            print("✅ Tabelas criadas/verificadas com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao criar tabelas: {e}")
    
    def insert_initial_data(self):
        """Insere perguntas e respostas iniciais"""
        try:
            cursor = self.connection.cursor()
            
            # Verificar se já existem perguntas para não duplicar
            cursor.execute("SELECT COUNT(*) FROM Perguntas")
            count = cursor.fetchone()[0]
            print(f"📊 Perguntas no banco: {count}")
            
            if count == 0:
                print("📥 Inserindo dados iniciais...")
                
                # Inserir perguntas
                perguntas = [
                    ('Você já sofreu bullying?', 1),
                    ('Você já presenciou alguém sofrendo bullying?', 2),
                    ('Como você reage ao ver uma situação de bullying?', 3),
                    ('Você já praticou bullying?', 4),
                    ('Na sua escola/trabalho, há ações contra bullying?', 5),
                    ('Você acha que o bullying pode causar traumas duradouros?', 6),
                    ('Se alguém próximo fizesse bullying, você interviria?', 7),
                    ('Você já foi excluído de grupos ou atividades?', 8),
                    ('Como você descreve o ambiente onde vive/trabalha/estuda?', 9),
                    ('Você busca aprender sobre empatia e respeito?', 10)
                ]
                
                cursor.executemany(
                    "INSERT INTO Perguntas (texto_perg, ordem_perg) VALUES (?, ?)",
                    perguntas
                )
                
                # Inserir opções de resposta
                opcoes_resposta = [
                    # Pergunta 1
                    (1, 'Nunca', 1),
                    (1, 'Ocasionalmente, mas não me afetou profundamente', 2),
                    (1, 'Sim, e isso impactou minha autoestima ou saúde mental', 3),
                    
                    # Pergunta 2
                    (2, 'Nunca', 1),
                    (2, 'Sim, e tentei intervir ou ajudar', 3),
                    (2, 'Sim, mas não soube como agir', 2),
                    
                    # Pergunta 3
                    (3, 'Ignoro ou evito me envolver', 1),
                    (3, 'Busco ajuda de um adulto ou autoridade', 3),
                    (3, 'Defendo a vítima diretamente', 2),
                    
                    # Pergunta 4
                    (4, 'Nunca', 3),
                    (4, 'Já participei indiretamente (como risadas)', 2),
                    (4, 'Sim, mas me arrependo hoje', 1),
                    
                    # Pergunta 5
                    (5, 'Sim, e são eficazes', 3),
                    (5, 'Existem, mas não são divulgadas', 2),
                    (5, 'Não há iniciativas', 1),
                    
                    # Pergunta 6
                    (6, 'Sim, e é um problema grave', 3),
                    (6, 'Depende da situação', 2),
                    (6, 'Não, é algo passageiro', 1),
                    
                    # Pergunta 7
                    (7, 'Sim, diretamente', 3),
                    (7, 'Conversaria em privado', 2),
                    (7, 'Não me envolveria', 1),
                    
                    # Pergunta 8
                    (8, 'Nunca', 1),
                    (8, 'Ocasionalmente', 2),
                    (8, 'Frequentemente', 3),
                    
                    # Pergunta 9
                    (9, 'Respeitoso e inclusivo', 3),
                    (9, 'Há conflitos, mas são raros', 2),
                    (9, 'Hostil e competitivo', 1),
                    
                    # Pergunta 10
                    (10, 'Sim, constantemente', 3),
                    (10, 'Às vezes, quando necessário', 2),
                    (10, 'Não vejo necessidade', 1)
                ]
                
                cursor.executemany(
                    "INSERT INTO Resposta (id_pergunta, texto_opcao, pontuacao) VALUES (?, ?, ?)",
                    opcoes_resposta
                )
                
                self.connection.commit()
                print("✅ Dados iniciais inseridos com sucesso!")
            else:
                print("✅ Dados já existem no banco.")
            
        except Exception as e:
            print(f"❌ Erro ao inserir dados iniciais: {e}")
    
    def buscar_perguntas(self):
        """Busca todas as perguntas com suas opções"""
        try:
            cursor = self.connection.cursor()
            
            # Buscar perguntas ordenadas
            cursor.execute("SELECT * FROM Perguntas ORDER BY ordem_perg")
            perguntas = []
            for row in cursor.fetchall():
                pergunta = dict(row)
                perguntas.append(pergunta)
            
            print(f"📋 Encontradas {len(perguntas)} perguntas")
            
            # Para cada pergunta, buscar suas opções
            for pergunta in perguntas:
                cursor.execute(
                    "SELECT * FROM Resposta WHERE id_pergunta = ? ORDER BY id_opcao",
                    (pergunta['id_perg'],)
                )
                opcoes = []
                for row in cursor.fetchall():
                    opcoes.append(dict(row))
                pergunta['opcoes'] = opcoes
                print(f"  📝 Pergunta {pergunta['id_perg']}: {len(opcoes)} opções")
            
            return perguntas
        except Exception as e:
            print(f"❌ Erro ao buscar perguntas: {e}")
            return []
    
    def salvar_resposta_usuario(self, soma_total, perfil):
        """Salva o resultado do questionário do usuário"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO UserRespostas (somaTotal_resp, perfil_resp) VALUES (?, ?)",
                (soma_total, perfil)
            )
            self.connection.commit()
            print(f"💾 Resposta salva: {soma_total} pontos - {perfil}")
            return True
        except Exception as e:
            print(f"❌ Erro ao salvar resposta do usuário: {e}")
            return False
    
    def buscar_estatisticas(self):
        """Busca estatísticas das respostas dos usuários"""
        try:
            cursor = self.connection.cursor()
            
            # Contagem por perfil
            cursor.execute('''
                SELECT perfil_resp, COUNT(*) as total 
                FROM UserRespostas 
                GROUP BY perfil_resp
            ''')
            estatisticas = [dict(row) for row in cursor.fetchall()]
            
            # Total de respostas
            cursor.execute("SELECT COUNT(*) as total FROM UserRespostas")
            total_geral = cursor.fetchone()[0]
            
            return {
                'perfis': estatisticas,
                'total_geral': total_geral
            }
        except Exception as e:
            print(f"❌ Erro ao buscar estatísticas: {e}")
            return {'perfis': [], 'total_geral': 0}
    
    def close(self):
        """Fecha a conexão com o banco"""
        if self.connection:
            self.connection.close()
            print("✅ Conexão com SQLite fechada.")

# Instância global do banco de dados
database = Database()

def get_db():
    return database