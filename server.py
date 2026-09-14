import os
import sys
import threading

from connections import Connection
from listener import Listener


def handle_connection(conn: Connection):
    while True:
        data = conn.receive_message()
        if not data:
            print(repr(conn)[1:-1] + " is sclosed.")
            break
        from_client = data.decode()
        print(f"Recived data: {from_client}")
        conn.send_message("im server".encode())
    conn.close()


def run_server(ip, port):
    serv = Listener(ip, port)
    serv.start()
    while True:
        t = threading.Thread(target=handle_connection, args=([serv.accept()]))
        t.start()
    serv.close()


def main():
    run_server(sys.argv[1], int(sys.argv[2]))


if __name__ == "__main__":
    sys.exit(main())
