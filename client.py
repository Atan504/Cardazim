import argparse
import socket
import sys

from connections import Connection
from card import Card
###########################################################
####################### YOUR CODE #########################
###########################################################


def run_client(server_ip, server_port, name, creator, riddle, solution, path):
    con = Connection.connect(server_ip, server_port)

    card = Card.create_card(name, creator, path, riddle, solution)

    con.send_bytes(card.serialize())
    from_server = con.receive_message()
    con.send_message("")
    con.close()
    print(from_server)


###########################################################
##################### END OF YOUR CODE ####################
###########################################################


def get_args():
    parser = argparse.ArgumentParser(description="Send data to server.")
    parser.add_argument("server_ip", type=str, help="the server's ip")
    parser.add_argument("server_port", type=int, help="the server's port")
    parser.add_argument("name", type=str, help="card's name")
    parser.add_argument("creator", type=str, help="card's creator name")
    parser.add_argument("riddle", type=str, help="card's riddle")
    parser.add_argument("solution", type=str, help="card's solution")
    parser.add_argument("path", type=str, help="card's image path")
    return parser.parse_args()


def main():
    """
    Implementation of CLI and sending data to server.
    """
    args = get_args()
    try:
        run_client(args.server_ip, args.server_port, args.name, args.creator, args.riddle, args.solution, args.path)
        print("Done.")
    except Exception as error:
        print(f"ERROR: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
