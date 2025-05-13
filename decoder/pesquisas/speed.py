import pandas as pd
from datetime import timedelta

LIMITE_VELOCIDADE = 40  # km/h

# ========== 1. Leitura dos arquivos ==========
def ler_tm08(path):
    df = pd.read_csv(path, sep=None, engine='python')
    df = df[df['Evento Gerador'].isin(['Retorno à velocidade normal', 'Velocidade máxima excedida'])]
    df['mrvDataHoraExibicao'] = pd.to_datetime(df['mrvDataHoraExibicao'], errors='coerce')
    df['mrvDataHoraExibicao'] += timedelta(hours=3)  # Corrigir fuso
    return df[['mrvDataHoraExibicao', 'Velocidade', 'Evento Gerador', 'Latitude', 'Longitude']].sort_values('mrvDataHoraExibicao')

def ler_gv58(path):
    df = pd.read_csv(path, encoding='latin1')
    df = df[df['Tipo Mensagem'] == 'GTSPD']
    df['Data/Hora Evento'] = pd.to_datetime(df['Data/Hora Evento'], errors='coerce')
    df = df[['Data/Hora Evento', 'Velocidade', 'Latitude', 'Longitude']]
    return df.dropna().sort_values('Data/Hora Evento')

# ========== 2. Extração dos eventos ==========
def extrair_eventos_tm08(df):
    eventos = []
    excedendo = None
    for _, row in df.iterrows():
        if row['Evento Gerador'] == 'Velocidade máxima excedida':
            excedendo = row
        elif row['Evento Gerador'] == 'Retorno à velocidade normal' and excedendo is not None:
            tempo = row['mrvDataHoraExibicao'] - excedendo['mrvDataHoraExibicao']
            eventos.append({
                'inicio': excedendo['mrvDataHoraExibicao'],
                'fim': row['mrvDataHoraExibicao'],
                'duracao': tempo,
                'vel_subida': excedendo['Velocidade'],
                'vel_retorno': row['Velocidade'],
                'vel_max': max(excedendo['Velocidade'], row['Velocidade']),
                'vel_media': (excedendo['Velocidade'] + row['Velocidade']) / 2,
                'local_inicio': (excedendo['Latitude'], excedendo['Longitude']),
                'local_fim': (row['Latitude'], row['Longitude']),
            })
            excedendo = None
    return eventos

def extrair_eventos_gv58(df):
    eventos = []
    excedendo = None
    for _, row in df.iterrows():
        if row['Velocidade'] > LIMITE_VELOCIDADE and excedendo is None:
            excedendo = row
        elif row['Velocidade'] <= LIMITE_VELOCIDADE and excedendo is not None:
            tempo = row['Data/Hora Evento'] - excedendo['Data/Hora Evento']
            eventos.append({
                'inicio': excedendo['Data/Hora Evento'],
                'fim': row['Data/Hora Evento'],
                'duracao': tempo,
                'vel_subida': excedendo['Velocidade'],
                'vel_retorno': row['Velocidade'],
                'vel_media': (excedendo['Velocidade'] + row['Velocidade']) / 2,
                'vel_max': max(excedendo['Velocidade'], row['Velocidade']),
                'local_inicio': (excedendo['Latitude'], excedendo['Longitude']),
                'local_fim': (row['Latitude'], row['Longitude']),
            })
            excedendo = None
    return eventos

# ========== 3. Impressão dos eventos lado a lado ==========
def print_eventos_comparados(tm08_eventos, gv58_eventos):
    col_width = 45
    separator = " | "
    divider = "-" * col_width + separator + "-" * col_width

    print("\n" + "=" * 25 + " DETALHES DOS EVENTOS DE EXCESSO DE VELOCIDADE " + "=" * 25)
    print(f"\n📌 Detalhes dos eventos de excesso - TM08".ljust(col_width) + separator + "📌 Detalhes dos eventos de excesso - GV58")

    max_len = max(len(tm08_eventos), len(gv58_eventos))

    for i in range(max_len):
        e1 = tm08_eventos[i] if i < len(tm08_eventos) else None
        e2 = gv58_eventos[i] if i < len(gv58_eventos) else None

        def print_line(label, key, fmt="{}", default="---"):
            val1 = default
            if e1 and key in e1 and e1[key] is not None:
                if isinstance(e1[key], pd.Timestamp):
                    val1 = e1[key].strftime("%Y-%m-%d %H:%M:%S")
                else:
                    val1 = fmt.format(e1[key])

            val2 = default
            if e2 and key in e2 and e2[key] is not None:
                if isinstance(e2[key], pd.Timestamp):
                    val2 = e2[key].strftime("%Y-%m-%d %H:%M:%S")
                else:
                    val2 = fmt.format(e2[key])

            left_text = f"{label}: {val1}"
            right_text = f"{label}: {val2}"
            print(f"{left_text:<{col_width}}{separator}{right_text}")

        print(f"\n🔹 Evento {i+1}")
        print(divider)
        print_line("⏱️ Início", "start_time")
        print_line("🚀 Vel. registrada", "vel_subida", "{:.2f} km/h")
        print_line("⏱️ Fim", "end_time")
        print_line("\U0001f680 Vel. de retorno registrada", "vel_retorno", "{:.2f} km/h")
        print_line("⏳ Duração", "duration", "{:.0f} segundos")
        print(divider)

# ========== 4. Análise principal ==========
def analisar():
    tm08_df = ler_tm08('tm08_vel.csv')
    gv58_df = ler_gv58('4-GPS-beidou_decoded.csv')

    eventos_tm08 = extrair_eventos_tm08(tm08_df)
    eventos_gv58 = extrair_eventos_gv58(gv58_df)

    def calcular_resumo(eventos):
        if not eventos:
            return {
                'total_events': 0,
                'excess_events': 0,
                'return_events': 0,
                'total_excess_time': 0,
                'avg_excess_time': 0,
                'max_speed': 0,
                'avg_speed_during_excess': 0,
                'excess_durations': []
            }

        total_tempo = sum([e['duracao'].total_seconds() for e in eventos])
        avg_tempo = total_tempo / len(eventos)
        max_speed = max([e['vel_max'] for e in eventos])
        avg_speed = sum([e['vel_media'] for e in eventos]) / len(eventos)

        excess_durations = [
            {
                'start_time': e['inicio'],
                'end_time': e['fim'],
                'duration': e['duracao'].total_seconds(),
                'max_speed': e['vel_max'],
                'vel_subida': e['vel_subida'],
                'vel_retorno': e['vel_retorno'],
                'local_inicio': e['local_inicio'],
                'local_fim': e['local_fim']
            }
            for e in eventos
        ]

        return {
            'total_events': len(eventos) * 2,
            'excess_events': len(eventos),
            'return_events': len(eventos),
            'total_excess_time': total_tempo,
            'avg_excess_time': avg_tempo,
            'max_speed': max_speed,
            'avg_speed_during_excess': avg_speed,
            'excess_durations': excess_durations
        }

    tm08_results = calcular_resumo(eventos_tm08)
    gv58_results = calcular_resumo(eventos_gv58)

    # Impressão do resumo
    print("\n===== RESUMO DE ANÁLISE DE VELOCIDADE =====")

    for label, result in [('TM08', tm08_results), ('GV58', gv58_results)]:
        print(f"\n----- Dispositivo {label} -----")
        print(f"Total de eventos: {result['total_events']}")
        print(f"Eventos de excesso: {result['excess_events']}")
        print(f"Eventos de retorno: {result['return_events']}")
        print(f"Tempo total em excesso: {result['total_excess_time']:.0f} segundos")
        print(f"Tempo médio em excesso: {result['avg_excess_time']:.1f} segundos")
        print(f"Velocidade máxima: {result['max_speed']:.2f} km/h")
        print(f"Velocidade média durante excesso: {result['avg_speed_during_excess']:.2f} km/h")

    # Comparativos
    print("\n----- Comparativo entre dispositivos -----")
    time_diff = abs(tm08_results['total_excess_time'] - gv58_results['total_excess_time'])
    events_diff = abs(tm08_results['total_events'] - gv58_results['total_events'])
    max_speed_diff = abs(tm08_results['max_speed'] - gv58_results['max_speed'])

    print(f"Diferença no tempo total em excesso: {time_diff:.2f} segundos")
    print(f"Diferença no número de eventos: {events_diff}")
    print(f"Diferença na velocidade máxima: {max_speed_diff:.2f} km/h")

    print_eventos_comparados(tm08_results['excess_durations'], gv58_results['excess_durations'])

if __name__ == "__main__":
    analisar()