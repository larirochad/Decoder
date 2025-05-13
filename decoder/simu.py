import simplekml
import pandas as pd
import random
from geopy.distance import geodesic
import datetime
import requests
import gzip
import shutil
import os

#############################################
# CONFIGURAÇÕES DO USUÁRIO
#############################################

arquivo_kml = "rota.kml"  # Nome do arquivo KML exportado do My Maps
velocidade_urbana = 40 / 3.6  # m/s
velocidade_rodovia = 100 / 3.6  # m/s
variacao_percentual = 0.10  # ±10%

#############################################
# 1. Ler os pontos do arquivo KML
#############################################

from fastkml import kml

with open(arquivo_kml, 'rt', encoding="utf-8") as f:
    doc = f.read()

k = kml.KML()
k.from_string(doc.encode("utf-8"))

placemarks = list(k.features())

# Assume que é uma única camada
document = list(placemarks[0].features())[0]
placemarks = list(document.features())

coordenadas = []
for pm in placemarks:
    try:
        coords = pm.geometry.coords[:]
        for coord in coords:
            coordenadas.append((coord[1], coord[0]))  # lat, lon
    except:
        pass

#############################################
# 2. Calcular tempos e velocidades
#############################################

tempo = 0
ultimo_ponto = None
saida = []

for ponto in coordenadas:
    lat, lon = ponto

    if ultimo_ponto:
        distancia = geodesic(ultimo_ponto, ponto).meters

        # Decide velocidade base
        if distancia < 300:
            velocidade_base = velocidade_urbana
        else:
            velocidade_base = velocidade_rodovia

        # Aplica variação aleatória
        variacao = velocidade_base * variacao_percentual
        velocidade_real = velocidade_base + random.uniform(-variacao, variacao)

        tempo_delta = distancia / velocidade_real
        tempo += tempo_delta

    else:
        velocidade_real = 0  # parado no início

    saida.append({
        'tempo_s': round(tempo, 2),
        'latitude': lat,
        'longitude': lon,
        'velocidade_m_s': round(velocidade_real, 2)
    })

    ultimo_ponto = ponto

# Salvar CSV
pd.DataFrame(saida).to_csv("trajeto_simulado.csv", index=False)
print("CSV gerado: trajeto_simulado.csv")

#############################################
# 3. Download automático das efemérides
#############################################

hoje = datetime.datetime.utcnow()
ano = hoje.year % 100  # últimos dois dígitos
dia_do_ano = hoje.timetuple().tm_yday
nome_arquivo = f"brdc{dia_do_ano:03d}0.{ano:02d}n.gz"
url = f"https://cddis.nasa.gov/archive/gnss/data/daily/{hoje.year}/{dia_do_ano:03d}/brdc/{nome_arquivo}"

print(f"Baixando efemérides: {url}")
r = requests.get(url)

if r.status_code == 200:
    with open(nome_arquivo, 'wb') as f:
        f.write(r.content)
    print(f"Efemérides baixadas: {nome_arquivo}")

    # Descompactar
    nome_final = nome_arquivo.replace('.gz', '')
    with gzip.open(nome_arquivo, 'rb') as f_in:
        with open(nome_final, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"Efemérides descompactadas: {nome_final}")

else:
    print("Não foi possível baixar as efemérides. Verifique a data ou URL.")

#############################################
print("\nArquivo CSV e efemérides prontos para usar no gps-sdr-sim!")