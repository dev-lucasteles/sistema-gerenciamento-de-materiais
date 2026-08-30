import matplotlib
matplotlib.use('Agg') 
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
import os

def obter_area_de_trabalho():
    home = os.path.expanduser("~")
    caminhos = [
        os.path.join(home, "OneDrive", "Área de Trabalho"),
        os.path.join(home, "OneDrive", "Desktop"),
        os.path.join(home, "Desktop"),
        os.path.join(home, "Área de Trabalho")
    ]
    for caminho in caminhos:
        if os.path.exists(caminho):
            return caminho
    return os.path.join(home, "Desktop")

def criar_grafico(dados_grafico, monitor_responsavel, data_hora, caminho_txt):
    materiais = [d['material'] for d in dados_grafico][::-1]
    esperado = [d['esperado'] for d in dados_grafico][::-1]
    encontrado = [d['encontrado'] for d in dados_grafico][::-1]
    anotacoes_grafico = [d['anotacao'] for d in dados_grafico][::-1]

    altura_dinamica = max(10.0, len(materiais) * 0.6)
    fig = Figure(figsize=(16, altura_dinamica))
    
    # Fundo do gráfico em tom super claro, quase branco
    fig.patch.set_facecolor('#f8f9fa')
    
    canvas = FigureCanvasAgg(fig)
    ax = fig.add_subplot(111)
    ax.set_facecolor('#f8f9fa')
    
    y = np.arange(len(materiais))
    altura = 0.35

    # Cores pastéis e modernas
    cor_esperado = '#ced4da' 
    ax.barh(y + altura/2, esperado, altura, label='Esperado', color=cor_esperado, edgecolor='none')
    
    # Vermelho/Azul corporativos
    cores_encontrado = ['#e74c3c' if enc < esp else '#3498db' for enc, esp in zip(encontrado, esperado)]
    barras_enc = ax.barh(y - altura/2, encontrado, altura, label='Encontrado', color=cores_encontrado, edgecolor='none')

    # Ajustes de Fontes
    ax.set_xlabel('Quantidade de Itens', fontsize=14, fontweight='bold', color='#34495e', labelpad=15)
    
    if data_hora:
        titulo_grafico = f'Relatório de Check-list Diário\nConferido por: {monitor_responsavel}   |   {data_hora}'
    else:
        titulo_grafico = f'Relatório de Check-list Diário\nConferido por: {monitor_responsavel}'
        
    ax.set_title(titulo_grafico, fontsize=20, fontweight='bold', color='#2c3e50', pad=20)
    
    ax.set_yticks(y)
    ax.set_yticklabels(materiais, fontsize=13, color='#34495e')
    ax.tick_params(axis='x', labelsize=12, colors='#34495e')
    ax.tick_params(axis='y', length=0) # Remove os tracinhos rústicos do eixo Y
    
    # Adicionando um grid sutil de fundo para auxiliar a leitura
    ax.xaxis.grid(True, linestyle='--', alpha=0.5, color='#adb5bd')
    ax.set_axisbelow(True) # Garante que o grid fique atrás das barras

    # Removendo bordas soltas ao redor do gráfico (Despining)
    for spine in ['top', 'right', 'left']:
        ax.spines[spine].set_visible(False)
    ax.spines['bottom'].set_color('#adb5bd')
    ax.spines['bottom'].set_linewidth(1)

    # Legenda limpa
    ax.legend(fontsize=13, loc='upper right', frameon=True, facecolor='white', edgecolor='#e9ecef', framealpha=0.9)
    
    labels_personalizados = [f"{enc}{anot}" for enc, anot in zip(encontrado, anotacoes_grafico)]
    ax.bar_label(barras_enc, labels=labels_personalizados, padding=8, color='#2c3e50', fontweight='bold', fontsize=13)
    
    ax.margins(x=0.25)
    
    fig.tight_layout(rect=[0, 0, 1, 0.95])

    caminho_desktop = obter_area_de_trabalho()
    pasta_destino = os.path.join(caminho_desktop, "Graficos_Checklist")
    
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
    
    nome_base = os.path.basename(caminho_txt).replace('.txt', '.png')
    nome_imagem = os.path.join(pasta_destino, nome_base)
    
    fig.savefig(nome_imagem, dpi=300, bbox_inches='tight')
    
    print(f"Sucesso! Gráfico salvo na Área de Trabalho em: {nome_imagem}")
    
    return nome_imagem