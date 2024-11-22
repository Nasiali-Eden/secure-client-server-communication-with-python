import socket
import multiprocessing
import re

# Server configuration
HOST = '127.0.0.1'
PORT = 12345

def process_task(task):
    """
    Safely evaluate a mathematical expression sent by the client.
    """
    try:
        # Simple sanitization to avoid malicious input
        if not re.match(r'^[\d+\-*/(). ]+$', task):
            return "Error: Invalid expression"
        
        # Evaluate the expression
        result = eval(task)
        return f"Result: {result}"
    except Exception as e:
        return f"Error processing task: {str(e)}"

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
            
            # Process the task using multiprocessing
            with multiprocessing.Pool(1) as pool:  # Limit to 1 process for task isolation
                result = pool.apply(process_task, (task,))
            
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
            process = multiprocessing.Process(target=handle_client, args=(client_socket, address))
            process.start()
    finally:
        server.close()
        print("Server closed.")

if __name__ == "__main__":
    start_server()
