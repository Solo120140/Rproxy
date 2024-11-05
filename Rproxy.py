import socket
import threading

# Define the local binding address and port
LOCAL_HOST = '127.0.0.1'
LOCAL_PORT = 4583

# Define the mining pool address and port
POOL_HOST = 'stratum-na.rplant.xyz'
POOL_PORT = 17068

def handle_client(client_socket):
    # Connect to the mining pool
    pool_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pool_socket.connect((POOL_HOST, POOL_PORT))

    def forward_data(source, destination):
        while True:
            data = source.recv(4096)
            if not data:
                break
            destination.sendall(data)

    # Create threads for bidirectional data transfer
    threading.Thread(target=forward_data, args=(client_socket, pool_socket)).start()
    threading.Thread(target=forward_data, args=(pool_socket, client_socket)).start()

# Start the TCP server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((LOCAL_HOST, LOCAL_PORT))
server.listen(5)

print(f"Proxy server listening on {LOCAL_HOST}:{LOCAL_PORT}...")

while True:
    client_socket, addr = server.accept()
    print(f"Accepted connection from {addr}")
    threading.Thread(target=handle_client, args=(client_socket,)).start()
