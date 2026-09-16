import socket


class Connection:
    def __init__(self, connection: socket.socket):
        self.connection = connection

    def __repr__(self):
        source = self.connection.getsockname()
        destination = self.connection.getpeername()
        return f"<Connection from {source} to {destination}>"

    def send_message(self, message: str):
        self.send_bytes(message.encode())

    def send_bytes(self, byts: bytes):
        packet = len(byts).to_bytes(8) + byts
        self.connection.send(packet)

    def receive_message(self) -> str:
        self.receive_bytes().decode()

    def receive_bytes(self) -> bytes:
        try:
            length = int.from_bytes(self.connection.recv(8))
            buffer = length
            data = b""

            while buffer > 0:  # making sure to receive all data
                temp = self.connection.recv(buffer)
                data += temp
                buffer -= len(temp)

            if len(data) != length:
                print(f"Message not the expected length! expected: {length}, got: {len(data)}")

            return data

        except Exception as error:
            print(f"ERROR: {error}")

    @classmethod
    def connect(cls, host: str, port: int):
        soc = socket.socket()
        soc.connect((host, port))
        return Connection(soc)

    def close(self):
        self.connection.close()

    def __exit__(self, exc_type, exc, tb):
        self.close()
