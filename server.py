import socket
import sys
import os


def run_server(ip, port):
    serv = socket.socket()
    serv.bind((ip, port))
    serv.listen()
    while True:
        conn, addr = serv.accept()
        while True:
            data = conn.recv(4096)
            if not data:
                break
            from_client = data.decode()
            print(f"Recived data: {from_client}")
            conn.send("im server".encode())
        conn.close()
    serv.close()


def main():
    run_server(sys.argv[1], int(sys.argv[2]))


if __name__ == "__main__":
    sys.exit(main())
