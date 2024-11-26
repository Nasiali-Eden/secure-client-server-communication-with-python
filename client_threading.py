import socket
import ssl
import threading
import logging

# Server configuration
HOST = '127.0.0.1'  # Server IP address
PORT = 12345        # Port for client connections
CERT_FILE = "server.crt"  # Path to the server's certificate
KEY_FILE = "server.key"   # Path to the server's private key

# Configure logging for debugging and monitoring
logging.basicConfig(
    filename="server.log",  # Log file name
    level=logging.INFO,     # Log level
    format="%(asctime)s - %(levelname)s - %(message)s"  # Log message format
)

def process_task(task):
    # Process a given task (example: reverse a string)
    try:
        logging.info(f"Processing task: {task}")  # Log task processing
        result = task[::-1]  # Reverse the string
        return f"Processed task: {result}"  # Return processed result
    except Exception as e:
        logging.error(f"Error processing task: {e}")  # Log task errors
        return f"Error processing task: {str(e)}"  # Return error message

def handle_client(client_socket, address):
    # Handle communication with a single client
    logging.info(f"New connection from {address}")  # Log new client connection
    try:
        while True:
            task = client_socket.recv(1024).decode('utf-8')  # Receive task from client
            if not task:  # Check for client disconnection
                logging.info(f"Client {address} disconnected.")  # Log disconnection
                break
            logging.info(f"Task received from {address}: {task}")  # Log received task

            result = process_task(task)  # Process the task
            client_socket.send(result.encode('utf-8'))  # Send result back to the client
    except (ConnectionResetError, BrokenPipeError):  # Handle abrupt disconnections
        logging.warning(f"Connection with {address} lost unexpectedly.")  # Log warning
    except Exception as e:  # Handle other exceptions
        logging.error(f"Unexpected error with client {address}: {e}")  # Log error
    finally:
        client_socket.close()  # Close the client connection
        logging.info(f"Connection with {address} closed.")  # Log connection closure

def start_server():
    # Start the secure server and listen for client connections
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket
    server = ssl.wrap_socket(server, keyfile=KEY_FILE, certfile=CERT_FILE, server_side=True)  # Wrap socket with SSL

    server.bind((HOST, PORT))  # Bind server to IP and port
    server.listen(5)  # Listen for incoming connections
    logging.info(f"Secure server listening on {HOST}:{PORT}")  # Log server start

    try:
        while True:
            try:
                client_socket, address = server.accept()  # Accept a new client connection
                client_thread = threading.Thread(target=handle_client, args=(client_socket, address))  # Start a thread for the client
                client_thread.start()  # Run the client thread
            except Exception as e:  # Handle errors while accepting new connections
                logging.error(f"Error accepting new connection: {e}")  # Log error
    finally:
        server.close()  # Close the server socket
        logging.info("Server shut down.")  # Log server shutdown

if __name__ == "__main__":
    start_server()  # Run the server
