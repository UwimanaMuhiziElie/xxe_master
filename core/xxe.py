import socket

class OutOfBandListener:
    def __init__(self, listen_host, listen_port):
        self.listen_host = listen_host
        self.listen_port = listen_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((listen_host, listen_port))
        self.server_socket.listen(1)
        print(f"Listening on {listen_host}:{listen_port} for out-of-band interactions...")

    def start_listener(self):
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                data = client_socket.recv(1024).decode('utf-8')
                print(f"Received Out-of-Band Data: {data} from {client_address}")
                client_socket.close()
        except Exception as e:
            print(f"Listener error: {e}")
