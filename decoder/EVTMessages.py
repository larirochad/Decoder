from recordMessages import *

import global_state

# Message Type List
EVTMessageTypeList = [""] * 89
EVTMessageTypeList.insert(1,"GTPNA")
EVTMessageTypeList.insert(2,"GTPFA")
EVTMessageTypeList.insert(3,"GTMPN")
EVTMessageTypeList.insert(4,"GTMPF")
EVTMessageTypeList.insert(6,"GTBPL")
EVTMessageTypeList.insert(7,"GTBTC")
EVTMessageTypeList.insert(8,"GTSTC")
EVTMessageTypeList.insert(9,"GTSTT")
EVTMessageTypeList.insert(12,"GTPDP")
EVTMessageTypeList.insert(13,"GTIGN")
EVTMessageTypeList.insert(14,"GTIGF")
EVTMessageTypeList.insert(15,"GTUPD")
EVTMessageTypeList.insert(16,"GTIDN")
EVTMessageTypeList.insert(17,"GTIDF")
EVTMessageTypeList.insert(18,"GTDAT")
EVTMessageTypeList.insert(20,"GTJDR")
EVTMessageTypeList.insert(21,"GTGSS")
EVTMessageTypeList.insert(23,"GTSTR")
EVTMessageTypeList.insert(24,"GTSTP")
EVTMessageTypeList.insert(25,"GTCRA")
EVTMessageTypeList.insert(27,"GTDOS")
EVTMessageTypeList.insert(28,"GTGES")
EVTMessageTypeList.insert(29,"GTLSP")
EVTMessageTypeList.insert(30,"GTTMP")
EVTMessageTypeList.insert(32,"GTJDS")
EVTMessageTypeList.insert(33,"GTRMD")
EVTMessageTypeList.insert(40,"GTUPC")
EVTMessageTypeList.insert(41,"GTCLT")
EVTMessageTypeList.insert(42,"GTCFU")
EVTMessageTypeList.insert(45,"GTVGN")
EVTMessageTypeList.insert(46,"GTVGF")
EVTMessageTypeList.insert(47,"GTASC")
EVTMessageTypeList.insert(48,"GTPNR")
EVTMessageTypeList.insert(49,"GTPFR")
EVTMessageTypeList.insert(51,"GTHBE")
EVTMessageTypeList.insert(52,"GTBCS")
EVTMessageTypeList.insert(53,"GTBDS")
EVTMessageTypeList.insert(65,"GTBAA")
EVTMessageTypeList.insert(67,"GTBID")
EVTMessageTypeList.insert(70,"GTBAR")
EVTMessageTypeList.insert(73,"GTSVR")
EVTMessageTypeList.insert(84,"GTEUC")
EVTMessageTypeList.insert(86,"GTRTP")
EVTMessageTypeList.insert(88,"GTHUM")

evtGenericEventGroup = ["GTPNA","GTPFA","GTMPN","GTMPF","GTBTC","GTSTC","GTSTT","GTPDP","GTIDN","GTSTR","GTSTP","GTLSP"]



def parse_evt_message(d,decoded_file_name,log_flag):
    print("Group: Event Report")
    size = len(d)
    message_type = d[8:10]
    count_number = d[size - 12:(size - 8) - size]
    print("Message Type: " + message_type + " -> " + EVTMessageTypeList[int(message_type, 16)])
    msg = "+SACK:" + count_number + "$"


    if EVTMessageTypeList[int(message_type, 16)] in evtGenericEventGroup:
        print("Formato Genérico")
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
        satellites_in_use = d[p:p + 2]
        p += 2
        #report_id = d[p:p + 2]
        #p += 2
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
        print("External Power Voltage: ", external_power_voltage)
        #print("Analog Input Mode: " + analog_input_mode)
        #print("Analog Input1 Voltage: " + analog_input1_voltage)
        #print("Digital Input Status: " + digital_input_status)
        #print("Digital Output Status: " + digital_output_status)
        #print("Motion Status: " + motion_status)
        #print("Satellites in Use: " + satellites_in_use)
        #print("Number: " + number)
        #print("GNSS Accuracy: " + gnss_accuracy)
        #print("Speed: " + speed)
        #print("Azimuth: " + azimuth)
        #print("Altitude: " + altitude)
        #print("Longitude: " + longitude)
        #print("Latitude: " + latitude)
        #print("GNSS UTC Time: " + gnss_utc_time)
        #print("MCC: " + mcc)
        #print("MNC: " + mnc)
        #print("LAC: " + lac)
        #print("Cell ID: " + cell_id)
        #print("Current Mileage: " + current_mileage)
        #print("Total Mileage: " + total_mileage)
        #print("Current Hour Meter Count: " + current_hour_meter_count)
        #print("Total Hour Meter Count: " + total_hour_meter_count)
        dia = str(int(send_time[6:8], 16))
        mes = str(int(send_time[4:6], 16))
        ano = str(int(send_time[0:4], 16))
        hora = str(int(send_time[8:10], 16))
        min = str(int(send_time[10:12], 16))
        seg = str(int(send_time[12:14], 16))
        print("Send Time: " + send_time + f" | {dia.zfill(2)}/{mes.zfill(2)}/{ano} | {hora.zfill(2)}:{min.zfill(2)}:"
                                          f"{seg.zfill(2)}")

        if log_flag == 1:
            record_decoded(decoded_file_name, f"{dia.zfill(2)}/{mes.zfill(2)}/{ano},{hora.zfill(2)}:"
                                          f"{min.zfill(2)}:{seg.zfill(2)},{imei},0x{count_number},"
                                          f"{EVTMessageTypeList[int(message_type, 16)]},"
                                          f"0x{report_mask},{device_type},0x{protocol_version},0x{firmware_version},"
                                          f"{battery_level},{external_power_voltage},{analog_input_mode},"
                                          f"{analog_input1_voltage},{digital_input_status},{digital_output_status},"
                                          f"{motion_status},{satellites_in_use},-,"
                                          f"{gnss_accuracy},{speed},{azimuth},0x{altitude},"
                                          f"{latitude_final},{longitude_final},"
                                          f"{gnss_utc_time},{mcc},{mnc},{lac},{cell_id},0x{current_mileage},"
                                          f"0x{total_mileage},0x{current_hour_meter_count},0x{total_hour_meter_count},-,-")
    else:############################################################
        print("Formato Específico")
        if EVTMessageTypeList[int(message_type, 16)] == "GTIGN" or EVTMessageTypeList[int(message_type, 16)] == "GTIGF":
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
            battery_level = int(d[p:p + 2], 16) # ja faz a conversão para dec
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
            satellites_in_use = d[p:p + 2]
            p += 2
            duration_of_ignition = str(int(d[p:p+8],16)) #segundos
            p+=8
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
            send_time = d[p:p + 14]
            p += 14

            print("Report Mask: " + report_mask)
            # print("Device Type: " + device_type)
            # print("Protocol Version: " + protocol_version)
            # print("Firmware Version: " + firmware_version)
            imei = (str(int(unique_id1, 16)) + str(int(unique_id2, 16)) + str(int(unique_id3, 16)) +
                    str(int(unique_id4, 16)) + str(int(unique_id5, 16)) + str(int(unique_id6, 16)) +
                    str(int(unique_id7, 16)) + str(int(unique_id8, 16)))
            print("Unique ID: " + imei)
            print("Battery Level: ", battery_level)
            print("External Power Voltage: ", external_power_voltage/1000.0)
            print("Analog Input Mode: " + analog_input_mode)
            print("Analog Input1 Voltage: " + analog_input1_voltage)
            print("Digital Input Status: " + digital_input_status)
            print("Digital Output Status: " + digital_output_status)
            print("Motion Status: " + motion_status)
            print("Satellites in Use: " + satellites_in_use)
            print("Duration of Ignition: " + duration_of_ignition)
            print("Number: " + number)
            print("GNSS Accuracy: " + gnss_accuracy)
            print("Speed: " + speed)
            print("Azimuth: " + azimuth)
            print("Altitude: " + altitude)
            print("Longitude: " + str(int(longitude,16)))
            print("Latitude: " + str(int(latitude,16)))
            print("GNSS UTC Time: " + gnss_utc_time)
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
                                              f"{EVTMessageTypeList[int(message_type, 16)]},"
                                              f"0x{report_mask},{device_type},0x{protocol_version},0x{firmware_version},"
                                              f"{battery_level},{external_power_voltage},{analog_input_mode},"
                                              f"{analog_input1_voltage},{digital_input_status},{digital_output_status},"
                                              f"{motion_status},{satellites_in_use},{duration_of_ignition},"
                                              f"{gnss_accuracy},{speed},{azimuth},0x{altitude},"
                                              f"{latitude_final},{longitude_final},"
                                              f"{gnss_utc_time},{mcc},{mnc},{lac},{cell_id},0x{current_mileage},"
                                              f"0x{total_mileage},0x{current_hour_meter_count},0x{total_hour_meter_count},-,-")

        elif EVTMessageTypeList[int(message_type, 16)] == "GTVGN" or EVTMessageTypeList[int(message_type, 16)] == "GTVGF":
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
            satellites_in_use = d[p:p + 2]
            p += 2
            reserved = d[p:p+2]
            p+=2
            report_type = d[p:p+2]
            p+=2
            duration_of_ignition = d[p:p+8]
            p+=8
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
            send_time = d[p:p + 14]
            p += 14

            print("Report Mask: " + report_mask)
            # print("Device Type: " + device_type)
            # print("Protocol Version: " + protocol_version)
            # print("Firmware Version: " + firmware_version)
            imei = (str(int(unique_id1, 16)) + str(int(unique_id2, 16)) + str(int(unique_id3, 16)) +
                    str(int(unique_id4, 16)) + str(int(unique_id5, 16)) + str(int(unique_id6, 16)) +
                    str(int(unique_id7, 16)) + str(int(unique_id8, 16)))
            print("Unique ID: " + imei)
            print("Battery Level: ", battery_level)
            print("External Power Voltage: ", external_power_voltage)
            # print("Analog Input Mode: " + analog_input_mode)
            # print("Analog Input1 Voltage: " + analog_input1_voltage)
            # print("Digital Input Status: " + digital_input_status)
            # print("Digital Output Status: " + digital_output_status)
            # print("Motion Status: " + motion_status)
            # print("Satellites in Use: " + satellites_in_use)
            print("Duration of Ignition: " + duration_of_ignition)
            # print("Number: " + number)
            # print("GNSS Accuracy: " + gnss_accuracy)
            # print("Speed: " + speed)
            # print("Azimuth: " + azimuth)
            # print("Altitude: " + altitude)
            # print("Longitude: " + longitude)
            # print("Latitude: " + latitude)
            # print("GNSS UTC Time: " + gnss_utc_time)
            # print("MCC: " + mcc)
            # print("MNC: " + mnc)
            # print("LAC: " + lac)
            # print("Cell ID: " + cell_id)
            # print("Current Mileage: " + current_mileage)
            # print("Total Mileage: " + total_mileage)
            # print("Current Hour Meter Count: " + current_hour_meter_count)
            # print("Total Hour Meter Count: " + total_hour_meter_count)
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
                                              f"{EVTMessageTypeList[int(message_type, 16)]},"
                                              f"0x{report_mask},{device_type},0x{protocol_version},0x{firmware_version},"
                                              f"{battery_level},{external_power_voltage},{analog_input_mode},"
                                              f"{analog_input1_voltage},{digital_input_status},{digital_output_status},"
                                              f"{motion_status},{satellites_in_use},{duration_of_ignition},"
                                              f"{gnss_accuracy},{speed},{azimuth},0x{altitude},"
                                              f"{latitude_final},{longitude_final},"
                                              f"{gnss_utc_time},{mcc},{mnc},{lac},{cell_id},0x{current_mileage},"
                                              f"0x{total_mileage},0x{current_hour_meter_count},0x{total_hour_meter_count},-,-")

        elif EVTMessageTypeList[int(message_type, 16)] == "GTPFR":
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
            satellites_in_use = d[p:p + 2]
            p += 2
            power_off_reason = d[p:p + 2]
            p += 2
            #report_type = d[p:p + 2]
            #p += 2
            #duration_of_ignition = d[p:p + 8]
            #p += 8
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
            send_time = d[p:p + 14]
            p += 14

            print("Report Mask: " + report_mask)
            # print("Device Type: " + device_type)
            # print("Protocol Version: " + protocol_version)
            # print("Firmware Version: " + firmware_version)
            imei = (str(int(unique_id1, 16)) + str(int(unique_id2, 16)) + str(int(unique_id3, 16)) +
                    str(int(unique_id4, 16)) + str(int(unique_id5, 16)) + str(int(unique_id6, 16)) +
                    str(int(unique_id7, 16)) + str(int(unique_id8, 16)))
            print("Unique ID: " + imei)
            print("Battery Level: ", battery_level)
            print("External Power Voltage: ", external_power_voltage)
            # print("Analog Input Mode: " + analog_input_mode)
            # print("Analog Input1 Voltage: " + analog_input1_voltage)
            # print("Digital Input Status: " + digital_input_status)
            # print("Digital Output Status: " + digital_output_status)
            # print("Motion Status: " + motion_status)
            # print("Satellites in Use: " + satellites_in_use)
            #print("Duration of Ignition: " + duration_of_ignition)
            # print("Number: " + number)
            # print("GNSS Accuracy: " + gnss_accuracy)
            # print("Speed: " + speed)
            # print("Azimuth: " + azimuth)
            # print("Altitude: " + altitude)
            # print("Longitude: " + longitude)
            # print("Latitude: " + latitude)
            # print("GNSS UTC Time: " + gnss_utc_time)
            # print("MCC: " + mcc)
            # print("MNC: " + mnc)
            # print("LAC: " + lac)
            # print("Cell ID: " + cell_id)
            # print("Current Mileage: " + current_mileage)
            # print("Total Mileage: " + total_mileage)
            # print("Current Hour Meter Count: " + current_hour_meter_count)
            # print("Total Hour Meter Count: " + total_hour_meter_count)
            print("Power Off Reason: " + power_off_reason)
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
                                              f"{EVTMessageTypeList[int(message_type, 16)]},"
                                              f"0x{report_mask},{device_type},0x{protocol_version},0x{firmware_version},"
                                              f"{battery_level},{external_power_voltage},{analog_input_mode},"
                                              f"{analog_input1_voltage},{digital_input_status},{digital_output_status},"
                                              f"{motion_status},{satellites_in_use},-,"
                                              f"{gnss_accuracy},{speed},{azimuth},0x{altitude},"
                                              f"{latitude_final},{longitude_final},"
                                              f"{gnss_utc_time},{mcc},{mnc},{lac},{cell_id},0x{current_mileage},"
                                              f"0x{total_mileage},0x{current_hour_meter_count},0x{total_hour_meter_count},"
                                              f"{power_off_reason},-")

        elif EVTMessageTypeList[int(message_type, 16)] == "GTPNR":
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
            satellites_in_use = d[p:p + 2]
            p += 2
            power_on_reason = d[p:p + 2]
            p += 2
            #report_type = d[p:p + 2]
            #p += 2
            #duration_of_ignition = d[p:p + 8]
            #p += 8
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
            send_time = d[p:p + 14]
            p += 14

            print("Report Mask: " + report_mask)
            # print("Device Type: " + device_type)
            # print("Protocol Version: " + protocol_version)
            # print("Firmware Version: " + firmware_version)
            imei = (str(int(unique_id1, 16)) + str(int(unique_id2, 16)) + str(int(unique_id3, 16)) +
                    str(int(unique_id4, 16)) + str(int(unique_id5, 16)) + str(int(unique_id6, 16)) +
                    str(int(unique_id7, 16)) + str(int(unique_id8, 16)))
            print("Unique ID: " + imei)
            print("Battery Level: ", battery_level)
            print("External Power Voltage: ", external_power_voltage)
            # print("Analog Input Mode: " + analog_input_mode)
            # print("Analog Input1 Voltage: " + analog_input1_voltage)
            # print("Digital Input Status: " + digital_input_status)
            # print("Digital Output Status: " + digital_output_status)
            # print("Motion Status: " + motion_status)
            # print("Satellites in Use: " + satellites_in_use)
            #print("Duration of Ignition: " + duration_of_ignition)
            # print("Number: " + number)
            # print("GNSS Accuracy: " + gnss_accuracy)
            # print("Speed: " + speed)
            # print("Azimuth: " + azimuth)
            # print("Altitude: " + altitude)
            # print("Longitude: " + longitude)
            # print("Latitude: " + latitude)
            # print("GNSS UTC Time: " + gnss_utc_time)
            # print("MCC: " + mcc)
            # print("MNC: " + mnc)
            # print("LAC: " + lac)
            # print("Cell ID: " + cell_id)
            # print("Current Mileage: " + current_mileage)
            # print("Total Mileage: " + total_mileage)
            # print("Current Hour Meter Count: " + current_hour_meter_count)
            # print("Total Hour Meter Count: " + total_hour_meter_count)
            print("Power On Reason: " + power_on_reason)
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
                                              f"{EVTMessageTypeList[int(message_type, 16)]},"
                                              f"0x{report_mask},{device_type},0x{protocol_version},0x{firmware_version},"
                                              f"{battery_level},{external_power_voltage},{analog_input_mode},"
                                              f"{analog_input1_voltage},{digital_input_status},{digital_output_status},"
                                              f"{motion_status},{satellites_in_use},-,"
                                              f"{gnss_accuracy},{speed},{azimuth},0x{altitude},"
                                              f"{latitude_final},{longitude_final},"
                                              f"{gnss_utc_time},{mcc},{mnc},{lac},{cell_id},0x{current_mileage},"
                                              f"0x{total_mileage},0x{current_hour_meter_count},0x{total_hour_meter_count},"
                                              f"-,{power_on_reason}")

        else:
            if log_flag == 1:
                record_decoded(decoded_file_name,",,,," + EVTMessageTypeList[int(message_type, 16)])
    return msg