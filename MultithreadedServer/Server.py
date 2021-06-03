import socket
import threading
import logging
from file_protocol import FileProtocol

fp = FileProtocol()

class ProcessClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        while True:
            data = self.connection.recv(32)
            if data:
                d = data.decode()
                result = fp.processString(d)
                result += "\r\n\r\n"
                self.connection.sendall(result.encode())
            else:
                break
        self.connection.close()

class Server(threading.Thread):
    def __init__(self, ipaddress, port):
        self.ipinfo = (ipaddress, port)
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        threading.Thread.__init__(self)

    def run(self):
        logging.warning(f"Server is running on {self.ipinfo}")
        self.my_socket.bind(self.ipinfo)
        self.my_socket.listen(1)

        while True:
            self.connection, self.client_address = self.my_socket.accept()
            logging.warning(f"Connection from {self.client_address}")
            clt = ProcessClient(self.connection, self.client_address)
            clt.start()
            self.the_clients.append(clt)

if __name__ == '__main__':
    server = Server(ipaddress='127.0.0.1', port=6666)
    server.start()