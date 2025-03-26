import pandas as pd
import inquirer
import os

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


def verificar_sequencia(caminho_arquivo):
    try:
        # Tentar ler com diferentes codificações
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

        df.columns = df.columns.str.strip().str.lower()
        if 'sequência' not in df.columns and 'sequencia' not in df.columns:
            coluna_seq = next((col for col in df.columns if 'seq' in col), None)
            if not coluna_seq:
                print("Erro: Nenhuma coluna de sequência encontrada.")
                return None
        else:
            coluna_seq = 'sequência' if 'sequência' in df.columns else 'sequencia'

        # Limpar e filtrar dados
        df_clean = df.dropna(subset=[coluna_seq]).copy()
        df_clean[coluna_seq] = df_clean[coluna_seq].astype(str).str.lower().str.strip()

        # Garantir que todos comecem com '0x' e tenham exatamente 4 dígitos hexadecimais
        df_clean = df_clean[df_clean[coluna_seq].str.match(r'^(0x)?[0-9a-f]{1,4}$')]
        df_clean[coluna_seq] = df_clean[coluna_seq].apply(
            lambda x: '0x' + x[-4:].zfill(4) if not x.startswith('0x') else '0x' + x[2:].zfill(4)
        )

        # Converter para valores numéricos para ordenação
        df_clean['num_valor'] = df_clean[coluna_seq].apply(lambda x: int(x[2:], 16))
        
        
        # Ordenar os dados em ordem crescente pelos valores numéricos
        df_clean = df_clean.sort_values(by='num_valor').reset_index(drop=True)
        
        valores = df_clean[coluna_seq].tolist()
        indices = df_clean.index.tolist()


        # Verificação da sequência (string baseada, confiável com 2 bytes)
        problemas = []
        for i in range(len(valores) - 1):
            atual = valores[i]
            proximo = valores[i + 1]
            if atual >= proximo:
                tipo_anterior = df_clean.iloc[i].get('tipo mensagem', 'N/D')
                tipo_proximo = df_clean.iloc[i + 1].get('tipo mensagem', 'N/D')
                problemas.append({
                    'linha': indices[i + 1] + 2,
                    'valor_anterior': atual,
                    'valor_proximo': proximo,
                    'tipo_anterior': tipo_anterior,
                    'tipo_proximo': tipo_proximo
                })

        # Resultados
        print("\n=== RESULTADO DA ANÁLISE ===")
        print(f"Mensagens analisadas: {len(valores)}")
        print(f"Início da sequência: {valores[0]}")
        print(f"Fim da sequência:    {valores[-1]}")
        print(f"Sequência estritamente crescente? {'✅ Sim' if not problemas else '❌ Não'}")
        


        if problemas:
            print(f"\n⚠️ Problemas encontrados ({len(problemas)}):")
            for prob in problemas[:5]:
                print(f"Linha {prob['linha']}: Tipo {prob['tipo_anterior']} {prob['valor_anterior']} → {prob['valor_proximo']} Tipo {prob['tipo_proximo']}")
            if len(problemas) > 5:
                print(f"... e mais {len(problemas) - 5} problemas.")

        escolha = inquirer.prompt([
        inquirer.List("arquivo", 
                     message="Quer analisar os dados em ordem crescente??", 
                     choices=["Não", "Sim"])
         ])["arquivo"]
        
        if escolha == "Sim":
            print("\n=== DADOS ORDENADOS ===")
            print(df_clean[[coluna_seq, 'num_valor', 'tipo mensagem']].to_string())
        else: 

            return {
                'total': len(valores),
                'sequencia_ok': not problemas,
                'problemas': problemas,
                'valores': valores
            }
        return {
            'total': len(valores),
            'sequencia_ok': not problemas,
            'problemas': problemas,
            'valores': valores
        }
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        return None
    
# if __name__ == "__main__":
#     print("=== ANALISADOR DE MENSAGENS EM BUFFER ===")
#     arquivo = selecionar_arquivo()
#     print(f"\nArquivo selecionado: {arquivo}")
    
#     resultados = verificar_sequencia(arquivo)
    
#     if resultados:
#         print("\nAnálise concluída com sucesso!")
#     else:
#         print("\nFalha na análise do arquivo.")