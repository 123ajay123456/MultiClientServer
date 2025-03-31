import socket
import os

# Server Configuration
SERVER_IP = input("Enter the server IP: ")  # e.g., 192.168.1.10
SERVER_PORT = 5005
BUFFER_SIZE = 65536

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_name(client_name):
    """Send the client name to the server."""
    client_socket.sendto(client_name.encode("utf-8"), (SERVER_IP, SERVER_PORT))

def send_file(file_path):
    """Send a file to the server in chunks."""
    if not os.path.exists(file_path):
        print(f"File {file_path} not found!")
        return

    with open(file_path, "rb") as f:
        while chunk := f.read(65500):
            client_socket.sendto(chunk, (SERVER_IP, SERVER_PORT))
            print(f"Sent {len(chunk)} bytes to {SERVER_IP}:{SERVER_PORT}")

if __name__ == "__main__":
    client_name = input("Enter your name: ")
    send_name(client_name)
    
    file_path = input("Enter the path to the file to send: ")
    send_file(file_path)
