import socket
import pickle

class Networking:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.con.connect((self.ip, self.port))
            print("[CONNECTION ESTABLISHED]")
            return self.con
        except:
            print("Can't reach the server at the moment.")

    def host(self):
        try:
            self.con.bind((self.ip, self.port))
            print("[SERVER STARTED]")
            return self.con
        except:
            print("[ERROR]")

    def send(self, con, data):
        data = pickle.dumps(data)
        data_len = str(len(data))
        data_len = (8 - len(data_len)) * '0' + data_len

        con.send(data_len.encode())
        con.send(data)

    def recv(self, con):
        data_len = con.recv(8)
        data = con.recv(int(data_len))

        return pickle.loads(data)