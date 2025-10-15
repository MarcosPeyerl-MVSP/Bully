# perfilGrafico.py
import matplotlib
matplotlib.use('Agg')  # Usar backend não-interativo
import matplotlib.pyplot as plt
import io
import base64
from formDB import get_db

class GraficoPerfil:
    def __init__(self):
        self.db = get_db()
    
    def gerar_grafico_perfis(self):
        """Gera um gráfico de barras com a distribuição dos perfis"""
        try:
            # Buscar estatísticas do banco
            stats = self.db.buscar_estatisticas()
            perfis = stats.get('perfis', [])
            
            if not perfis:
                # Retorna uma imagem placeholder se não houver dados
                return self._gerar_placeholder()
            
            # Preparar dados para o gráfico
            nomes_perfis = []
            quantidades = []
            cores = []
            
            # Definir cores para cada perfil
            cores_perfis = {
                'Alheio à Problemática': '#FF6B6B',
                'Consciente mas Cauteloso': '#4ECDC4', 
                'Atuante na Causa': '#45B7D1',
                'Fora da faixa': '#96CEB4'
            }
            
            for perfil_data in perfis:
                perfil = perfil_data['perfil_resp']
                quantidade = perfil_data['total']
                
                nomes_perfis.append(perfil)
                quantidades.append(quantidade)
                cores.append(cores_perfis.get(perfil, '#999999'))
            
            # Criar o gráfico
            plt.figure(figsize=(12, 8))
            bars = plt.bar(nomes_perfis, quantidades, color=cores, alpha=0.8, edgecolor='white', linewidth=2)
            
            # Personalizar o gráfico
            plt.title('Distribuição de Perfis - Questionário Anti-Bullying', 
                     fontsize=16, fontweight='bold', pad=20, color='#2d3748')
            plt.xlabel('Perfis', fontsize=12, fontweight='bold', color='#2d3748')
            plt.ylabel('Quantidade de Pessoas', fontsize=12, fontweight='bold', color='#2d3748')
            
            # Adicionar valores nas barras
            for bar, quantidade in zip(bars, quantidades):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                        f'{quantidade}', ha='center', va='bottom', fontweight='bold', fontsize=11)
            
            # Estilizar o gráfico
            plt.grid(axis='y', alpha=0.3, linestyle='--')
            plt.gca().set_facecolor('#f8f9fa')
            plt.gcf().patch.set_facecolor('white')
            
            # Remover bordas
            for spine in plt.gca().spines.values():
                spine.set_visible(False)
            
            # Rotacionar labels do eixo X se necessário
            plt.xticks(rotation=15, ha='right')
            plt.tight_layout()
            
            # Converter para base64
            img = io.BytesIO()
            plt.savefig(img, format='png', dpi=100, bbox_inches='tight')
            img.seek(0)
            graph_url = base64.b64encode(img.getvalue()).decode()
            plt.close()
            
            return f"data:image/png;base64,{graph_url}"
            
        except Exception as e:
            print(f"❌ Erro ao gerar gráfico: {e}")
            return self._gerar_placeholder()
    
    def _gerar_placeholder(self):
        """Gera um gráfico placeholder quando não há dados"""
        try:
            plt.figure(figsize=(10, 6))
            plt.text(0.5, 0.5, 'Aguardando dados...\nRealize o questionário para ver as estatísticas', 
                    ha='center', va='center', transform=plt.gca().transAxes, 
                    fontsize=14, style='italic', color='gray')
            plt.gca().set_facecolor('#f8f9fa')
            plt.gcf().patch.set_facecolor('white')
            
            # Remover eixos
            plt.axis('off')
            
            img = io.BytesIO()
            plt.savefig(img, format='png', dpi=100, bbox_inches='tight')
            img.seek(0)
            graph_url = base64.b64encode(img.getvalue()).decode()
            plt.close()
            
            return f"data:image/png;base64,{graph_url}"
            
        except Exception as e:
            print(f"❌ Erro ao gerar placeholder: {e}")
            return None
    
    def gerar_grafico_pizza(self):
        """Gera um gráfico de pizza com a distribuição dos perfis"""
        try:
            stats = self.db.buscar_estatisticas()
            perfis = stats.get('perfis', [])
            
            if not perfis:
                return self._gerar_placeholder()
            
            # Preparar dados
            labels = []
            sizes = []
            colors = []
            
            cores_perfis = {
                'Alheio à Problemática': '#FF6B6B',
                'Consciente mas Cauteloso': '#4ECDC4',
                'Atuante na Causa': '#45B7D1',
                'Fora da faixa': '#96CEB4'
            }
            
            for perfil_data in perfis:
                perfil = perfil_data['perfil_resp']
                quantidade = perfil_data['total']
                
                labels.append(f"{perfil}\n({quantidade})")
                sizes.append(quantidade)
                colors.append(cores_perfis.get(perfil, '#999999'))
            
            # Criar gráfico de pizza
            plt.figure(figsize=(10, 8))
            wedges, texts, autotexts = plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                              startangle=90, textprops={'fontsize': 10})
            
            # Estilizar
            plt.title('Distribuição de Perfis - Questionário Anti-Bullying', 
                     fontsize=16, fontweight='bold', pad=20, color='#2d3748')
            
            # Melhorar aparência dos textos
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(9)
            
            for text in texts:
                text.set_fontsize(10)
            
            plt.axis('equal')
            plt.tight_layout()
            
            # Converter para base64
            img = io.BytesIO()
            plt.savefig(img, format='png', dpi=100, bbox_inches='tight')
            img.seek(0)
            graph_url = base64.b64encode(img.getvalue()).decode()
            plt.close()
            
            return f"data:image/png;base64,{graph_url}"
            
        except Exception as e:
            print(f"❌ Erro ao gerar gráfico de pizza: {e}")
            return self._gerar_placeholder()

# Instância global
grafico_manager = GraficoPerfil()