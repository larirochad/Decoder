from recordMessages import *
# Message Type List
INFMessageTypeList = [""] * 40
INFMessageTypeList.insert(1,"GTINF")
INFMessageTypeList.insert(2,"GTGPS")
INFMessageTypeList.insert(4,"GTCID")
INFMessageTypeList.insert(5,"GTCSQ")
INFMessageTypeList.insert(6,"GTVER")
INFMessageTypeList.insert(7,"GTBAT")
INFMessageTypeList.insert(8,"GTIOS")
INFMessageTypeList.insert(9,"GTTMZ")
INFMessageTypeList.insert(10,"GTGSM")
INFMessageTypeList.insert(11,"GTGSV")
INFMessageTypeList.insert(13,"GTCVN")
INFMessageTypeList.insert(20,"GTCSN")
INFMessageTypeList.insert(24,"GTBTI")
INFMessageTypeList.insert(26,"GTCML")
INFMessageTypeList.insert(28,"GTSCS")
INFMessageTypeList.insert(39,"GTESQ")

def parse_inf_message(d,decoded_file_name,log_flag):
    print("Group: Device Information Report")
    size = len(d)
    message_type = d[8:10]
    count_number = d[size - 12:(size - 8) - size]
    print("Message Type: " + message_type + " -> " + INFMessageTypeList[int(message_type, 16)])
    msg = "+SACK:" + count_number + "$"
    if log_flag == 1:
        record_decoded(decoded_file_name,",,,," + INFMessageTypeList[int(message_type, 16)])
    return msg

