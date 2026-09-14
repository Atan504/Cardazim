import argparse
import socket
import sys


###########################################################
####################### YOUR CODE #########################
###########################################################


def run_client(server_ip, server_port):
    soc = socket.socket()
    soc.connect((server_ip, server_port))
    while True:
        data = input().encode()
        if not data:
            send_data(soc, "".encode())
            soc.close()
            break
        from_server = send_data(soc, data)
        print(from_server.decode())


def send_data(sock, data: bytes):
    packet = len(data).to_bytes(4) + data
    sock.send(packet)
    return sock.recv(4096)


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
