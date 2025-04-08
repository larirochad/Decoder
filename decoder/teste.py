from datetime import datetime

last_send_time = None

def calcular_diferenca_tempo(send_time):
    global last_send_time
    dia = int(send_time[6:8], 16)
    mes = int(send_time[4:6], 16)
    ano = int(send_time[0:4], 16)
    hora = int(send_time[8:10], 16)
    minuto = int(send_time[10:12], 16)
    segundo = int(send_time[12:14], 16)

    if ano == 0 or mes == 0 or dia == 0:
        print("Data com valores inválidos (zero). Ignorando cálculo de tempo.")
        return None

    new_time = datetime(ano, mes, dia, hora, minuto, segundo)

    if last_send_time is not None:
        diff = (new_time - last_send_time).total_seconds()
        print(f"Diferença de tempo: {diff} segundos")
    else:
        print("Primeira ocorrência, sem diferença de tempo.")
        diff = None

    last_send_time = new_time
    return diff


def parse_gteri_message(d):
    print("Mensagem bruta:", d)
    message_type = d[8:10]
    print("Message type:", message_type, "(esperado: 12 / decimal 18)")

    if int(message_type, 16) == 18:
        print(">> Entrei no bloco GTERI")
        report_mask = d[10:18]
        print("Report Mask:", report_mask)
        
        if report_mask == "00fe7fbf":
            print("Máscara compatível com 00fe7fbf")
        else:
            print("Máscara incompatível com 00fe7fbf")

            
            eri_mask = d[18:26]
            p = 30
            device_type = d[p:p + 6]
            p += 6
            protocol_version = d[p:p + 4]
            p += 4
            firmware_version = d[p:p + 4]
            p += 4
            unique_id1 = d[p:p + 2]
            p += 2
            unique_id2 = d[p:p + 2]
            p += 2
            unique_id3 = d[p:p + 2]
            p += 2
            unique_id4 = d[p:p + 2]
            p += 2
            unique_id5 = d[p:p + 2]
            p += 2
            unique_id6 = d[p:p + 2]
            p += 2
            unique_id7 = d[p:p + 2]
            p += 2
            unique_id8 = d[p:p + 2]
            p += 2
            battery_level = int(d[p:p + 2], 16)
            p += 2
            external_power_voltage = int(d[p:p + 4], 16)
            p += 4
            analog_input_mode = d[p:p + 4]
            p += 4
            #analog_input1_voltage = d[p:p + 4]
            #p += 4
            digital_input_status = d[p:p + 2]
            p += 2
            digital_output_status = d[p:p + 2]
            p += 2
            motion_status = d[p:p + 2]
            p += 2
            satellites_in_use = d[p:p + 2]
            p += 2
            report_id = d[p:p + 2]
            p += 2
            reserved = d[p:p + 2]
            p += 2
            onewire = d[p:p + 2]
            p += 2 
            rat = d[p:p + 2]
            p += 2 
            band = d[p:p + 4]
            p += 4
            IgnTrigger = d[p:p + 8]
            p += 8
            number = d[p:p + 2]
            p += 2
            gnss_accuracy = d[p:p + 2]
            p += 2
            speed = d[p:p + 6]
            p += 6
            azimuth = d[p:p + 4]
            p += 4
            altitude = d[p:p + 4]
            p += 4
            longitude = d[p:p + 8]
            if longitude == "00000000":
                longitude_final = "00000000"
            else:
                longitude_final = str((int(longitude, 16) - 4294967295) / 1e6)
            p += 8
            latitude = d[p:p + 8]
            if latitude == "00000000":
                latitude_final = "00000000"
            else:
                latitude_final = str((int(latitude, 16) - 4294967295) / 1e6)
            p += 8
            gnss_utc_time = d[p:p + 14]
            p += 14
            mcc = d[p:p + 4]
            p += 4
            mnc = d[p:p + 4]
            p += 4
            lac = d[p:p + 4]
            p += 4
            cell_id = d[p:p + 8]
            p += 8
            reserved = d[p:p + 2]
            p += 2
            current_mileage = d[p:p + 6]
            p += 6
            total_mileage = d[p:p + 10]
            p += 10
            current_hour_meter_count = d[p:p + 6]
            p += 6
            total_hour_meter_count = d[p:p + 12]
            p += 12
            RFID = d[p:p + 2]
            p += 2
            send_time = d[p:p + 14]
            p += 14

            print("mask eri: ", eri_mask)
            print("Report Mask: " + report_mask)
            print("Device Type: " + device_type)
            print("Protocol Version: " + protocol_version)
            print("Firmware Version: " + firmware_version)
            imei = (str(int(unique_id1, 16)) + str(int(unique_id2, 16)) + str(int(unique_id3, 16)) +
                    str(int(unique_id4, 16)) + str(int(unique_id5, 16)) + str(int(unique_id6, 16)) +
                    str(int(unique_id7, 16)) + str(int(unique_id8, 16)))
            print("Unique ID: " + imei)
            print("Battery Level: ", battery_level)
            print("External Power Voltage: ", external_power_voltage)
            print("Analog Input Mode: " + analog_input_mode)
            #print("Analog Input1 Voltage: " + analog_input1_voltage)  Não tem!
            print("Digital Input Status: " + digital_input_status)
            print("Digital Output Status: " + digital_output_status)
            print("Motion Status: " + motion_status)
            print("Satellites in Use: " + satellites_in_use)
            print("Report type: ", report_id)
            print("reserved: ", reserved)
            print("1wire: ", onewire)
            print("RAT: ", rat)
            print("band: ", band)
            print("IGN trigger: ", IgnTrigger)
            print("Number: " + number)
            print("GNSS Accuracy: " + gnss_accuracy)
            print("Speed: " + speed)
            print("Azimuth: " + azimuth)
            print("Altitude: " + altitude)
            print("Longitude: " + longitude_final)
            print("Latitude: " + latitude_final)
            print("GNSS UTC Time: " + gnss_utc_time)
            dia1 = (int(gnss_utc_time[6:8], 16))
            mes1 = (int(gnss_utc_time[4:6], 16))
            ano1 = (int(gnss_utc_time[0:4], 16))
            hora1 = (int(gnss_utc_time[8:10], 16))
            min1 = (int(gnss_utc_time[10:12], 16))
            seg1 = (int(gnss_utc_time[12:14], 16))
            # seg_fix = (int(gnss_utc_time[12:14]))
            # print(
            #     "Time fix: " + gnss_utc_time + f" | {dia.zfill(2)}/{mes.zfill(2)}/{ano} | {hora.zfill(2)}:{min.zfill(2)}:"
            #                                 f"{seg.zfill(2)}")
            print("MCC: " + mcc)
            print("MNC: " + mnc)
            print("LAC: " + lac)
            print("Cell ID: " + cell_id)
            print("Current Mileage: " + current_mileage)
            print("Total Mileage: " + total_mileage)
            print("Current Hour Meter Count: " + current_hour_meter_count)
            print("Total Hour Meter Count: " + total_hour_meter_count)
            print("RFID: ",RFID)
            dia = str(int(send_time[6:8], 16))
            mes = str(int(send_time[4:6], 16))
            ano = str(int(send_time[0:4], 16))
            hora = str(int(send_time[8:10], 16))
            min = str(int(send_time[10:12], 16))
            seg = str(int(send_time[12:14], 16))
            print(
                "Send Time: " + send_time + f" | {dia.zfill(2)}/{mes.zfill(2)}/{ano} | {hora.zfill(2)}:{min.zfill(2)}:"
                                            f"{seg.zfill(2)}")
        if send_time:
            calcular_diferenca_tempo(send_time)

    else:
        print(">> Não é mensagem GTERI")


# Exemplo de mensagem com tipo 0x12 (18 decimal)
mensagem_hex = "2b5253501209fe3fbf00028002007380200309020915564a58060e07630464320c00000000110c1000000400030000000001010000000110023efcf35331fe9bb00707e904080e3324072400048632043a1c09000000000000000000000000000000040b1e0007e904080e33271d00c2c20d0a"

parse_gteri_message(mensagem_hex)
