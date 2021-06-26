from time import time
import socket
import json
import base64
import logging
from multiprocessing import Process, Pool

server_address = ('127.0.0.1', 6666)

def sendCommand(command_str = ""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"Connecting to {server_address}")

    try:
        logging.warning(f"Sending message ")
        sock.sendall(command_str.encode())
        data_received = ""
        while True:
            data = sock.recv(16)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break

        result = json.loads(data_received)
        logging.warning("Data received from server: ")
        return result
    except:
        logging.warning("Error during receiving data")
        return False

def remoteList():
    command_str = f"LIST"
    result = sendCommand(command_str)
    if result['status'] == 'OK':
        print("List of files: ")
        for file in result['data']:
            print(f"- {file}")
        return True
    else:
        print("Failed")
        return False

def remoteGet(filename="", count=1):
    awal = time()
    command_str = f"GET {filename}"
    result = sendCommand(command_str)
    if result['status'] == 'OK':
        filename = result['data_nama'] + str(count) + "." + result['data_ext'];
        content = base64.b64decode(result['data_file'])
        fp = open(filename, 'wb+')
        fp.write(content)
        fp.close()
        akhir = time()
        logging.warning(f"Getting {filename} in {akhir-awal}")
        return True
    else:
        print("Gagal")
        return False

if __name__ == '__main__':
    files = dict()

    for i in range(100):
        tp = str(int(i))
        files[tp] = str("pokijan.jpg")

    texec = dict()
    status_task = dict()
    task_pool = Pool(processes=100)

    begin = time()
    count = 1

    for k in files:
        print(f"Getting {files[k]}")
        texec[k] = task_pool.apply_async(func=remoteGet, args=(files[k],count,))
        count += 1

    for k in files:
        status_task[k] = texec[k].get(timeout=10)

    end = time()
    duration = end - begin
    print(f"Total time required to request 100 files of pokijan.jpg is {duration} seconds")


