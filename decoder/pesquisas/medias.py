import os
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

# # Caminho para o arquivo CSV
# arq = os.path.dirname(os.path.abspath(__file__))
# arq2 = os.path.abspath(os.path.join(arq, '..', 'logs/decoded'))
# arquivo_csv = os.path.join(arq2, 'Dados_analisar_xande-const0.csv')

# df = pd.read_csv(arquivo_csv, encoding='latin1')
def analise_medias(caminho_arquivo):

    codificacoes = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
    for encoding in codificacoes:
        try:
            df = pd.read_csv(caminho_arquivo, encoding=encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        print("Erro: Não foi possível ler o arquivo com as codificações testadas.")
        return None

    coluna_satelites = 'Satélites'

    satelites = pd.to_numeric(df[coluna_satelites], errors='coerce')
    satelites = satelites.dropna()


    media = satelites.mean()
    # mediana = satelites.median()
    moda = stats.mode(satelites, keepdims=True).mode[0]
    desvio_padrao = satelites.std()
    minimo = satelites.min()
    maximo = satelites.max()

    print("=== Estatísticas dos Satélites ===")
    print(f"Média         : {media:.2f}")
    # print(f"Mediana       : {mediana}")
    print(f"Moda          : {moda}")
    print(f"Desvio Padrão : {desvio_padrao:.2f}")
    print(f'Mínimo: {minimo}')
    print(f'Máximo: {maximo}')


    # # HDOP (Precisão GNSS)
    coluna_hdop = 'Precisão GNSS'
    hdop = pd.to_numeric(df[coluna_hdop], errors='coerce').dropna()

    media_hdop = hdop.mean()
    # mediana_hdop = hdop.median()
    moda_hdop = stats.mode(hdop, keepdims=True).mode[0]
    desvio_padrao_hdop = hdop.std()
    minimo_hdop = hdop.min()
    maximo_hdop = hdop.max()

    print("=== Estatísticas do HDOP ===")
    print(f"Média         : {media_hdop:.2f}")
    # print(f"Mediana       : {mediana_hdop}")
    print(f"Moda          : {moda_hdop}")
    print(f"Desvio Padrão : {desvio_padrao_hdop:.2f}")
    print(f"Mínimo        : {minimo_hdop}")
    print(f"Máximo        : {maximo_hdop}\n")


    # === GRÁFICOS EM UMA FIGURA ===
    fig, axs = plt.subplots(3, 1, figsize=(10, 12))

    # 1. Histograma
    axs[0].hist(satelites, bins=10, edgecolor='black')
    axs[0].set_title('Histograma - Satélites')
    axs[0].set_xlabel('Número de Satélites')
    axs[0].set_ylabel('Frequência')
    axs[0].grid(True)

    # 2. Boxplot
    axs[1].boxplot(satelites, vert=True)
    axs[1].set_title('Boxplot - Satélites')
    axs[1].set_ylabel('Número de Satélites')
    axs[1].grid(True)

    # 3. Gráfico de linha
    axs[2].plot(satelites.values, marker='o', linestyle='-')
    axs[2].set_title('Variação dos Satélites ao Longo das Leituras')
    axs[2].set_xlabel('Índice da Leitura')
    axs[2].set_ylabel('Número de Satélites')
    axs[2].set_ylim(0, 14)
    axs[2].grid(True)
    # Ajusta layout e exibe
    plt.tight_layout()
    plt.show()


    plt.show()
   
    # Plotagem
    plt.figure(figsize=(12, 6))
    sns.kdeplot(satelites, fill=True, color='purple', linewidth=2)

    # Adiciona os pontos individuais na base (rug plot)
    sns.rugplot(satelites, color='black', height=0.05)  # height ajusta o tamanho das barrinhas

    # Linhas verticais para estatísticas principais
    plt.axvline(media, color='blue', linestyle='-', linewidth=2, label='Média')
    # plt.axvline(mediana, color='green', linestyle='--', linewidth=2, label='Mediana')
    plt.axvline(moda, color='red', linestyle='-.', linewidth=2, label='Moda')
    plt.axvline(minimo, color='orange', linestyle=':', linewidth=2, label='Mínimo')
    plt.axvline(maximo, color='brown', linestyle=':', linewidth=2, label='Máximo')

    # Faixa de desvio padrão ao redor da média
    plt.fill_betweenx(
        y=[0, plt.ylim()[1]],
        x1=media - desvio_padrao,
        x2=media + desvio_padrao,
        color='blue',
        alpha=0.1,
        label='±1 Desvio Padrão'
    )

    # Título e legenda
    plt.title('Distribuição de Satélites com Estatísticas e Pontos Individuais')
    plt.xlabel('Número de Satélites')
    plt.ylabel('Densidade')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Histograma do HDOP
    plt.figure(figsize=(10, 6))
    plt.hist(hdop, bins=10, edgecolor='black', color='teal')
    plt.title('Histograma - HDOP (Precisão GNSS)')
    plt.xlabel('HDOP')
    plt.ylabel('Frequência')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


  # === KDE do HDOP ===
    plt.figure(figsize=(12, 6))
    sns.kdeplot(hdop, fill=True, color='teal', linewidth=2)
    sns.rugplot(hdop, color='black', height=0.05)

    plt.axvline(media_hdop, color='blue', linestyle='-', linewidth=2, label='Média')
    # plt.axvline(mediana_hdop, color='green', linestyle='--', linewidth=2, label='Mediana')
    plt.axvline(moda_hdop, color='red', linestyle='-.', linewidth=2, label='Moda')
    plt.axvline(minimo_hdop, color='orange', linestyle=':', linewidth=2, label='Mínimo')
    plt.axvline(maximo_hdop, color='brown', linestyle=':', linewidth=2, label='Máximo')

    plt.fill_betweenx(
        y=[0, plt.ylim()[1]],
        x1=media_hdop - desvio_padrao_hdop,
        x2=media_hdop + desvio_padrao_hdop,
        color='blue',
        alpha=0.1,
        label='±1 Desvio Padrão'
    )

    plt.title('Distribuição do HDOP com Estatísticas e Pontos Individuais')
    plt.xlabel('HDOP')
    plt.ylabel('Densidade')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()



