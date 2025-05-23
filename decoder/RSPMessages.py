from recordMessages import *
from datetime import datetime

# Message Type List
RSPMessageTypeList = [""] * 104
RSPMessageTypeList.insert(1, "GTTOW")
RSPMessageTypeList.insert(3, "GTLBC")
RSPMessageTypeList.insert(4, "GTEPS")
RSPMessageTypeList.insert(5, "GTDIS")
RSPMessageTypeList.insert(6, "GTOIB")
RSPMessageTypeList.insert(7, "GTFRI")
RSPMessageTypeList.insert(9, "GTSPD")
RSPMessageTypeList.insert(10, "GTSOS")
RSPMessageTypeList.insert(11, "GTRTL")
RSPMessageTypeList.insert(12, "GTDOG")
RSPMessageTypeList.insert(14, "GTAIS")
RSPMessageTypeList.insert(15, "GTHBM")
RSPMessageTypeList.insert(16, "GTIGL")
RSPMessageTypeList.insert(17, "GTIDA")
RSPMessageTypeList.insert(18, "GTERI")
RSPMessageTypeList.insert(21, "GTGOT")
RSPMessageTypeList.insert(26, "GTVGL")
RSPMessageTypeList.insert(103, "GTRTI")

# rspGenericEventGroup = ["GTTOW","GTAIS","GTDIS","GTIOB","GTSPD","GTRTL","GTDOG","GTIGL","GTVGL","GTHBM","GTEPS"]

rspGenericEventGroup = ["GTTOW","GTAIS","GTDIS","GTIOB","GTSPD","GTRTL","GTIGL","GTVGL","GTHBM","GTEPS"]

last_send_time = None


def calcular_diferenca_tempo(send_time):
    """
    Calcula a diferença de tempo entre a última e a nova mensagem GTFRI 
    """
    global last_send_time 
    #i = send_time
    # Converter send_time de HEX para datetime
    dia = int(send_time[6:8], 16)
    mes = int(send_time[4:6], 16)
    ano = int(send_time[0:4], 16)
    hora = int(send_time[8:10], 16)
    minuto = int(send_time[10:12], 16)
    segundo = int(send_time[12:14], 16)

    new_time = datetime(ano, mes, dia, hora, minuto, segundo)

    if last_send_time is not None:
        diff = (new_time - last_send_time).total_seconds()
        # print(f"Diferença de tempo: {diff} segundos")
    else:
        print("Primeira ocorrência, sem diferença de tempo.")
        diff = None


    # Atualiza o tempo global
    last_send_time = new_time
    
    return diff
    


def parse_rsp_message(d,decoded_file_name,log_flag):

    print("Group: Position Related Report")
    size = len(d)
    message_type = d[8:10]
    count_number = d[size - 12:(size - 8) - size]
    print("Message Type: " + message_type + " -> " + RSPMessageTypeList[int(message_type, 16)])
    msg = "+SACK:" + count_number + "$"

    if RSPMessageTypeList[int(message_type, 16)] in rspGenericEventGroup:
        print("Formato Genérico")
        report_mask = d[10:18]
        if report_mask == "00fe7fbf": # Máscara genérica RSP e EVT
            print("Máscara compatível com 00fe7fbf")
        else:
            print("Máscara incompatível com 00fe7fbf")

        p = 22
        device_type = d[p:p+6]
        p+=6
        protocol_version = d[p:p+4]
        p+=4
        firmware_version = d[p:p+4]
        p+=4
        unique_id1 = d[p:p+2]
        p+=2
        unique_id2 = d[p:p+2]
        p+=2
        unique_id3 = d[p:p+2]
        p+=2
        unique_id4 = d[p:p+2]
        p+=2
        unique_id5 = d[p:p+2]
        p+=2
        unique_id6 = d[p:p+2]
        p+=2
        unique_id7 = d[p:p+2]
        p+=2
        unique_id8 = d[p:p+2]
        p+=2
        battery_level = int(d[p:p+2],16)
        p+=2
        external_power_voltage = int(d[p:p+4],16)
        p+=4
        analog_input_mode = d[p:p+4]
        p+=4
        analog_input1_voltage = d[p:p+4]
        p+=4
        digital_input_status = d[p:p+2]
        p+=2
        digital_output_status = d[p:p+2]
        p+=2
        motion_status = d[p:p+2]
        p+=2
        satellites_in_use = int(d[p:p + 2], 16)
        p+=2
        report_id = d[p:p+2]
        p+=2
        number = d[p:p+2]
        p+=2
        gnss_accuracy = d[p:p+2]
        p+=2
        speed_total = d[p:p + 6]
        p += 6
        speed_dec = int(speed_total[:4], 16)
        speed_frac = int(speed_total[4:], 16)
        speed = speed_dec + (speed_frac/10)
        azimuth = d[p:p+4]
        p+=4
        altitude = d[p:p+4]
        p+=4
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
        gnss_utc_time = d[p:p+14]
        p+=14
        mcc = d[p:p+4]
        p+=4
        mnc = d[p:p+4]
        p+=4
        lac = d[p:p+4]
        p+=4
        cell_id = d[p:p+8]
        p+=8
        reserved = d[p:p + 2]
        p += 2
        current_mileage1 = int(d[p:p + 4], 16)
        p += 4
        current_mileage2 = int(d[p:p + 2], 16)
        p += 2
        current_mileage = current_mileage1 + (current_mileage2 / 10)
        total_mileage1 = int(d[p:p + 8], 16)
        p += 8
        total_mileage2 = int(d[p:p + 2], 16)
        p += 2
        total_mileage = total_mileage1 + (total_mileage2 / 10)
        current_hour_meter_count_hh = str(int(d[p:p + 2], 16))
        p += 2
        current_hour_meter_count_mm = str(int(d[p:p + 2], 16))
        p += 2
        current_hour_meter_count_ss = str(int(d[p:p + 2], 16))
        p += 2
        current_hour_meter_count = (f"{current_hour_meter_count_hh}:{current_hour_meter_count_mm.zfill(2)}:"
                                    f"{current_hour_meter_count_ss.zfill(2)}")
        total_hour_meter_count_hh = str(int(d[p:p + 8], 16))
        p += 8
        total_hour_meter_count_mm = str(int(d[p:p + 2], 16))
        p += 2
        total_hour_meter_count_ss = str(int(d[p:p + 2], 16))
        p += 2
        total_hour_meter_count = (f"{total_hour_meter_count_hh}:{total_hour_meter_count_mm.zfill(2)}:"
                                    f"{total_hour_meter_count_ss.zfill(2)}")

        id_length = d[p:p + 2]
        p += 2
        if int(id_length, 16) != 0:
            id = d[p:p + (int(id_length, 16) * 2)]
            p += int(id_length, 16) * 2
        else:
            id = "0"
        send_time = d[p:p + 14]
        p += 14

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
        print("Analog Input1 Voltage: " + analog_input1_voltage)
        print("Digital Input Status: " + digital_input_status)
        print("Digital Output Status: " + digital_output_status)
        print("Motion Status: " + motion_status)
        print("Satellites in Use: " + str(satellites_in_use))
        print("Number: " + number)
        print("GNSS Accuracy: " + gnss_accuracy)
        dia1 = (int(gnss_utc_time[6:8], 16))
        mes1 = (int(gnss_utc_time[4:6], 16))
        ano1 = (int(gnss_utc_time[0:4], 16))
        hora1 = (int(gnss_utc_time[8:10], 16))
        min1 = (int(gnss_utc_time[10:12], 16))
        seg1 = (int(gnss_utc_time[12:14], 16))
        print("Speed: " + str(speed))
        print("Azimuth: " + azimuth)
        print("Altitude: " + altitude)
        print("Longitude: " + longitude)
        print("Latitude: " + latitude)
        print("GNSS UTC Time: " + gnss_utc_time)

        print("MCC: " + mcc)
        print("MNC: " + mnc)
        print("LAC: " + lac)
        print("Cell ID: " + cell_id)
        print("Current Mileage: " + str(current_mileage))
        print("Total Mileage: " + str(total_mileage))
        print("Current Hour Meter Count: " + str(current_hour_meter_count))
        print("Total Hour Meter Count: " + str(total_hour_meter_count))
        dia = str(int(send_time[6:8],16))
        mes = str(int(send_time[4:6],16))
        ano = str(int(send_time[0:4],16))
        hora = str(int(send_time[8:10],16))
        min = str(int(send_time[10:12],16))
        seg = str(int(send_time[12:14],16))
        print("Send Time: " + send_time + f" | {dia.zfill(2)}/{mes.zfill(2)}/{ano} | {hora.zfill(2)}:{min.zfill(2)}:"
                                          f"{seg.zfill(2)}")
    
        try:
            if ano1 == 0:
                print("Ignorando fix e seguindo o fluxo...")
                Time_fix = None 
            else:
                Time_fix = datetime(ano1, mes1, dia1, hora1, min1, seg1)
        except ValueError as e:
            print(f"Erro ao criar Time_fix: {e}")
            Time_fix = None  # Se houver erro, define como None e continua o fluxo
            



        if log_flag == 1:
            record_decoded(decoded_file_name, f"{dia.zfill(2)}/{mes.zfill(2)}/{ano},{hora.zfill(2)}:"
                                          f"{min.zfill(2)}:{seg.zfill(2)},{imei},0x{count_number},"
                                          f"{RSPMessageTypeList[int(message_type, 16)]},"
                                          f"0x{report_mask},{device_type},0x{protocol_version},0x{firmware_version},"
                                          f"{battery_level},{external_power_voltage},{analog_input_mode},"
                                          f"{analog_input1_voltage},{digital_input_status},{digital_output_status},"
                                          f"{motion_status},{satellites_in_use},-,"
                                          f"{gnss_accuracy},{speed},{azimuth},0x{altitude},"
                                          f"{latitude_final},{longitude_final},"
                                          f"{gnss_utc_time},{mcc},{mnc},{lac},{cell_id},0x{current_mileage},"
                                          f"0x{total_mileage},0x{current_hour_meter_count},0x{total_hour_meter_count},-,-,-,-,{Time_fix}")

    elif RSPMessageTypeList[int(message_type, 16)] == "GTFRI":
            report_mask = d[10:18]
            if report_mask == "00fe7fbf":  # Máscara genérica RSP e EVT
                print("Máscara compatível com 00fe7fbf")
            else:
                print("Máscara incompatível com 00fe7fbf")

            p = 22
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
            analog_input1_voltage = d[p:p + 4]
            p += 4
            digital_input_status = d[p:p + 2]
            p += 2
            digital_output_status = d[p:p + 2]
            p += 2
            motion_status = d[p:p + 2]
            p += 2
            satellites_in_use = int(d[p:p + 2], 16)
            p += 2
            report_id = d[p:p + 2]
            p += 2
            number = d[p:p + 2]
            p += 2
            gnss_accuracy = d[p:p + 2]
            p += 2
            speed_total = d[p:p + 6]
            p += 6
            speed_dec = int(speed_total[:4], 16)
            speed_frac = int(speed_total[4:], 16)
            speed = speed_dec + (speed_frac/10)
           
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
            send_time = d[p:p + 14]
            p += 14

            
            print("Report Mask: " + report_mask)
            #print("Device Type: " + device_type)
            #print("Protocol Version: " + protocol_version)
            #print("Firmware Version: " + firmware_version)
            imei = (str(int(unique_id1, 16)) + str(int(unique_id2, 16)) + str(int(unique_id3, 16)) +
                    str(int(unique_id4, 16)) + str(int(unique_id5, 16)) + str(int(unique_id6, 16)) +
                    str(int(unique_id7, 16)) + str(int(unique_id8, 16)))
            print("Unique ID: " + imei)
            print("Battery Level: ", battery_level)
            # print("External Power Voltage: ", external_power_voltage)
            print("Analog Input Mode: " + analog_input_mode)
            #print("Analog Input1 Voltage: " + analog_input1_voltage)  Não tem!
            print("Digital Input Status: " + digital_input_status)
            print("Digital Output Status: " + digital_output_status)
            print("Motion Status: " + motion_status)
            print("Satellites in Use: " +  str(satellites_in_use))
            print("Number: " + number)
            print("GNSS Accuracy: " + gnss_accuracy)
            print("Speed: " + str(speed))
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
            dia = str(int(send_time[6:8], 16))
            mes = str(int(send_time[4:6], 16))
            ano = str(int(send_time[0:4], 16))
            hora = str(int(send_time[8:10], 16))
            min = str(int(send_time[10:12], 16))
            seg = str(int(send_time[12:14], 16))
            print(
                "Send Time: " + send_time + f" | {dia.zfill(2)}/{mes.zfill(2)}/{ano} | {hora.zfill(2)}:{min.zfill(2)}:"
                                            f"{seg.zfill(2)}")
            

            diff = calcular_diferenca_tempo(send_time)
            diffON = None
            diffOFF = None

            motion_status_var = str(motion_status)  # Converte para string
            print(f"motion: ", motion_status_var)
            # Pegar apenas o primeiro caractere do motion_status
            motion_prefix = motion_status_var[0] if len(motion_status_var) > 0 else None

            diffON = diffON if diffON is not None else "-"
            diffOFF = diffOFF if diffOFF is not None else "-"

            if motion_prefix == "2":  
                diffON = diff  
                print(f"IGN: diferença de tempo: {diffON} segundos")

            elif motion_prefix == "1":  # Veículo desligado (IGF)
                diffOFF = diff
                print(f"IGF: diferença de tempo: {diffOFF} segundos")

          

            try:
                if ano1 == 0:
                    print("Ignorando fix e seguindo o fluxo...")
                    Time_fix = None 
                else:
                    Time_fix = datetime(ano1, mes1, dia1, hora1, min1, seg1)
            except ValueError as e:
                print(f"Erro ao criar Time_fix: {e}")
                Time_fix = None  # Se houver erro, define como None e continua o fluxo

            if log_flag == 1:
                record_decoded(decoded_file_name, f"{dia.zfill(2)}/{mes.zfill(2)}/{ano},{hora.zfill(2)}:"
                                              f"{min.zfill(2)}:{seg.zfill(2)},{imei},0x{count_number},"
                                              f"{RSPMessageTypeList[int(message_type, 16)]},"
                                              f"0x{report_mask},{device_type},0x{protocol_version},0x{firmware_version},"
                                              f"{battery_level},-,{analog_input_mode},-,"
                                              f"{digital_input_status},{digital_output_status},"
                                              f"{motion_status},{satellites_in_use},-,"
                                              f"{gnss_accuracy},{speed},{azimuth},0x{altitude},"
                                              f"{latitude_final},{longitude_final},"
                                              f"{gnss_utc_time},{mcc},{mnc},{lac},{cell_id},0x{current_mileage},"
                                              f"0x{total_mileage},0x{current_hour_meter_count},0x{total_hour_meter_count},-,-, {diffON}, {diffOFF}, {Time_fix} ")

        
    
    # elif RSPMessageTypeList[int(message_type, 16)] == 'GTERI':
    #     report_mask = d[10:18]
    #     print("Report Mask:", report_mask)

    #     if report_mask == "00fe7fbf":
    #             print("Máscara compatível com 00fe7fbf")
    #     else:
    #         print("Máscara incompatível com 00fe7fbf")
    #     eri_mask = d[18:26]
    #     p = 30
    #     device_type = d[p:p + 6]
    #     p += 6
    #     protocol_version = d[p:p + 4]
    #     p += 4
    #     firmware_version = d[p:p + 4]
    #     p += 4
    #     unique_id1 = d[p:p + 2]
    #     p += 2
    #     unique_id2 = d[p:p + 2]
    #     p += 2
    #     unique_id3 = d[p:p + 2]
    #     p += 2
    #     unique_id4 = d[p:p + 2]
    #     p += 2
    #     unique_id5 = d[p:p + 2]
    #     p += 2
    #     unique_id6 = d[p:p + 2]
    #     p += 2
    #     unique_id7 = d[p:p + 2]
    #     p += 2
    #     unique_id8 = d[p:p + 2]
    #     p += 2
    #     battery_level = int(d[p:p + 2], 16)
    #     p += 2
    #     external_power_voltage = int(d[p:p + 4], 16)
    #     p += 4
    #     analog_input_mode = d[p:p + 4]
    #     p += 4
    #     # analog_input1_voltage = d[p:p + 4]
    #     # p += 4
    #     digital_input_status = d[p:p + 2]
    #     p += 2
    #     digital_output_status = d[p:p + 2]
    #     p += 2
    #     motion_status = d[p:p + 2]
    #     p += 2
    #     satellites_in_use = int(d[p:p + 2], 16)
    #     p += 2
    #     report_id = d[p:p + 2]
    #     p += 2
    #     reserved = d[p:p + 2]
    #     p += 2
    #     onewire = d[p:p + 2]
    #     p += 2 
    #     ble = d[p:p + 2]
    #     p += 2
    #     rat = d[p:p + 2]
    #     p += 2 
    #     band = d[p:p + 4]
    #     p += 4
    #     IgnTrigger = d[p:p + 8]
    #     p += 8
    #     number = d[p:p + 2]
    #     p += 2
    #     gnss_accuracy = d[p:p + 2]
    #     p += 2
    #     speed_total = d[p:p + 6]
    #     p += 6
    #     speed_dec = int(speed_total[:4], 16)
    #     speed_frac = int(speed_total[4:], 16)
    #     speed = speed_dec + (speed_frac/10)
    #     azimuth = d[p:p + 4]
    #     p += 4
    #     altitude = d[p:p + 4]
    #     p += 4
    #     longitude = d[p:p + 8]
    #     if longitude == "00000000":
    #         longitude_final = "00000000"
    #     else:
    #         longitude_final = str((int(longitude, 16) - 4294967295) / 1e6)
    #     p += 8
    #     latitude = d[p:p + 8]
    #     if latitude == "00000000":
    #         latitude_final = "00000000"
    #     else:
    #         latitude_final = str((int(latitude, 16) - 4294967295) / 1e6)
    #     p += 8
    #     gnss_utc_time = d[p:p + 14]
    #     p += 14
    #     mcc = d[p:p + 4]
    #     p += 4
    #     mnc = d[p:p + 4]
    #     p += 4
    #     lac = d[p:p + 4]
    #     p += 4
    #     cell_id = d[p:p + 8]
    #     p += 8
    #     reserved = d[p:p + 2]
    #     p += 2
    #     current_mileage = d[p:p + 6]
    #     p += 6
    #     total_mileage = d[p:p + 10]
    #     p += 10
    #     current_hour_meter_count = d[p:p + 6]
    #     p += 6
    #     total_hour_meter_count = d[p:p + 12]
    #     p += 12
    #     RFID = d[p:p + 2]
    #     p += 2
    #     send_time = d[p:p + 14]
    #     p += 14

    #     print("mask eri: ", eri_mask)
    #     print("Report Mask: " + report_mask)
    #     print("Device Type: " + device_type)
    #     print("Protocol Version: " + protocol_version)
    #     print("Firmware Version: " + firmware_version)
    #     imei = (str(int(unique_id1, 16)) + str(int(unique_id2, 16)) + str(int(unique_id3, 16)) +
    #             str(int(unique_id4, 16)) + str(int(unique_id5, 16)) + str(int(unique_id6, 16)) +
    #             str(int(unique_id7, 16)) + str(int(unique_id8, 16)))
    #     print("Unique ID: " + imei)
    #     print("Battery Level: ", battery_level)
    #     print("External Power Voltage: ", external_power_voltage)
    #     print("Analog Input Mode: " + analog_input_mode)
    #     # print("Analog Input1 Voltage: " + analog_input1_voltage)  
    #     print("Digital Input Status: " + digital_input_status)
    #     print("Digital Output Status: " + digital_output_status)
    #     print("Motion Status: " + motion_status)
    #     print("Satellites in Use: " + str(satellites_in_use))
    #     print("Report type: ", report_id)
    #     print("reserved: ", reserved)
    #     print("1wire: ", onewire)
    #     print("Bluetooth Accessory Number: ", ble)
    #     print("RAT: ", rat)
    #     print("band: ", band)
    #     print("IGN trigger: ", IgnTrigger)
    #     print("Number: " + number)
    #     print("GNSS Accuracy: " + gnss_accuracy)
    #     print("Speed: " + str(speed))
    #     print("Azimuth: " + azimuth)
    #     print("Altitude: " + altitude)
    #     print("Longitude: " + longitude_final)
    #     print("Latitude: " + latitude_final)
    #     print("GNSS UTC Time: " + gnss_utc_time)
    #     dia1 = (int(gnss_utc_time[6:8], 16))
    #     mes1 = (int(gnss_utc_time[4:6], 16))
    #     ano1 = (int(gnss_utc_time[0:4], 16))
    #     hora1 = (int(gnss_utc_time[8:10], 16))
    #     min1 = (int(gnss_utc_time[10:12], 16))
    #     seg1 = (int(gnss_utc_time[12:14], 16))
    #     # seg_fix = (int(gnss_utc_time[12:14]))
    #     # print(
    #     #     "Time fix: " + gnss_utc_time + f" | {dia.zfill(2)}/{mes.zfill(2)}/{ano} | {hora.zfill(2)}:{min.zfill(2)}:"
    #     #                                 f"{seg.zfill(2)}")
    #     print("MCC: " + mcc)
    #     print("MNC: " + mnc)
    #     print("LAC: " + lac)
    #     print("Cell ID: " + cell_id)
    #     print("Current Mileage: " + current_mileage)
    #     print("Total Mileage: " + total_mileage)
    #     print("Current Hour Meter Count: " + current_hour_meter_count)
    #     print("Total Hour Meter Count: " + total_hour_meter_count)
    #     print("RFID: ",RFID)
    #     dia = str(int(send_time[6:8], 16))
    #     mes = str(int(send_time[4:6], 16))
    #     ano = str(int(send_time[0:4], 16))
    #     hora = str(int(send_time[8:10], 16))
    #     min = str(int(send_time[10:12], 16))
    #     seg = str(int(send_time[12:14], 16))
    #     print(
    #         "Send Time: " + send_time + f" | {dia.zfill(2)}/{mes.zfill(2)}/{ano} | {hora.zfill(2)}:{min.zfill(2)}:"
    #                                     f"{seg.zfill(2)}")
        

    #     diff = calcular_diferenca_tempo(send_time)
    #     diffON = None
    #     diffOFF = None

    #     motion_status_var = str(motion_status)  # Converte para string
    #     print(f"motion: ", motion_status_var)
    #     # Pegar apenas o primeiro caractere do motion_status
    #     motion_prefix = motion_status_var[0] if len(motion_status_var) > 0 else None

    #     diffON = diffON if diffON is not None else "-"
    #     diffOFF = diffOFF if diffOFF is not None else "-"

    #     if motion_prefix == "2":  
    #         diffON = diff  
    #         print(f"IGN: diferença de tempo: {diffON} segundos")

    #     elif motion_prefix == "1":  # 9Veículo desligado (IGF)
    #         diffOFF = diff
    #         print(f"IGF: diferença de tempo: {diffOFF} segundos")

        

    #     try:
    #         if ano1 == 0:
    #             print("Ignorando fix e seguindo o fluxo...")
    #             Time_fix = None 
    #         else:
    #             Time_fix = datetime(ano1, mes1, dia1, hora1, min1, seg1)
    #     except ValueError as e:
    #         print(f"Erro ao criar Time_fix: {e}")
    #         Time_fix = None  # Se houver erro, define como None e continua o fluxo

    #     if log_flag == 1:
    #         record_decoded(decoded_file_name, f"{dia.zfill(2)}/{mes.zfill(2)}/{ano},{hora.zfill(2)}:"
    #                                         f"{min.zfill(2)}:{seg.zfill(2)},{imei},0x{count_number},"
    #                                         f"{RSPMessageTypeList[int(message_type, 16)]},"
    #                                         f"0x{report_mask},{device_type},0x{protocol_version},0x{firmware_version},"
    #                                         f"{battery_level},{external_power_voltage },{analog_input_mode},-,"
    #                                         f"{digital_input_status},{digital_output_status},"
    #                                         f"{motion_status},{satellites_in_use},-,-,"
    #                                         f"{gnss_accuracy},{speed},{azimuth},0x{altitude},"
    #                                         f"{latitude_final},{longitude_final},"
    #                                         f"{gnss_utc_time},{mcc},{mnc},{lac},{cell_id},0x{current_mileage},"
    #                                         f"0x{total_mileage},0x{current_hour_meter_count},0x{total_hour_meter_count},-,-, {diffON}, {diffOFF}, {Time_fix} ")
            

    elif RSPMessageTypeList[int(message_type, 16)] == 'GTERI':
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
        # analog_input1_voltage = d[p:p + 4]
        # p += 4
        digital_input_status = d[p:p + 2]
        p += 2
        digital_output_status = d[p:p + 2]
        p += 2
        motion_status = d[p:p + 2]
        p += 2
        satellites_in_use = int(d[p:p + 2], 16)
        p += 2
        report_id = d[p:p + 2]
        p += 2
        reserved = d[p:p + 2]
        p += 2
        onewire = d[p:p + 2]
        p += 2 
        ble = d[p:p + 2]
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
        speed_total = d[p:p + 6]
        p += 6
        speed_dec = int(speed_total[:4], 16)
        speed_frac = int(speed_total[4:], 16)
        speed = speed_dec + (speed_frac/10)
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
        current_mileage1 = int(d[p:p + 4], 16)
        p += 4
        current_mileage2 = int(d[p:p + 2], 16)
        p += 2
        current_mileage = current_mileage1 + (current_mileage2 / 10)
        total_mileage1 = int(d[p:p + 8], 16)
        p += 8
        total_mileage2 = int(d[p:p + 2], 16)
        p += 2
        total_mileage = total_mileage1 + (total_mileage2 / 10)
        current_hour_meter_count_hh = str(int(d[p:p + 2], 16))
        p += 2
        current_hour_meter_count_mm = str(int(d[p:p + 2], 16))
        p += 2
        current_hour_meter_count_ss = str(int(d[p:p + 2], 16))
        p += 2
        current_hour_meter_count = (f"{current_hour_meter_count_hh}:{current_hour_meter_count_mm.zfill(2)}:"
                                    f"{current_hour_meter_count_ss.zfill(2)}")
        total_hour_meter_count_hh = str(int(d[p:p + 8], 16))
        p += 8
        total_hour_meter_count_mm = str(int(d[p:p + 2], 16))
        p += 2
        total_hour_meter_count_ss = str(int(d[p:p + 2], 16))
        p += 2
        total_hour_meter_count = (f"{total_hour_meter_count_hh}:{total_hour_meter_count_mm.zfill(2)}:"
                                    f"{total_hour_meter_count_ss.zfill(2)}")

        id_length = d[p:p + 2]
        p += 2
        if int(id_length, 16) != 0:
            id = d[p:p + (int(id_length, 16) * 2)]
            p += int(id_length, 16) * 2
        else:
            id = "0"
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
        # print("Analog Input1 Voltage: " + analog_input1_voltage)  
        print("Digital Input Status: " + digital_input_status)
        print("Digital Output Status: " + digital_output_status)
        print("Motion Status: " + motion_status)
        print("Satellites in Use: " + str(satellites_in_use))
        print("Report type: ", report_id)
        print("reserved: ", reserved)
        print("1wire: ", onewire)
        print("Bluetooth Accessory Number: ", ble)
        print("RAT: ", rat)
        print("band: ", band)
        print("IGN trigger: ", IgnTrigger)
        print("Number: " + number)
        print("GNSS Accuracy: " + gnss_accuracy)
        print("Speed: " + str(speed))
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
        #     "Time fix: " + gnss_utc_time + f" | {dia1.zfill(2)}/{mes1.zfill(2)}/{ano1} | {hora1.zfill(2)}:{min1.zfill(2)}:"
        #                                 f"{seg.zfill(2)}")
        print("MCC: " + mcc)
        print("MNC: " + mnc)
        print("LAC: " + lac)
        print("Cell ID: " + cell_id)
        print("Current Mileage: " + str(current_mileage))
        print("Total Mileage: " + str(total_mileage))
        print("Current Hour Meter Count: " + current_hour_meter_count)
        print("Total Hour Meter Count: " + str(total_hour_meter_count))
        print("RFID: ", id)
        dia = str(int(send_time[6:8], 16))
        mes = str(int(send_time[4:6], 16))
        ano = str(int(send_time[0:4], 16))
        hora = str(int(send_time[8:10], 16))
        min = str(int(send_time[10:12], 16))
        seg = str(int(send_time[12:14], 16))
        print(
            "Send Time: " + send_time + f" | {dia.zfill(2)}/{mes.zfill(2)}/{ano} | {hora.zfill(2)}:{min.zfill(2)}:"
                                        f"{seg.zfill(2)}")
    

        diff = calcular_diferenca_tempo(send_time)
        diffON = None
        diffOFF = None

        try:
            if ano1 == 0:
                print("Ignorando fix e seguindo o fluxo...")
                Time_fix = None 
            else:
                Time_fix = datetime(ano1, mes1, dia1, hora1, min1, seg1)
        except ValueError as e:
            print(f"Erro ao criar Time_fix: {e}")
            Time_fix = None  # Se houver erro, define como None e continua o fluxo
            motion_status_var = str(motion_status)  # Converte para string
            print(f"motion: ", motion_status_var)
            # Pegar apenas o primeiro caractere do motion_status
            motion_prefix = motion_status_var[0] if len(motion_status_var) > 0 else None

            diffON = diffON if diffON is not None else "-"
            diffOFF = diffOFF if diffOFF is not None else "-"

            if motion_prefix == "2":  
                diffON = diff  
                print(f"IGN: diferença de tempo: {diffON} segundos")

            elif motion_prefix == "1":  # Veículo desligado (IGF)
                diffOFF = diff
                print(f"IGF: diferença de tempo: {diffOFF} segundos")
    
        if log_flag == 1:
            record_decoded(decoded_file_name, f"{dia.zfill(2)}/{mes.zfill(2)}/{ano},{hora.zfill(2)}:"
                                        f"{min.zfill(2)}:{seg.zfill(2)},{imei},0x{count_number},"
                                        f"{RSPMessageTypeList[int(message_type, 16)]},"
                                        f"0x{report_mask},{device_type},0x{protocol_version},0x{firmware_version},"
                                        f"{battery_level},{external_power_voltage },{analog_input_mode},-,"
                                        f"{digital_input_status},{digital_output_status},"
                                        f"{motion_status},{satellites_in_use},-,-,"
                                        f"{gnss_accuracy},{speed},{azimuth},0x{altitude},"
                                        f"{latitude_final},{longitude_final},"
                                        f"{gnss_utc_time},{mcc},{mnc},{lac},{cell_id},0x{current_mileage},"
                                        f"0x{total_mileage},0x{current_hour_meter_count},0x{total_hour_meter_count},-,-, {diffON}, {diffOFF}, {Time_fix}")



    elif RSPMessageTypeList[int(message_type, 16)] == "GTDOG":
        report_mask = d[10:18]
        if report_mask == "00fe7fbf":  # Máscara genérica RSP e EVT
            print("Máscara compatível com 00fe7fbf")
        else:
            print("Máscara incompatível com 00fe7fbf")
        # print("esta aqui")
        p = 22
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
        analog_input1_voltage = d[p:p + 4]
        p += 4
        digital_input_status = d[p:p + 2]
        p += 2
        digital_output_status = d[p:p + 2]
        p += 2
        motion_status = d[p:p + 2]
        p += 2
        satellites_in_use = int(d[p:p + 2], 16)
        p += 2
        report_id = d[p:p + 2]
        p += 2
        number = d[p:p + 2]
        p += 2
        gnss_accuracy = d[p:p + 2]
        p += 2
        speed_total = d[p:p + 6]
        p += 6
        speed_dec = int(speed_total[:4], 16)
        speed_frac = int(speed_total[4:], 16)
        speed = speed_dec + (speed_frac/10)
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
        print("Analog Input1 Voltage: " + analog_input1_voltage) 
        print("Digital Input Status: " + digital_input_status)
        print("Digital Output Status: " + digital_output_status)
        print("Motion Status: " + motion_status)
        print("Report type " + report_id)
        print("Satellites in Use: " + str(satellites_in_use))
        print("Number: " + number)
        print("GNSS Accuracy: " + gnss_accuracy)
        print("Speed: " + str(speed))
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
        dia = str(int(send_time[6:8], 16))
        mes = str(int(send_time[4:6], 16))
        ano = str(int(send_time[0:4], 16))
        hora = str(int(send_time[8:10], 16))
        min = str(int(send_time[10:12], 16))
        seg = str(int(send_time[12:14], 16))
        print(
            "Send Time: " + send_time + f" | {dia.zfill(2)}/{mes.zfill(2)}/{ano} | {hora.zfill(2)}:{min.zfill(2)}:"
                                        f"{seg.zfill(2)}")
        

              

       

        if log_flag == 1:
            record_decoded(decoded_file_name, f"{dia.zfill(2)}/{mes.zfill(2)}/{ano},{hora.zfill(2)}:"
                                            f"{min.zfill(2)}:{seg.zfill(2)},{imei},0x{count_number},"
                                            f"{RSPMessageTypeList[int(message_type, 16)]},"
                                            f"0x{report_mask},{device_type},0x{protocol_version},0x{firmware_version},"
                                            f"{battery_level},{external_power_voltage },{analog_input_mode},-,"
                                            f"{digital_input_status},{digital_output_status},"
                                            f"{motion_status},{satellites_in_use},{report_id},-,"
                                            f"{gnss_accuracy},{speed},{azimuth},0x{altitude},"
                                            f"{latitude_final},{longitude_final},"
                                            f"{gnss_utc_time},{mcc},{mnc},{lac},{cell_id},0x{current_mileage},"
                                            f"0x{total_mileage},0x{current_hour_meter_count},0x{total_hour_meter_count},-,-, -,-,- ")
        

    else:
            if log_flag == 1:
                record_decoded(decoded_file_name,",,,," + RSPMessageTypeList[int(message_type, 16)])                
    return msg