import socket
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 12345

def process_task(task):
    """
    Process a given task.
    Example: Count words in a given string.
    """
    print(f"Processing task: {task}")
    word_count = len(task.split())
    return f"Word count: {word_count}"

def handle_client(client_socket, address):
    print(f"New connection: {address}")
    try:
        while True:
            # Receive task from the client
            task = client_socket.recv(1024).decode('utf-8')
            if not task:
                print(f"Client {address} disconnected.")
                break
            
            print(f"Task received from {address}: {task}")
            # Process the task
            result = process_task(task)
            
            # Send result back to the client
            client_socket.send(result.encode('utf-8'))
    except (ConnectionResetError, BrokenPipeError):
        print(f"Connection with {address} lost.")
    finally:
        print(f"Closing connection with {address}.")
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    try:
        while True:
            client_socket, address = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.start()
    finally:
        server.close()
        print("Server closed.")

if __name__ == "__main__":
    start_server()
