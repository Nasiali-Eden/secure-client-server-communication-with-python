import socket
import ssl
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 12345
CERT_FILE = "server.crt"  # Path to the certificate file
KEY_FILE = "server.key"   # Path to the private key file

def handle_client(client_socket, address):
    print(f"New secure connection: {address}")
    try:
        while True:
            # Receive data from the client
            task = client_socket.recv(1024).decode('utf-8')
            if not task:
                print(f"Client {address} disconnected.")
                break
            print(f"Task received from {address}: {task}")
            # Placeholder for task processing
            result = f"Processed task: {task}"
            client_socket.send(result.encode('utf-8'))
    except Exception as e:
        print(f"Error with client {address}: {e}")
    finally:
        client_socket.close()
        print(f"Connection with {address} closed.")

def start_server():
    # Create a socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Wrap the socket with SSL
    server = ssl.wrap_socket(server, keyfile=KEY_FILE, certfile=CERT_FILE, server_side=True)

    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Secure server listening on {HOST}:{PORT}")

    try:
        while True:
            client_socket, address = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.start()
    finally:
        server.close()
        print("Server shut down.")

if __name__ == "__main__":
    start_server()
