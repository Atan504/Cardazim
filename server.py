import sys
import threading

from connections import Connection
from listener import Listener
from card import Card


def handle_connection(conn: Connection):
    while True:
        from_client = conn.receive_bytes()
        if not from_client:
            print(repr(conn)[1:-1] + " is sclosed.")
            break
        card = Card.deserialize(from_client)
        print(str(card))
        conn.send_message("im server")
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
