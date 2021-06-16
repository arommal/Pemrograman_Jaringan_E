import socket
import threading
import logging
import json
from chat import Chat

chat_server = Chat()

class ProcessClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        rcv = ""
        while True:
            data = self.connection.recv(32)
            if data:
                d = data.decode()
                rcv += d
                if rcv[-2:] == '\r\n':
                    logging.warning("Data from client: {}" . format(rcv))
                    result = json.dumps(chat_server.process(rcv))
                    result += "\r\n\r\n"
                    logging.warning("Reply to client: {}" . format(result))
                    self.connection.sendall(result.encode())
                    rcv = ""
            else:
                break

        self.connection.close()


class Server(threading.Thread):
    def __init__(self):
        self.clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind(('127.0.0.1', 8889))
        self.my_socket.listen(1)
        while True:
            self.connection, self.client_address = self.my_socket.accept()
            logging.warning("Connection from {}" . format(self.client_address))
            client = ProcessClient(self.connection, self.client_address)
            client.start()
            self.clients.append(client)


if __name__=="__main__":
    server = Server()
    server.start()