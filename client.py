import argparse
import socket
import sys


###########################################################
####################### YOUR CODE #########################
###########################################################


def send_data(server_ip, server_port, data):
    soc = socket.socket()
    soc.connect((server_ip, server_port))
    soc.send(data)
    from_server = soc.recv(4096)
    soc.close()
    print(from_server.decode())
    pass


###########################################################
##################### END OF YOUR CODE ####################
###########################################################


def get_args():
    parser = argparse.ArgumentParser(description="Send data to server.")
    parser.add_argument("server_ip", type=str, help="the server's ip")
    parser.add_argument("server_port", type=int, help="the server's port")
    parser.add_argument("data", type=str, help="the data")
    return parser.parse_args()


def main():
    """
    Implementation of CLI and sending data to server.
    """
    args = get_args()
    try:
        send_data(args.server_ip, args.server_port, args.data.encode())
        print("Done.")
    except Exception as error:
        print(f"ERROR: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
