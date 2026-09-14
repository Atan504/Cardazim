import socket
import sys
import os
import threading


def handle_connection(conn: socket.socket, addr):
    while True:
        length = int.from_bytes(conn.recv(4))
        print(f"length {length}")
        data = conn.recv(length)
        if not data:
            print(f"connection {addr[0]}:{addr[1]} closed.")
            break
        from_client = data.decode()
        print(f"Recived data: {from_client}")
        conn.send("im server".encode())
    conn.close()


def run_server(ip, port):
    serv = socket.socket()
    serv.bind((ip, port))
    serv.listen()
    while True:
        t = threading.Thread(target=handle_connection, args=(serv.accept()))
        t.start()
    serv.close()


def main():
    run_server(sys.argv[1], int(sys.argv[2]))


if __name__ == "__main__":
    sys.exit(main())
