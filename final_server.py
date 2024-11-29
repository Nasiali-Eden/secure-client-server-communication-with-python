import socket
import ssl
import threading
import logging
import time

# Server configuration
HOST = '127.0.0.1'  # Server's IP address
PORT = 12345        # Port for client connections
CERT_FILE = "server.crt"  # Path to the SSL certificate
KEY_FILE = "server.key"   # Path to the SSL private key
TASK_TIMEOUT = 30  # Timeout (in seconds) for handling unresponsive clients
SERVER_TIMEOUT = 60  # Timeout (in seconds) for no incoming connections

# Predefined user credentials
VALID_USERS = {
    "Tesla": "password1",
    "admin": "administrator",
    "Selina": "selinakyle"
}

# Configure logging
logging.basicConfig(
    filename="server.log",  # Log file name
    level=logging.INFO,     # Log level
    format="%(asctime)s - %(levelname)s - %(message)s"  # Log format
)
console = logging.StreamHandler()  # Create a console handler
console.setLevel(logging.INFO)  # Set level for console output
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")  # Format for console
console.setFormatter(formatter)  # Apply format to console
logging.getLogger().addHandler(console)  # Add console handler to the root logger

def authenticate(client_socket):
    # Authenticate the client by validating username and password
    try:
        client_socket.send("Username: ".encode('utf-8'))  # Prompt for username
        username = client_socket.recv(1024).decode('utf-8')  # Receive username

        client_socket.send("Password: ".encode('utf-8'))  # Prompt for password
        password = client_socket.recv(1024).decode('utf-8')  # Receive password

        if VALID_USERS.get(username) == password:  # Validate credentials
            client_socket.send("Authentication successful.".encode('utf-8'))  # Success message
            logging.info(f"Client authenticated: {username}")  # Log success
            return True
        else:
            client_socket.send("Authentication failed.".encode('utf-8'))  # Failure message
            logging.warning(f"Failed login attempt with username: {username}")  # Log failure
            return False
    except Exception as e:
        logging.error(f"Error during authentication: {e}")  # Log error
        return False

def process_task(task):
    # Process a task (example: reverse a string)
    try:
        logging.info(f"Processing task: {task}")  # Log task
        result = task[::-1]  # Reverse the string
        time.sleep(3)  # Simulate delay in processing
        return f"Processed task: {result}"  # Return result
    except Exception as e:
        logging.error(f"Error processing task: {e}")  # Log error
        return f"Error: {str(e)}"  # Return error message

def handle_client(client_socket, address):
    # Handle communication with a client
    logging.info(f"New connection from {address}")  # Log new connection
    client_socket.settimeout(TASK_TIMEOUT)  # Set timeout for client responses
    try:
        if not authenticate(client_socket):  # Authenticate the client
            logging.warning(f"Client {address} failed authentication.")  # Log failure
            return  # Close the connection if authentication fails

        while True:  # Handle tasks after successful authentication
            task = client_socket.recv(1024).decode('utf-8')  # Receive task
            if not task:  # Check for disconnection
                logging.info(f"Client {address} disconnected.")  # Log disconnection
                break
            logging.info(f"Task received from {address}: {task}")  # Log received task
            result = process_task(task)  # Process the task
            client_socket.send(result.encode('utf-8'))  # Send result back
    except (ConnectionResetError, BrokenPipeError):  # Handle abrupt disconnection
        logging.warning(f"Connection with {address} lost unexpectedly.")  # Log warning
    except Exception as e:  # Handle unexpected errors
        logging.error(f"Unexpected error with client {address}: {e}")  # Log error
    finally:
        client_socket.close()  # Close the client socket
        logging.info(f"Connection with {address} closed.")  # Log closure

def start_server():
    # Create an SSL context with the required settings
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)  # Context for server authentication
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)  # Load the server's certificate and private key

    # Create a server socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow port reuse
        server_socket.bind((HOST, PORT))  # Bind the server to the host and port
        server_socket.listen(5)  # Listen for incoming connections
        server_socket.settimeout(SERVER_TIMEOUT)  # Set a timeout for incoming connections
        logging.info(f"Server listening on {HOST}:{PORT}")  # Log server startup

        try:
            with context.wrap_socket(server_socket, server_side=True) as secure_server:  # Wrap the server with SSL
                while True:
                    try:
                        client_socket, address = secure_server.accept()  # Accept a client connection
                        logging.info(f"Accepted connection from {address}")  # Log connection
                        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))  # Create a thread for the client
                        client_thread.start()  # Start the client thread
                    except socket.timeout:  # Handle no incoming connections within the timeout
                        logging.info("No connections received. Shutting down the server.")  # Log shutdown message
                        break  # Exit the loop to shut down the server
        except Exception as e:
            logging.error(f"Server error: {e}")  # Log server error
        finally:
            logging.info("Server shut down.")  # Log server shutdown

if __name__ == "__main__":
    start_server()  # Run the server
