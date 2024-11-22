import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 12345        # Port to listen on

# Function to handle client connections
def handle_client(client_socket, address):
    print(f"New connection: {address}")
    try:
        while True:
            # Receive data from client
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print(f"Client {address} disconnected.")
                break  # Exit loop if no message is received
            print(f"Message from {address}: {message}")
            # Echo message back to client
            client_socket.send(f"Echo: {message}".encode('utf-8'))
    except (ConnectionResetError, BrokenPipeError):
        print(f"Connection with {address} lost.")
    finally:
        print(f"Closing connection with {address}.")
        client_socket.close()  # Ensure the client socket is closed

# Main server function
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, address = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

if __name__ == "__main__":
    start_server()
