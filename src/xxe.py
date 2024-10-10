import socket
import logging
from config.logger_config import setup_logging  # Updated import path

class OutOfBandListener:
    def __init__(self, listen_host, listen_port, allowed_ips=None):
        self.listen_host = listen_host
        self.listen_port = listen_port
        self.allowed_ips = allowed_ips or []  # List of allowed IPs; empty list means allow all
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((listen_host, listen_port))
        self.server_socket.listen(5)  # Allow up to 5 queued connections
        self.logger = setup_logging()
        self.logger.info(f"Listening on {listen_host}:{listen_port} for out-of-band interactions...")

    def start_listener(self):
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                if self.is_ip_allowed(client_address[0]):
                    self.handle_client(client_socket, client_address)
                else:
                    self.logger.warning(f"Connection attempt from disallowed IP: {client_address[0]}")
                    client_socket.close()
        except Exception as e:
            self.logger.error(f"Listener error: {e}")
        finally:
            self.server_socket.close()

    def is_ip_allowed(self, client_ip):
        if not self.allowed_ips:
            return True  # Allow all if no IP restrictions are set
        return client_ip in self.allowed_ips

    def handle_client(self, client_socket, client_address):
        try:
            data = self.receive_all_data(client_socket)
            self.logger.info(f"Received Out-of-Band Data: {data} from {client_address}")
        except Exception as e:
            self.logger.error(f"Error handling client {client_address}: {e}")
        finally:
            client_socket.close()

    def receive_all_data(self, client_socket):
        data_chunks = []
        while True:
            chunk = client_socket.recv(4096)  # Receive data in chunks of 4096 bytes
            if not chunk:
                break
            data_chunks.append(chunk)
        return b''.join(data_chunks).decode('utf-8')

