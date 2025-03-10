from RSPMessages import *
from INFMessages import *
from EVTMessages import *
from recordMessages import *

import threading
import socket
import binascii
import datetime
import ifaddr
import os

# debug = 1-ativado, 0-desativado
debug = 0
sem_log = 0

msg_to_send = 0

# Prefixes
HBDPrefix = "2b484244"
plusPrefix = "2b"
rspPrefix = "5350"
infPrefix = "4e46"
evtPrefix = "5654"
crdPrefix = "5244"
ackPrefix = "2b41434b"
bChar = "42"

# thread concorrente para enviar comandos escritos no terminal
def worker():
    while True:
        cmd = input()
        server.sendto(str.encode(cmd, "utf-8"), address)
        record_raw(payload_file_name, "S", cmd)
        record_decoded(decoded_file_name,cmd)

# D: Enviado pelo Device
# S: Enviado pelo Server

adapters = ifaddr.get_adapters()
server_ip = 0

for adapter in adapters:
    if adapter.nice_name == "SonicWall_NetExtender_SSL Tunnel":
        server_ip = adapter.ips[1].ip
        print("VPN está ativa no IP {}".format(server_ip))
if server_ip == 0:
    print("VPN não está ativada.")
    exit()

if debug == 0:
    server_port = int(input("Digite a porta de comunicação: "))
    if server_port > 65535 or server_port < 0:
        print("Porta inválida")
        exit()
else:
    server_port = 9116
    #server_port = 10000

log_directory = "logs/"
os.makedirs(log_directory, exist_ok=True)  # Cria a pasta se não existir

if sem_log == 0:
    logDecision = int(input("Deseja criar um log? (1-Sim; 0-Não): "))
    if logDecision != 1:
        logDecision = 0
        print("Não será criado um log.")
        payload_file_name = ""
        decoded_file_name = ""
    else:
        val = input("Digite o nome do arquivo de log a ser criado: ")
        payload_file_name = os.path.join(log_directory, val + "_raw.csv")
        decoded_file_name = os.path.join(log_directory, val + "_decoded.csv")
        #payload_file_name = "log_raw.csv"
else:
    logDecision = 0
    payload_file_name = ""
    decoded_file_name = ""

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((server_ip, server_port))
except:
    print("Erro de IP ou Porta.")
    exit()

if logDecision == 1:
    try:
        open(payload_file_name, "r")
        print("Arquivo já existente, o log será adicionado a ele.")
    except:
        print("Arquivo não existe, um novo log será criado.")
        with open(payload_file_name, "a+") as f:
            f.write("Data,Hora,Origem,Payload\n")
            f.close()
        with open(decoded_file_name, "a+") as d:
            d.write("Data Inclusão,Hora Inclusão,Data Evento,Hora Evento,IMEI,Sequência,"
                    "Tipo Mensagem,Máscara,Tipo Dispositivo,Versão Protocolo,Versão Firmware,Bateria Interna,"
                    "Alimentação Externa,Analog Input Mode,Analog Input1 Voltage,Digital Input Status,"
                    "Digital Output Status,Motion Status,Satélites,Duração da Ignição,Precisão GNSS,"
                    "Velocidade,Azimuth,Altitude,Latitude,Longitude,GNSS UTC Time,MCC,MNC,LAC,Cell ID,"
                    "Hodômetro Atual,Hodômetro Total,Horímetro Atual,Horímetro Total,Motivo Power Off,"
                    "Motivo Power On"  "Diferença dos tempos de FRI\n")
            d.close()

print("Server iniciado no IP {} e porta {}".format(server_ip,server_port))

threading.Thread(target=worker, daemon=True).start()

while True:
    message, address = server.recvfrom(1024)
    data = binascii.hexlify(message).decode()
    #size = len(data)
    #print(size)
    curr_time = datetime.datetime.now()
    date_time = curr_time.strftime("%d/%m/%Y,%H:%M:%S,")
    print("\n")
    print(date_time + "D," + data)
    if logDecision == 1:
        record_raw(payload_file_name,"D",data)

    # Decodificando a mensagem
    plus_sign = data[0:2]
    message_prefix = data[0:8]

    # Processando Mensagens
    if message_prefix == HBDPrefix:
        print("Heartbeat")
        size = len(data)
        device_type_heartbeat = data[12:18]
        protocol_version_heartbeat = data[18:22]
        count_number = data[size - 12:(size - 8) - size]
        msg_to_send = "+SACK:GTHBD,"+device_type_heartbeat+protocol_version_heartbeat+","+count_number+"$"
        print(date_time + "S," + msg_to_send)
        server.sendto(str.encode(msg_to_send,"utf-8"), address)
        if logDecision == 1:
            record_raw(payload_file_name,"S",msg_to_send)
            record_decoded(decoded_file_name,",,,,HBD")
    elif message_prefix == ackPrefix:
        print("+ACK")
        size = len(data)
        device_type_heartbeat = data[12:18]
        protocol_version_heartbeat = data[18:22]
        count_number = data[size - 12:(size - 8) - size]
        msg_to_send = "+SACK:" + count_number + "$"
        print(date_time + "S," + msg_to_send)
        server.sendto(str.encode(msg_to_send, "utf-8"), address)
        if logDecision == 1:
            record_raw(payload_file_name, "S", msg_to_send)
            record_decoded(decoded_file_name,",,,,ACK")
    elif plus_sign == plusPrefix:
        if data[2:4] == bChar: # B
            buffer = True
            print("Buffer: Sim")
        else:
            buffer = False
            print("Buffer: Não")

        if data[4:8] == rspPrefix: # SP
            msg_to_send = parse_rsp_message(data,decoded_file_name,logDecision)
            print(date_time + "S," + msg_to_send)
            server.sendto(str.encode(msg_to_send, "utf-8"), address)
            if logDecision == 1:
                record_raw(payload_file_name, "S", msg_to_send)
        elif data[4:8] == infPrefix: # NF
            msg_to_send = parse_inf_message(data,decoded_file_name,logDecision)
            print(date_time + "S," + msg_to_send)
            server.sendto(str.encode(msg_to_send, "utf-8"), address)
            if logDecision == 1:
                record_raw(payload_file_name, "S", msg_to_send)
        elif data[4:8] == evtPrefix:  # VT
            msg_to_send = parse_evt_message(data,decoded_file_name,logDecision)
            print(date_time + "S," + msg_to_send)
            server.sendto(str.encode(msg_to_send, "utf-8"), address)
            if logDecision == 1:
                record_raw(payload_file_name, "S", msg_to_send)
        elif data[4:8] == crdPrefix:  # RD
            print("Group: Data Flow Report")
            print(date_time + "S," + msg_to_send)
            server.sendto(str.encode(msg_to_send, "utf-8"), address)
            if logDecision == 1:
                record_raw(payload_file_name, "S", msg_to_send)
        else:
            # print("Mensagem Desconhecida")
            # size = len(data)
            # count_number = data[size-4:(size-1) - size]
            # msg_to_send = "+SACK:" + count_number + "$"
            # print(date_time + "S," + msg_to_send)
            # server.sendto(str.encode(msg_to_send, "utf-8"), address)
            # if logDecision == 1:
            #     record_raw(payload_file_name, "S", msg_to_send)
        # Tentativa de converter a mensagem de hex para ASCII
            try:
            # Tentativa de converter a mensagem de hex para ASCII
                ascii_message = bytes.fromhex(data).decode('ascii')
                print("Mensagem Recebida (ASCII):", ascii_message)
            except ValueError:
                # Caso ocorra um erro na conversão, mantém como desconhecida
                print("Mensagem Desconhecida (erro na conversão)")

                size = len(data)
                count_number = data[size-4:(size-1) - size]
                msg_to_send = "+SACK:" + count_number + "$"
                print(date_time + "S," + msg_to_send)
                server.sendto(str.encode(msg_to_send, "utf-8"), address)