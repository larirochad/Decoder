import pandas as pd
from datetime import datetime
from contextlib import redirect_stderr


# def detect_encoding(file_path):
#     with open(file_path, 'rb') as f:
#         rawdata = f.read(10000)
#     return chardet.detect(rawdata)['encoding']

# def selecionar_arquivo():
#     caminho_csv = 'C:\\Users\\Larissa Rocha\\Documents\\GitHub\\Decoder\\decoder\\logs\\decoded'
    
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

def analyze_gnss_fix_time(caminho_arquivo):
    try:
        # Tentar ler com diferentes codificações
        codificacoes = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
        for encoding in codificacoes:
            try:
                df = pd.read_csv(caminho_arquivo, encoding=encoding)
                print(f"\nCodificação utilizada: {encoding}")
                break
            except UnicodeDecodeError:
                continue
        else:
            print("❌ Erro: Não foi possível ler o arquivo com as codificações testadas.")
            return

        df.columns = df.columns.str.strip()
        # print("\n✅ Colunas disponíveis no arquivo:", df.columns.tolist())

        # Mapeamento
        column_mapping = {
            'Evento': ['Evento', 'Data Evento', 'Dados Evento'],
            'Hora Evento': ['Hora Evento', 'Hora'],
            'Tipo Mensagem': ['Tipo Mensagem', 'Tipo Mensagei', 'Tipo'],
            'Time fix': ['Time fix', 'GNSS UTC Time', 'Tempo Fixo', 'Time for 1x']
        }

        matched_columns = {}
        for std_col, alts in column_mapping.items():
            for alt in alts:
                if alt in df.columns:
                    matched_columns[std_col] = alt
                    break

        missing = [col for col in column_mapping if col not in matched_columns]
        if missing:
            print(f"\n❌ Colunas necessárias não encontradas: {missing}")
            print("Verifique se o arquivo contém dados GNSS válidos.")
            return

        print("\nColunas mapeadas:")
        for k, v in matched_columns.items():
            print(f"  {k} -> {v}")

        df = df.rename(columns=matched_columns)
        df['Hora Evento'] = pd.to_datetime(df['Hora Evento'], format='%H:%M:%S', errors='coerce').dt.time
        df['Time fix'] = pd.to_datetime(df['Time fix'], errors='coerce')
        df = df.dropna(subset=['Hora Evento'])

        results = []
        last_none_time = None
        last_none_event_time = None

        for idx, row in df.iterrows():
            if pd.isna(row['Time fix']):
                last_none_time = row['Hora Evento']
                last_none_event_time = row.get('Evento', row.get(matched_columns.get('Evento', ''), ''))
            elif last_none_time is not None:
                try:
                    none_dt = datetime.combine(datetime.today(), last_none_time)
                    fix_dt = datetime.combine(datetime.today(), row['Hora Evento'])
                    diff = (fix_dt - none_dt).total_seconds()

                    if diff >= 0:
                        result = {
                            'Último evento sem fix': last_none_event_time,
                            'Hora último None': last_none_time.strftime('%H:%M:%S'),
                            'Primeiro evento com fix': row.get('Evento', row.get(matched_columns.get('Evento', ''), '')),
                            'Hora primeiro fix': row['Hora Evento'].strftime('%H:%M:%S'),
                            'Tempo para fix (segundos)': diff,
                            'Tipo Mensagem fix': row['Tipo Mensagem']
                        }
                        results.append(result)
                    last_none_time = None
                except Exception as e:
                    print(f"Erro ao calcular tempo (linha {idx}): {e}")

        if results:
            print("\n Resultados da análise:")
            print("=" * 80)
            for r in results:
                print(f"Entre {r['Hora último None']} e {r['Hora primeiro fix']}:")
                print(f"  Tempo para fix: {r['Tempo para fix (segundos)']} segundos")
                print(f"  Tipo de mensagem do fix: {r['Tipo Mensagem fix']}")
                print("-" * 80)

            tempos = [r['Tempo para fix (segundos)'] for r in results]
            print("\n📈 Resumo estatístico:")
            print(f"  Média:  {sum(tempos) / len(tempos):.2f} segundos")
            print(f"  Máximo: {max(tempos)} segundos")
            print(f"  Mínimo: {min(tempos)} segundos")
        else:
            print("\n Nenhum intervalo válido encontrado.")
            print("Verifique se há eventos com 'Time fix = None' seguidos por um horário válido.")

    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")

# if __name__ == "__main__":
#     warnings.filterwarnings("ignore", category=FutureWarning)
    
#     # Redirecionar stderr para capturar mensagens indesejadas
#     with redirect_stderr(io.StringIO()):
#         file_path = selecionar_arquivo()
#         analyze_gnss_fix_time(file_path)