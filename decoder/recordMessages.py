import datetime

def record_raw(file_name, source, msg):
    curr_time = datetime.datetime.now()
    date_time = curr_time.strftime("%d/%m/%Y,%H:%M:%S,")
    with open(file_name, "a+") as f:
        f.write(date_time + source + ',' + msg + "\n")
        f.close()

def record_decoded(file_name, msg):
    with open(file_name, "a+") as f:
        curr_time = datetime.datetime.now()
        date_time = curr_time.strftime("%d/%m/%Y,%H:%M:%S,")
        f.write(date_time + msg + "\n")
        f.close()

