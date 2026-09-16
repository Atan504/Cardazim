import socket


class Connection:
    def __init__(self, connection: socket.socket):
        self.connection = connection

    def __repr__(self):
        source = self.connection.getsockname()
        destination = self.connection.getpeername()
        return f"<Connection from {source} to {destination}>"

    def send_message(self, message: bytes):
        packet = len(message).to_bytes(4) + message
        self.connection.send(packet)

    def receive_message(self) -> bytes:
        try:
            length = int.from_bytes(self.connection.recv(4))
            return self.connection.recv(length)
        except Exception as error:
            print(f"ERROR: {error}")
            return 1

    @classmethod
    def connect(cls, host: str, port: int):
        soc = socket.socket()
        soc.connect((host, port))
        return Connection(soc)

    def close(self):
        self.connection.close()

    def __exit__(self, exc_type, exc, tb):
        self.close()
