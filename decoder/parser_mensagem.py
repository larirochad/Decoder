from RSPMessages import *
from INFMessages import *
from EVTMessages import *
from recordMessages import *
from datetime import datetime

# Prefixes
HBDPrefix = "2b484244"
ackPrefix = "2b41434b"
plusPrefix = "2b"
rspPrefix = "5350"
infPrefix = "4e46"
evtPrefix = "5654"
crdPrefix = "5244"
bChar = "42"

print("Digite a mensagem em hex:")

while True:
    cmd = input(">> ").strip().lower()
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y,%H:%M:%S,")

    print("\n" + date_time + "D," + cmd)

    plus_sign = cmd[0:2]
    prefix = cmd[0:8]

    try:
        if prefix == HBDPrefix:
            print("Tipo: Heartbeat (HBD)")

        elif prefix == ackPrefix:
            print("Tipo: ACK")

        elif plus_sign == plusPrefix:
            if cmd[2:4] == bChar:
                print("Buffer: Sim")
            else:
                print("Buffer: Não")

            msg_type = cmd[4:8]
            if msg_type == rspPrefix:
                print("Tipo: RSP")
                parse_rsp_message(cmd, "", 0)
            elif msg_type == infPrefix:
                print("Tipo: INF")
                parse_inf_message(cmd, "", 0)
            elif msg_type == evtPrefix:
                print("Tipo: EVT")
                parse_evt_message(cmd, "", 0)
            elif msg_type == crdPrefix:
                print("Tipo: CRD (Data Flow Report)")
            else:
                print("Mensagem com prefixo desconhecido.")
        else:
            print("Mensagem não reconhecida.")
    except Exception as e:
        print("Erro ao tentar parsear a mensagem:", e)

    print("-" * 50)
