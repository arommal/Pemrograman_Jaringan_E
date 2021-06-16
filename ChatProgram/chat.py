import uuid
import logging
import socket
import json
from queue import Queue

TARGET_IP = '127.0.0.1'
TARGET_PORT = 8889

class Chat:
    def __init__(self):
        self.sessions = {}
        self.users = {}
        self.users['Rosa'] = {
            'nama': 'Rosa Valentine',
            'negara': 'Indonesia',
            'password': 'asdasdasd',
            'incoming': {},
            'outgoing': {}
        }
        self.users['Afia'] = {
            'nama': 'Afia Hana',
            'negara': 'Indonesia',
            'password': 'asdasdasd',
            'incoming': {},
            'outgoing': {}
        }
        self.users['Salsa'] = {
            'nama': 'Salsabila Harlen',
            'negara': 'Indonesia',
            'password': 'asdasdasd',
            'incoming': {},
            'outgoing': {}
        }
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (TARGET_IP, TARGET_PORT)
        self.sock.connect(self.server_address)
        self.tokenid = ""

    def process(self, data):
        j = data.split(" ")

        try:
            cmd = j[0].strip()
            if cmd == "auth":
                username = j[1].strip()
                password = j[2].strip()
                logging.warning("AUTH: auth {} {}" . format(username, password))
                return self.authenticate(username, password)
            elif cmd == "send":
                session_id = self.tokenid
                username_to = j[1].strip()
                username_from = self.sessions[session_id]['username']
                message = ""
                for w in j[2:]:
                    message = "{} {}" . format(message, w)
                logging.warning("SEND: session {} send message from {} to {}" . format(session_id, username_from, username_to))
                return self.sendMessage(username_from, username_to, message)
            elif cmd == "inbox":
                session_id = self.tokenid
                username = self.sessions[session_id]['username']
                logging.warning("INBOX: {}" . format(session_id))
                return self.getInbox(username)
            else:
                return {'status': 'ERROR', 'message': 'Incorrect Protocol'}
        except KeyError:
            return {'status': 'ERROR', 'message': 'Information Not Found'}
        except IndexError:
            return {'status': 'ERROR', 'message': 'Incorrect Protocol'}

    def authenticate(self, username, password):
        if username not in self.users:
            return {'status': 'ERROR', 'message': 'User Does Not Exist'}
        if self.users[username]['password'] != password:
            return {'status': 'ERROR', 'message': 'Incorrect Password'}
        token_id = str(uuid.uuid4())
        self.sessions[token_id] = {'username': username, 'userdetail': self.users[username]}
        self.tokenid = token_id
        return {'status': 'OK', 'tokenid': token_id}

    def getUser(self, username):
        if username not in self.users:
            return False
        return self.users[username]

    def sendMessage(self, username_from, username_to, message):
        if self.tokenid == "":
            return {'status': 'ERROR', 'message': 'Session Not Found'}

        sender = self.getUser(username_from)
        receiver = self.getUser(username_to)

        if sender == False or receiver == False:
            return {'status': 'ERROR', 'message': 'User Not Found'}

        message = {'from': sender['nama'], 'to': receiver['nama'], 'message': message}

        outqueue = sender['outgoing']
        inqueue = receiver['incoming']

        try:
            outqueue[username_from].put(message)
        except KeyError:
            outqueue[username_from] = Queue()
            outqueue[username_from].put(message)

        try:
            inqueue[username_from].put(message)
        except KeyError:
            inqueue[username_from] = Queue()
            inqueue[username_from].put(message)

        return {'status': 'OK', 'message': 'Message Sent'}

    def getInbox(self, username):
        user = self.getUser(username)
        incoming = user['incoming']
        msgs = {}
        for u in incoming:
            msgs[u] = []
            while not incoming[u].empty():
                msgs[u].append(user['incoming'][u].get_nowait())

        return {'status': 'OK', 'message': msgs}


if __name__=="__main__":
    j = Chat()
    while True:
        cmdline = input("Command : ")
        print(j.process(cmdline))
