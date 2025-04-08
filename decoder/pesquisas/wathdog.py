import pandas as pd
from buffer import *
from sequence import *


def analise_watchdog(caminho_arquivo):
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
            
        motivos_reboot = {
            "01": "Reinicialização para modo de trabalho baseado em tempo",
            "02": "Reinicialização para modo de trabalho de ignição ligada",
            "03": "Reinicialização acionada por entrada",
            "04": "Watchdog de rede",
            "05": "Watchdog EGPRS/GSM e LTE",
            "06": "Watchdog de falha de envio",
            "07": "RF - Watchdog de rede",
            "08": "RF - Watchdog EGPRS/LTE",
            "09": "RF - Watchdog de falha de envio",
            "0A": "Falta de mensagens CANBUS do CAN100"
        }

        def identificar_motivo(report_type_str):
            if not isinstance(report_type_str, str):
                report_type_str = str(report_type_str)

            report_type_str = report_type_str.strip().upper()

            if len(report_type_str) == 1 and report_type_str[1] == '3':
                input_id = report_type_str[0]
                return f"Motivo: {report_type_str} | Input {input_id} por input id"
            
            motivo = motivos_reboot.get(report_type_str.zfill(2), f"Motivo: {report_type_str}")
            return f"{motivo}"
            
    
        df.columns = df.columns.str.strip().str.lower()
        
        col_tipo_msg = next((col for col in df.columns if "tipo mensagem" in col), None)
        col_report_type = next((col for col in df.columns if "report type" in col), None)

        if not col_tipo_msg or not col_report_type:
            print("❌ Colunas necessárias não encontradas.")
            return

        print("\n📋 Reboots encontrados (GTDOG):")
        for idx, row in df.iterrows():
            tipo_msg = str(row[col_tipo_msg]).strip().upper()
            if tipo_msg == "GTDOG":
                report_val = str(row[col_report_type]).strip()
                motivo = identificar_motivo(report_val)
                print(f"Linha {idx + 2}: GTDOG - {motivo}")  # +2 = 1 para cabeçalho + 1 para índice base 0

        print("\n✅ Análise concluída.")


    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        return None


# if __name__ == "__main__":
#     warnings.filterwarnings("ignore", category=FutureWarning)
#     caminho, df = selecionar_pasta()
#     if caminho and df is not None:
#         analise_watchdog(caminho, df)
