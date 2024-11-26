import socket
import ssl
import threading
import logging
import time

# Server configuration
HOST = '127.0.0.1'  # Server IP address
PORT = 12345        # Port for client connections
CERT_FILE = "server.crt"  # Path to the server's certificate
KEY_FILE = "server.key"   # Path to the server's private key
RETRY_DELAY = 5  # Delay in seconds between retries for accepting new connections
TASK_TIMEOUT = 15  # Timeout for processing tasks in seconds
MAX_THREADS = 3  # Maximum number of concurrent threads

# Configure logging
logging.basicConfig(
    filename="server.log",  # Log file for server events
    level=logging.INFO,     # Log level
    format="%(asctime)s - %(levelname)s - %(message)s"  # Log format
)

def process_task(task):
    # Simulate task processing (example: reverse a string)
    try:
        logging.info(f"Processing task: {task}")  # Log task
        result = task[::-1]  # Reverse the string
        time.sleep(3)  # Simulate processing delay
        return f"Processed task: {result}"  # Return result
    except Exception as e:
        logging.error(f"Error processing task: {e}")  # Log error
        return f"Error: {str(e)}"  # Return error message

def handle_client(client_socket, address):
    # Handle communication with a client
    logging.info(f"New connection from {address}")  # Log new connection
    client_socket.settimeout(TASK_TIMEOUT)  # Set timeout for client
    try:
        while True:
            try:
                task = client_socket.recv(1024).decode('utf-8')  # Receive task
                if not task:  # Check if client disconnected
                    logging.info(f"Client {address} disconnected.")  # Log disconnection
                    break
                logging.info(f"Task received from {address}: {task}")  # Log task
                result = process_task(task)  # Process the task
                client_socket.send(result.encode('utf-8'))  # Send result
            except socket.timeout:  # Handle task timeout
                logging.warning(f"Task timeout for client {address}")  # Log timeout
                break
    except (ConnectionResetError, BrokenPipeError):  # Handle abrupt disconnection
        logging.warning(f"Connection with {address} lost unexpectedly.")  # Log warning
    except Exception as e:  # Handle unexpected errors
        logging.error(f"Unexpected error with client {address}: {e}")  # Log error
    finally:
        client_socket.close()  # Close the client socket
        logging.info(f"Connection with {address} closed.")  # Log closure

def start_server():
    # Start the secure server with retry mechanism
    while True:  # Retry loop for server
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket
            server = ssl.wrap_socket(server, keyfile=KEY_FILE, certfile=CERT_FILE, server_side=True)  # SSL wrap
            server.bind((HOST, PORT))  # Bind the server to address and port
            server.listen(MAX_THREADS)  # Listen for incoming connections
            logging.info(f"Server listening on {HOST}:{PORT}")  # Log server start

            while True:
                client_socket, address = server.accept()  # Accept client connection
                client_thread = threading.Thread(target=handle_client, args=(client_socket, address))  # Create thread
                client_thread.start()  # Start thread
        except Exception as e:  # Handle server errors
            logging.error(f"Error: {e}. Retrying in {RETRY_DELAY} seconds.")  # Log retry
            time.sleep(RETRY_DELAY)  # Wait before retrying
        finally:
            server.close()  # Ensure server socket is closed
            logging.info("Server shut down.")  # Log shutdown

if __name__ == "__main__":
    start_server()  # Run the server
