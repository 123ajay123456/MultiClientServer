import os
import socket
import threading

# Server Configuration
SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5005
BUFFER_SIZE = 65536
SAVE_DIR = "server_files"

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))

# Dictionary to track client names
client_names = {}

def ensure_directory(client_name):
    """Ensure a unique directory exists for each client name."""
    client_dir = os.path.join(SAVE_DIR, client_name)
    os.makedirs(client_dir, exist_ok=True)
    return client_dir

def handle_client(data, client_address):
    """Handle incoming data from a client."""
    global client_names

    # Check if the client has provided a name
    if client_address not in client_names:
        client_name = data.decode("utf-8")
        client_names[client_address] = client_name
        print(f"Registered new client: {client_name} ({client_address})")
        return

    # Save data as a file in the client's directory
    client_name = client_names[client_address]
    client_dir = ensure_directory(client_name)
    file_path = os.path.join(client_dir, f"{client_name}_file.bin")

    with open(file_path, "ab") as f:
        f.write(data)

    print(f"Data saved from {client_name} ({client_address}) to {file_path}")

def server_main():
    print(f"Server started at {SERVER_IP}:{SERVER_PORT}")
    while True:
        try:
            data, client_address = server_socket.recvfrom(BUFFER_SIZE)
            threading.Thread(target=handle_client, args=(data, client_address)).start()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    os.makedirs(SAVE_DIR, exist_ok=True)
    server_main()
