# formDB.py
import sqlite3
import os

class Database:
    def __init__(self, db_name='form.db'):
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
                ORDER BY total DESC
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
    
    def buscar_todas_respostas(self):
        """Busca todas as respostas dos usuários para análise detalhada"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT id_resp, data_resp, somaTotal_resp, perfil_resp 
                FROM UserRespostas 
                ORDER BY data_resp DESC
            ''')
            respostas = [dict(row) for row in cursor.fetchall()]
            return respostas
        except Exception as e:
            print(f"❌ Erro ao buscar todas as respostas: {e}")
            return []
    
    def buscar_distribuicao_pontuacao(self):
        """Busca a distribuição das pontuações totais"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT 
                    somaTotal_resp,
                    COUNT(*) as quantidade,
                    perfil_resp
                FROM UserRespostas 
                GROUP BY somaTotal_resp, perfil_resp
                ORDER BY somaTotal_resp
            ''')
            distribuicao = [dict(row) for row in cursor.fetchall()]
            return distribuicao
        except Exception as e:
            print(f"❌ Erro ao buscar distribuição de pontuação: {e}")
            return []
    
    def buscar_estatisticas_detalhadas(self):
        """Busca estatísticas detalhadas incluindo médias e ranges"""
        try:
            cursor = self.connection.cursor()
            
            # Estatísticas básicas
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_respostas,
                    AVG(somaTotal_resp) as media_pontuacao,
                    MIN(somaTotal_resp) as minima_pontuacao,
                    MAX(somaTotal_resp) as maxima_pontuacao
                FROM UserRespostas
            ''')
            stats_gerais = dict(cursor.fetchone())
            
            # Estatísticas por perfil
            cursor.execute('''
                SELECT 
                    perfil_resp,
                    COUNT(*) as total,
                    AVG(somaTotal_resp) as media_pontuacao,
                    MIN(somaTotal_resp) as minima_pontuacao,
                    MAX(somaTotal_resp) as maxima_pontuacao
                FROM UserRespostas 
                GROUP BY perfil_resp
                ORDER BY total DESC
            ''')
            stats_perfis = [dict(row) for row in cursor.fetchall()]
            
            # Distribuição temporal (últimos 30 dias)
            cursor.execute('''
                SELECT 
                    DATE(data_resp) as data,
                    COUNT(*) as respostas_dia
                FROM UserRespostas 
                WHERE data_resp >= date('now', '-30 days')
                GROUP BY DATE(data_resp)
                ORDER BY data DESC
            ''')
            timeline = [dict(row) for row in cursor.fetchall()]
            
            return {
                'geral': stats_gerais,
                'perfis': stats_perfis,
                'timeline': timeline
            }
            
        except Exception as e:
            print(f"❌ Erro ao buscar estatísticas detalhadas: {e}")
            return {
                'geral': {},
                'perfis': [],
                'timeline': []
            }
    
    def limpar_respostas(self):
        """Limpa todas as respostas dos usuários (para testes)"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM UserRespostas")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='UserRespostas'")
            self.connection.commit()
            print("🗑️ Todas as respostas foram limpas")
            return True
        except Exception as e:
            print(f"❌ Erro ao limpar respostas: {e}")
            return False
    
    def exportar_dados(self, formato='json'):
        """Exporta os dados para análise externa"""
        try:
            dados = {}
            
            # Perguntas e opções
            dados['perguntas'] = self.buscar_perguntas()
            
            # Respostas dos usuários
            dados['respostas_usuarios'] = self.buscar_todas_respostas()
            
            # Estatísticas
            dados['estatisticas'] = self.buscar_estatisticas_detalhadas()
            
            if formato == 'json':
                import json
                return json.dumps(dados, indent=2, ensure_ascii=False, default=str)
            else:
                return dados
                
        except Exception as e:
            print(f"❌ Erro ao exportar dados: {e}")
            return None
    
    def buscar_resumo_perfis(self):
        """Busca um resumo simplificado dos perfis para gráficos rápidos"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute('''
                SELECT 
                    perfil_resp as perfil,
                    COUNT(*) as quantidade,
                    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM UserRespostas), 2) as percentual
                FROM UserRespostas 
                GROUP BY perfil_resp
                ORDER BY quantidade DESC
            ''')
            
            resumo = [dict(row) for row in cursor.fetchall()]
            return resumo
            
        except Exception as e:
            print(f"❌ Erro ao buscar resumo de perfis: {e}")
            return []
    
    def buscar_evolucao_temporal(self):
        """Busca a evolução temporal das respostas"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute('''
                SELECT 
                    DATE(data_resp) as data,
                    COUNT(*) as total_respostas,
                    AVG(somaTotal_resp) as media_pontuacao,
                    GROUP_CONCAT(perfil_resp) as perfis
                FROM UserRespostas 
                GROUP BY DATE(data_resp)
                ORDER BY data DESC
                LIMIT 30
            ''')
            
            evolucao = []
            for row in cursor.fetchall():
                data_row = dict(row)
                # Processar perfis para contar ocorrências
                if data_row['perfis']:
                    perfis_list = data_row['perfis'].split(',')
                    contagem_perfis = {}
                    for perfil in perfis_list:
                        contagem_perfis[perfil] = contagem_perfis.get(perfil, 0) + 1
                    data_row['distribuicao_perfis'] = contagem_perfis
                
                evolucao.append(data_row)
            
            return evolucao
            
        except Exception as e:
            print(f"❌ Erro ao buscar evolução temporal: {e}")
            return []
    
    def close(self):
        """Fecha a conexão com o banco"""
        if self.connection:
            self.connection.close()
            print("✅ Conexão com SQLite fechada.")

# Instância global do banco de dados
database = Database()

def get_db():
    """Retorna a instância do banco de dados"""
    return database

# Teste básico se executado diretamente
if __name__ == "__main__":
    db = Database()
    
    print("\n" + "="*50)
    print("TESTE DO BANCO DE DADOS FORMDB")
    print("="*50)
    
    # Testar busca de perguntas
    perguntas = db.buscar_perguntas()
    print(f"\n📋 Total de perguntas: {len(perguntas)}")
    
    for pergunta in perguntas:
        print(f"  Pergunta {pergunta['id_perg']}: {pergunta['texto_perg']}")
        for opcao in pergunta['opcoes']:
            print(f"    - {opcao['texto_opcao']} ({opcao['pontuacao']} pontos)")
    
    # Testar estatísticas
    stats = db.buscar_estatisticas()
    print(f"\n📊 Estatísticas:")
    print(f"  Total de respostas: {stats['total_geral']}")
    for perfil in stats['perfis']:
        print(f"  {perfil['perfil_resp']}: {perfil['total']}")
    
    # Testar resumo de perfis
    resumo = db.buscar_resumo_perfis()
    print(f"\n📈 Resumo de perfis:")
    for item in resumo:
        print(f"  {item['perfil']}: {item['quantidade']} ({item['percentual']}%)")
    
    print("\n✅ Teste do banco de dados concluído com sucesso!")