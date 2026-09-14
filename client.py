import argparse
import socket
import sys

from connections import Connection

###########################################################
####################### YOUR CODE #########################
###########################################################


def run_client(server_ip, server_port):
    con = Connection.connect(server_ip, server_port)
    while True:
        data = input().encode()
        if not data:
            con.send_message(b"")
            con.close()
            break
        con.send_message(data)
        from_server = con.receive_message()
        print(from_server.decode())


###########################################################
##################### END OF YOUR CODE ####################
###########################################################


def get_args():
    parser = argparse.ArgumentParser(description="Send data to server.")
    parser.add_argument("server_ip", type=str, help="the server's ip")
    parser.add_argument("server_port", type=int, help="the server's port")
    # parser.add_argument("data", type=str, help="the data")
    return parser.parse_args()


def main():
    """
    Implementation of CLI and sending data to server.
    """
    args = get_args()
    try:
        run_client(args.server_ip, args.server_port)
        print("Done.")
    except Exception as error:
        print(f"ERROR: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
