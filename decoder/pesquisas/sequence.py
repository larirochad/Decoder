import pandas as pd
import inquirer


def verificar_sequencia(caminho_arquivo):
    try:
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
        if 'sequência' not in df.columns:
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

        df_clean['num_valor'] = df_clean[coluna_seq].apply(lambda x: int(x[2:], 16)) # para inteiro
        df_clean = df_clean.sort_values(by='num_valor').reset_index(drop=True)

        valores = df_clean[coluna_seq].tolist()
        indices = df_clean.index.tolist()
        numeros = df_clean['num_valor'].tolist()

        #LISTA DE PROBLEMAS 
        problemas_ordem = []
        problemas_repetidos = []
        problemas_salto = []

        for i in range(len(numeros) - 1):
            atual_valor = numeros[i]
            proximo_valor = numeros[i + 1]
            atual_hex = valores[i]
            proximo_hex = valores[i + 1]

            tipo_anterior = df_clean.iloc[i].get('tipo mensagem', 'N/D')
            tipo_proximo = df_clean.iloc[i + 1].get('tipo mensagem', 'N/D')

            if atual_valor > proximo_valor: # para fora de ordem
                problemas_ordem.append({
                    'linha': indices[i + 1] + 2,
                    'valor_anterior': atual_hex,
                    'valor_proximo': proximo_hex,
                    'tipo_anterior': tipo_anterior,
                    'tipo_proximo': tipo_proximo
                })
            elif atual_valor == proximo_valor: #igual
                problemas_repetidos.append({
                    'linha': indices[i + 1] + 2,    
                    'valor_anterior': atual_hex,
                    'valor_proximo': proximo_hex,
                    'tipo_anterior': tipo_anterior,
                    'tipo_proximo': tipo_proximo
                })
            elif proximo_valor != atual_valor + 1: #(salto)
                problemas_salto.append({
                    'linha': indices[i + 1] + 2,
                    'valor_anterior': atual_hex,
                    'valor_proximo': proximo_hex,
                    'tipo_anterior': tipo_anterior,
                    'tipo_proximo': tipo_proximo
                })


        total_ordem = len(problemas_ordem)
        total_repetidos = len(problemas_repetidos)
        total_salto = len(problemas_salto)
        total_problemas = total_ordem + total_repetidos + total_salto

        if total_problemas:
            print(f"\n⚠️ Problemas encontrados ({total_problemas}):")

            if total_repetidos:
                print(f"\n🟰 Problemas de VALORES REPETIDOS ({total_repetidos}):")
                for prob in problemas_repetidos:
                    print(f"Linha {prob['linha']}: Tipo {prob['tipo_anterior']} {prob['valor_anterior']} = {prob['valor_proximo']} Tipo {prob['tipo_proximo']}")

            if total_ordem:
                print(f"\n🔁 Problemas de ORDEM INCORRETA ({total_ordem}):")
                for prob in problemas_ordem:
                    print(f"Linha {prob['linha']}: Tipo {prob['tipo_anterior']} {prob['valor_anterior']} → {prob['valor_proximo']} Tipo {prob['tipo_proximo']}")

            if total_salto:
                print(f"\n⏭️ Problemas de SALTO NA SEQUÊNCIA ({total_salto}):")
                for prob in problemas_salto:
                    print(f"Linha {prob['linha']}: Tipo {prob['tipo_anterior']} {prob['valor_anterior']} → {prob['valor_proximo']} Tipo {prob['tipo_proximo']}")
        else:
            print("\n✅ Nenhum problema encontrado na sequência!\n")


        # salvar = inquirer.prompt([
        #         inquirer.List("salvar_csv",
        #                     message="Deseja salvar a análise em um arquivo CSV?",
        #                     choices=["Não", "Sim"])
        #         ])["salvar_csv"]

        # if salvar == "Sim":
        #     project_base = os.path.dirname(os.path.abspath(__file__)) #onde ta o arquivo
        #     target_dir = os.path.abspath(os.path.join(project_base, '..', 'logs/analises')) #volta uma pasta e entra em logs/ e espera o tipo passado pelo teste
        
        # logs = os.path.join(target_dir, logs)


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
                'sequencia_ok': total_problemas == 0,
                'problemas_ordem': problemas_ordem,
                'problemas_salto': problemas_salto,
                'valores': valores
            }

        return {
            'total': len(valores),
            'sequencia_ok': total_problemas == 0,
            'problemas_ordem': problemas_ordem,
            'problemas_salto': problemas_salto,
            'valores': valores
        }

    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        return None
