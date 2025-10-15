# populate_user_responses.py
import sqlite3
import random
from datetime import datetime, timedelta

def populate_user_responses():
    """Popula a tabela UserRespostas com 20 registros de exemplo"""
    
    # Conectar ao banco de dados
    conn = sqlite3.connect('form.db')
    cursor = conn.cursor()
    
    # Perfis possíveis e suas faixas de pontuação
    perfis = {
        'Alheio à Problemática': (10, 16),
        'Consciente mas Cauteloso': (17, 23),
        'Atuante na Causa': (24, 30)
    }
    
    # Distribuição desejada dos perfis (aproximadamente)
    distribuicao = {
        'Alheio à Problemática': 6,      # ~30%
        'Consciente mas Cauteloso': 8,   # ~40%
        'Atuante na Causa': 6            # ~30%
    }
    
    # Lista para armazenar os registros
    registros = []
    
    # Gerar registros para cada perfil
    for perfil, quantidade in distribuicao.items():
        min_pontos, max_pontos = perfis[perfil]
        
        for i in range(quantidade):
            # Gerar pontuação aleatória dentro da faixa do perfil
            pontuacao = random.randint(min_pontos, max_pontos)
            
            # Gerar data aleatória nos últimos 30 dias
            dias_atras = random.randint(0, 30)
            data = datetime.now() - timedelta(days=dias_atras)
            data_str = data.strftime('%Y-%m-%d %H:%M:%S')
            
            registros.append((data_str, pontuacao, perfil))
    
    # Inserir registros no banco
    try:
        cursor.executemany(
            "INSERT INTO UserRespostas (data_resp, somaTotal_resp, perfil_resp) VALUES (?, ?, ?)",
            registros
        )
        
        conn.commit()
        print("✅ 20 registros inseridos na tabela UserRespostas com sucesso!")
        print("\n📊 Distribuição dos perfis:")
        for perfil, quantidade in distribuicao.items():
            print(f"   {perfil}: {quantidade} registros")
        
        # Verificar estatísticas
        cursor.execute("SELECT perfil_resp, COUNT(*) FROM UserRespostas GROUP BY perfil_resp")
        resultado = cursor.fetchall()
        print(f"\n📈 Total no banco após inserção:")
        for perfil, total in resultado:
            print(f"   {perfil}: {total} registros")
            
    except Exception as e:
        print(f"❌ Erro ao inserir registros: {e}")
        conn.rollback()
    finally:
        conn.close()

def verificar_estatisticas():
    """Verifica as estatísticas atuais da tabela UserRespostas"""
    conn = sqlite3.connect('form.db')
    cursor = conn.cursor()
    
    try:
        # Contagem total
        cursor.execute("SELECT COUNT(*) FROM UserRespostas")
        total = cursor.fetchone()[0]
        print(f"\n📊 ESTATÍSTICAS ATUAIS:")
        print(f"Total de registros: {total}")
        
        # Contagem por perfil
        cursor.execute("SELECT perfil_resp, COUNT(*) FROM UserRespostas GROUP BY perfil_resp ORDER BY COUNT(*) DESC")
        perfis = cursor.fetchall()
        print("\nDistribuição por perfil:")
        for perfil, count in perfis:
            percentual = (count / total) * 100
            print(f"  {perfil}: {count} ({percentual:.1f}%)")
        
        # Estatísticas de pontuação
        cursor.execute("SELECT MIN(somaTotal_resp), MAX(somaTotal_resp), AVG(somaTotal_resp) FROM UserRespostas")
        min_pontos, max_pontos, avg_pontos = cursor.fetchone()
        print(f"\nPontuações:")
        print(f"  Mínima: {min_pontos}")
        print(f"  Máxima: {max_pontos}")
        print(f"  Média: {avg_pontos:.1f}")
        
        # Últimos registros
        cursor.execute("SELECT data_resp, somaTotal_resp, perfil_resp FROM UserRespostas ORDER BY data_resp DESC LIMIT 5")
        ultimos = cursor.fetchall()
        print(f"\nÚltimos 5 registros:")
        for data, pontos, perfil in ultimos:
            print(f"  {data} - {pontos} pontos - {perfil}")
            
    except Exception as e:
        print(f"❌ Erro ao verificar estatísticas: {e}")
    finally:
        conn.close()

# Alternativa: Adicione esta função ao formDB.py existente
def popular_com_dados_exemplo(self):
    """Método para adicionar ao formDB.py para popular com dados de exemplo"""
    try:
        cursor = self.connection.cursor()
        
        # Verificar se já existem registros
        cursor.execute("SELECT COUNT(*) FROM UserRespostas")
        count = cursor.fetchone()[0]
        
        if count >= 20:
            print(f"✅ Já existem {count} registros na tabela UserRespostas")
            return
        
        # Dados de exemplo - 20 registros variados
        dados_exemplo = [
            # Alheio à Problemática (10-16 pontos)
            ('2024-01-15 10:30:00', 12, 'Alheio à Problemática'),
            ('2024-01-16 14:20:00', 14, 'Alheio à Problemática'),
            ('2024-01-17 09:15:00', 11, 'Alheio à Problemática'),
            ('2024-01-18 16:45:00', 15, 'Alheio à Problemática'),
            ('2024-01-19 11:30:00', 13, 'Alheio à Problemática'),
            ('2024-01-20 13:20:00', 16, 'Alheio à Problemática'),
            
            # Consciente mas Cauteloso (17-23 pontos)
            ('2024-01-15 08:45:00', 18, 'Consciente mas Cauteloso'),
            ('2024-01-16 12:30:00', 20, 'Consciente mas Cauteloso'),
            ('2024-01-17 15:20:00', 19, 'Consciente mas Cauteloso'),
            ('2024-01-18 10:15:00', 22, 'Consciente mas Cauteloso'),
            ('2024-01-19 14:40:00', 17, 'Consciente mas Cauteloso'),
            ('2024-01-20 09:50:00', 21, 'Consciente mas Cauteloso'),
            ('2024-01-21 11:25:00', 23, 'Consciente mas Cauteloso'),
            ('2024-01-22 16:10:00', 18, 'Consciente mas Cauteloso'),
            
            # Atuante na Causa (24-30 pontos)
            ('2024-01-16 13:45:00', 25, 'Atuante na Causa'),
            ('2024-01-17 10:30:00', 28, 'Atuante na Causa'),
            ('2024-01-18 15:20:00', 26, 'Atuante na Causa'),
            ('2024-01-19 12:15:00', 24, 'Atuante na Causa'),
            ('2024-01-20 14:50:00', 29, 'Atuante na Causa'),
            ('2024-01-21 09:40:00', 27, 'Atuante na Causa'),
        ]
        
        cursor.executemany(
            "INSERT INTO UserRespostas (data_resp, somaTotal_resp, perfil_resp) VALUES (?, ?, ?)",
            dados_exemplo
        )
        
        self.connection.commit()
        print(f"✅ {len(dados_exemplo)} registros de exemplo inseridos na tabela UserRespostas!")
        
        # Mostrar distribuição
        cursor.execute("SELECT perfil_resp, COUNT(*) FROM UserRespostas GROUP BY perfil_resp")
        resultado = cursor.fetchall()
        print("\n📊 Distribuição final:")
        for perfil, total in resultado:
            print(f"   {perfil}: {total} registros")
            
    except Exception as e:
        print(f"❌ Erro ao popular com dados exemplo: {e}")

if __name__ == "__main__":
    print("🧪 POPULANDO TABELA USERRESPOSTAS COM 20 REGISTROS")
    print("=" * 60)
    
    # Verificar estatísticas antes
    print("\n📋 ESTATÍSTICAS ANTES:")
    verificar_estatisticas()
    
    # Popular a tabela
    populate_user_responses()
    
    # Verificar estatísticas depois
    print("\n📋 ESTATÍSTICAS DEPOIS:")
    verificar_estatisticas()
    
    print("\n✅ Processo concluído!")