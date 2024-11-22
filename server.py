import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 12345        # Port to listen on
TIMEOUT = 60        # Timeout in seconds for inactivity

def handle_client(client_socket, address):
    print(f"New connection: {address}")
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print(f"Client {address} disconnected.")
                break
            print(f"Message from {address}: {message}")
            client_socket.send(f"Echo: {message}".encode('utf-8'))
    except (ConnectionResetError, BrokenPipeError):
        print(f"Connection with {address} lost.")
    finally:
        print(f"Closing connection with {address}.")
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    server.settimeout(TIMEOUT)  # Set the timeout for inactivity
    print(f"Server listening on {HOST}:{PORT} (Timeout: {TIMEOUT} seconds)")

    try:
        while True:
            try:
                client_socket, address = server.accept()
                print(f"Accepted connection from {address}")
                client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
                client_thread.start()
            except socket.timeout:
                print(f"No activity detected for {TIMEOUT} seconds. Server shutting down...")
                break
    finally:
        server.close()
        print("Server closed.")

if __name__ == "__main__":
    start_server()
