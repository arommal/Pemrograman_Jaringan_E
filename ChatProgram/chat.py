import socket
import os
import json

TARGET_IP = "127.0.0.1"
TARGET_PORT = 8889

class ChatClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (TARGET_IP,TARGET_PORT)
        self.sock.connect(self.server_address)
        self.tokenid=""

    def process(self,cmdline):
        j=cmdline.split(" ")
        try:
            command=j[0].strip()
            if (command == 'auth'):
                username = j[1].strip()
                password = j[2].strip()
                return self.login(username,password)
            elif (command == 'send'):
                usernameto = j[1].strip()
                message = ""
                for w in j[2:]:
                   message="{} {}" . format(message,w)
                return self.sendmessage(usernameto,message)
            elif (command == 'inbox'):
                return self.inbox()
            else:
                return "*Incorrect command"
        except IndexError:
                return "-Incorrect command"

    def sendstring(self,string):
        try:
            self.sock.sendall(string.encode())
            receivemsg = ""
            while True:
                data = self.sock.recv(64)
                if (data):
                    receivemsg = "{}{}" . format(receivemsg,data.decode())
                    if receivemsg[-4:] == '\r\n\r\n':
                        return json.loads(receivemsg)
        except:
            self.sock.close()
            return { 'status' : 'ERROR', 'message' : 'Gagal'}

    def login(self, username, password):
        string = "auth {} {} \r\n" . format(username,password)
        result = self.sendstring(string)
        if result['status']=='OK':
            self.tokenid = result['tokenid']
            return "---------------------------------\nUser {} logged in\nToken: {} " . format(username,self.tokenid)
        else:
            return "Error, {}" . format(result['message'])

    def sendmessage(self, usernameto, message):
        if (self.tokenid==""):
            return "Error, not authorized"
        string = "send {} {} {} \r\n" . format(self.tokenid,usernameto,message)
        result = self.sendstring(string)
        if result['status']=='OK':
            return "Message sent to {}" . format(usernameto)
        else:
            return "Error, {}" . format(result['message'])

    def inbox(self):
        if (self.tokenid==""):
            return "Error, not authorized"
        string="inbox {} \r\n" . format(self.tokenid)
        result = self.sendstring(string)
        if result['status']=='OK':
            print("-----------Your Inbox-----------")
            for i in result['messages']:
                print(result['messages'][i])
            # print(result['messages'].i)
            # for i in result:
            #     print(result[i])
        else:
            return "Error, {}" . format(result['message'])



if __name__=="__main__":
    cc = ChatClient()
    while True:
        cmdline = input("Command {}: " . format(cc.tokenid))
        print(cc.process(cmdline))

