import inquirer
import os
from buffer import *
from sequence import *
from time_fix import *
from tkinter import filedialog
from wathdog import *
from medias import *

def selecionar_pasta(tipo):
    
    project_base = os.path.dirname(os.path.abspath(__file__)) #onde ta o arquivo
    target_dir = os.path.abspath(os.path.join(project_base, '..', 'logs', tipo)) #volta uma pasta e entra em logs/ e espera o tipo passado pelo teste
 
    file_path = filedialog.askopenfilename( #abre a pasta
        initialdir=target_dir,
        filetypes=[("CSV files", "*.csv")] 
    )

    return file_path  


def seleciona_analise():

    project_base = os.path.dirname(os.path.abspath(__file__)) #onde ta o arquivo
    target_dir = os.path.abspath(os.path.join(project_base, '..', 'pesquisas')) #volta uma pasta e entra em logs/ e espera o tipo passado pelo teste

    testes = [f for f in os.listdir(target_dir) 
              if f.lower().endswith(".py") and f != "selecionador.py" #filtro para noa mostrar esse arquivo
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
        arquivo = selecionar_pasta("payload")
        print(f"\nArquivo selecionado: {arquivo}")
        analisar_mensagens_buffer(arquivo)

    elif teste == "sequence.py":
        arquivo = selecionar_pasta("decoded")
        print(f"\nArquivo selecionado: {arquivo}")
        verificar_sequencia(arquivo)
    
    elif teste == "time_fix.py":
        arquivo = selecionar_pasta("decoded")
        print(f"\nArquivo selecionado: {arquivo}")
        analyze_gnss_fix_time(arquivo)
 
    elif teste == "watchdog.py":
        arquivo = selecionar_pasta("decoded")
        print(f"\nArquivo selecionado: {arquivo}")
        analise_watchdog(arquivo)        
    
    elif teste == "medias.py":
        arquivo = selecionar_pasta ("decoded")
        print(f"\nArquivo selecionado: {arquivo}")
        analise_medias(arquivo)

    elif teste == "speed.py":
        arquivos = selecionar_pasta("decoded")
        arquivo1, arquivo2 = arquivo[:2]
        print(f"Arquivo selecionado {arquivo}, {arquivo2}\n")
