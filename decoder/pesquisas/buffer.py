import pandas as pd
import inquirer
import os
import warnings
from contextlib import redirect_stderr
import io

# def selecionar_arquivo():
#     caminho_csv = 'C:\\Users\\Larissa Rocha\\Documents\\GitHub\\Decoder\\decoder\\logs'
    
#     if not os.path.exists(caminho_csv):
#         print(f"Diretório não encontrado: {caminho_csv}")
#         exit()
    
#     arquivos = [f for f in os.listdir(caminho_csv) if f.lower().endswith(".csv")]
    
#     if not arquivos:
#         print("Nenhum arquivo CSV encontrado no diretório.")
#         exit()
    
#     opcoes = ["🔤 Digitar o nome do arquivo"] + arquivos
    
#     escolha = inquirer.prompt([
#         inquirer.List("arquivo", 
#                      message="Escolha um arquivo ou digite um nome:", 
#                      choices=opcoes)
#     ])["arquivo"]
    
#     if escolha == "🔤 Digitar o nome do arquivo":
#         nome_digitado = input("Digite o nome do arquivo (com .csv): ").strip()
#         if nome_digitado not in arquivos:
#             print("Arquivo não encontrado na pasta.")
#             exit()
#         arquivo_final = nome_digitado
#     else:
#         arquivo_final = escolha
    
#     return os.path.join(caminho_csv, arquivo_final)

def analisar_mensagens_buffer(caminho_arquivo):
    try:
        # Redireciona todos os avisos para um buffer vazio
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            f = io.StringIO()
            with redirect_stderr(f):
                df = pd.read_csv(caminho_arquivo, sep=',', on_bad_lines='skip', engine='python')
        
        if not all(col in df.columns for col in ['Data', 'Hora', 'Origem', 'Payload']):
            print("Erro: Estrutura do arquivo inválida")
            return None
        
        df.columns = df.columns.str.strip()
        colunas_esperadas = ['Data', 'Hora', 'Origem', 'Payload']
        
        colunas_encontradas = [col for col in colunas_esperadas if col in df.columns]
        if len(colunas_encontradas) < len(colunas_esperadas):
            print(f"Erro: O arquivo não possui todas as colunas necessárias. Esperado: {colunas_esperadas}")
            return None
        
        # Filtrar mensagens da origem 'D' que começam com '2b42'
        mensagens_buffer = df[(df['Origem'] == 'D') & 
                            (df['Payload'].str.startswith('2b42', na=False))].copy()  # Usando .copy() para evitar SettingWithCopyWarning
        
        # Verificar se há mensagens
        if mensagens_buffer.empty:
            print("Nenhuma mensagem em buffer encontrada.")
            return None
        
        # Converter para datetime com formato explícito
        try:
            mensagens_buffer.loc[:, 'DataHora'] = pd.to_datetime(
                mensagens_buffer['Data'] + ' ' + mensagens_buffer['Hora'],
                format='%d/%m/%Y %H:%M:%S',  # Formato corrigido para usar : em vez de .
                dayfirst=True
            )
        except ValueError as e:
            print(f"Erro ao converter datas: {str(e)}")
            print("Exemplo de formato encontrado:", mensagens_buffer['Data'].iloc[0] + " " + mensagens_buffer['Hora'].iloc[0])
            return None
        
        # Ordenar por data e hora
        mensagens_buffer.sort_values('DataHora', inplace=True)
        
        # Pegar primeiro e último horário
        primeiro_horario = mensagens_buffer.iloc[0]['Hora']
        ultimo_horario = mensagens_buffer.iloc[-1]['Hora']
        
        # Análise dos resultados
        total = len(mensagens_buffer)
        mensagens_por_hora = mensagens_buffer.groupby(['Data', 'Hora']).size().reset_index(name='Contagem')
        
        # Exibir resultados
        print("\n=== RESULTADOS DA ANÁLISE ===")
        print(f"Total de mensagens em buffer: {total}")
        print(f"Primeira mensagem em buffer: {primeiro_horario}")
        print(f"Última mensagem em buffer: {ultimo_horario}")
        
        return {
            'total_mensagens_buffer': total,
            'primeiro_horario': primeiro_horario,
            'ultimo_horario': ultimo_horario,
            'mensagens_por_hora': mensagens_por_hora.to_dict('records'),
            'exemplo_mensagens': mensagens_buffer.head(3).to_dict('records')
        }
        
    except Exception as e:
        print(f"Erro ao processar o arquivo: {str(e)}")
        return None

# if __name__ == "__main__":
#     print("=== ANALISADOR DE MENSAGENS EM BUFFER ===")
#     arquivo = selecionar_arquivo()
#     print(f"\nArquivo selecionado: {arquivo}")
    
#     resultados = analisar_mensagens_buffer(arquivo)
    
#     if resultados:
#         print("\nAnálise concluída com sucesso!")
#     else:
#         print("\nFalha na análise do arquivo.")