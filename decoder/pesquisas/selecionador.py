import inquirer
import os
from buffer import *
from sequency import *
from time_fix import *


def selecionar_arquivo(tipo):
    if tipo == "decoded":
        caminho_csv = 'C:\\Users\\Larissa Rocha\\Documents\\GitHub\\Decoder\\decoder\\logs\\decoded'
    if tipo == "payload":
        caminho_csv = 'C:\\Users\\Larissa Rocha\\Documents\\GitHub\\Decoder\\decoder\\logs\\payload'

    if not os.path.exists(caminho_csv):
        print(f"Diretório não encontrado: {caminho_csv}")
        exit()

    arquivos = [
        f for f in os.listdir(caminho_csv)
        if f.lower().endswith(".csv") 
    ]

    if not arquivos:
        print(f"Nenhum arquivo CSV com filtro encontrado.")
        exit()

    opcoes = ["🔤 Digitar o nome do arquivo"] + arquivos
    
    escolha = inquirer.prompt([
        inquirer.List("arquivo", 
                     message="Escolha um arquivo ou digite um nome", 
                     choices=opcoes)
    ])["arquivo"]
    
    if escolha == "🔤 Digitar o nome do arquivo":
        nome_digitado = input("Digite o nome do arquivo (com .csv): ").strip()
        if nome_digitado not in arquivos:
            print("Arquivo não encontrado na pasta ou não bate com o filtro.")
            exit()
        arquivo_final = nome_digitado
    else:
        arquivo_final = escolha
    
    return os.path.join(caminho_csv, arquivo_final)

def seleciona_analise():
    caminho_teste = 'C:\\Users\\Larissa Rocha\\Documents\\GitHub\\Decoder\\decoder\\pesquisas'
    
    testes = [f for f in os.listdir(caminho_teste) 
              if f.lower().endswith(".py") and f != "selecionador.py"
    ] 
    
    opcao = inquirer.prompt([
        inquirer.List(
            "modo",
            message="Qual o teste que quer fazer?",
            choices= testes
        )
    ])["modo"]
    
    return opcao

while True:
    print("\n=== Selecione a análise a ser feita ===\n")
    teste = seleciona_analise()
    
    # Escolhendo filtro com base no teste
    if teste == "buffer.py":
        arquivo = selecionar_arquivo("payload")
        print(f"\nArquivo selecionado: {arquivo}")
        analisar_mensagens_buffer(arquivo)

    elif teste == "sequency.py":
        arquivo = selecionar_arquivo("decoded")
        print(f"\nArquivo selecionado: {arquivo}")
        verificar_sequencia(arquivo)
    
    elif teste == "time_fix.py":
        arquivo = selecionar_arquivo("decoded")
        print(f"\nArquivo selecionado: {arquivo}")
        analyze_gnss_fix_time(arquivo)