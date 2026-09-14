import socket

from connections import Connection


class Listener:
    def __init__(self, ip: str, port: int):
        self.soc = socket.socket()
        self.soc.bind((ip, port))
        self.backlog = 1000

    def __repr__(self):
        addr = self.soc.getsockname()
        return f"Listener(port={addr[1]}, host={addr[0]}, backlog={self.backlog})"

    def start(self):
        self.soc.listen()

    def stop(self):
        self.soc.close()

    def accept(self):
        sock, addr = self.soc.accept()
        return Connection(sock)

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc, tb):
        self.stop()
