# SocketUtils
import socket
import pickle
import select


class SocketConnection:

    TCP_PORT = 5005
    BUFFER_SIZE = 1024

    def __init__(self):
        self.__socket = None

    def start_server(self, ip_address, port=TCP_PORT):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind((ip_address, port))
        self.__socket.listen()

    def receive_object(self):
        new_sock, addr = self.__socket.accept()
        all_data = b''
        while True:
            data = new_sock.recv(self.BUFFER_SIZE)
            if not data: break
            all_data = all_data + data
        return pickle.loads(all_data)

    def close(self):
        self.__socket.close()

    def send_object(self, ip_addr, blk, port=TCP_PORT):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((ip_addr, port))
        data = pickle.dumps(blk)
        self.__socket.send(data)
        self.close()





