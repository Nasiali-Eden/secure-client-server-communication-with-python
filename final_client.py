import socket
import ssl

# Server configuration
HOST = '127.0.0.1'  # Server's IP address
PORT = 12345        # Server's listening port
CERT_FILE = "server.crt"  # Path to the server's public certificate

def start_client():
    # Create an SSL context with required settings
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)  # Context for client authentication
    context.load_verify_locations(CERT_FILE)  # Load the server's certificate for verification

    # Create a client socket
    with socket.create_connection((HOST, PORT)) as sock:  # Connect to the server
        with context.wrap_socket(sock, server_hostname=HOST) as secure_sock:  # Wrap the socket with SSL
            print(f"Connected to server at {HOST}:{PORT}")  # Print success message

            # Authentication step
            print(secure_sock.recv(1024).decode('utf-8'))  # Prompt for username
            username = input("Enter username: ")  # Get username input
            secure_sock.send(username.encode('utf-8'))  # Send username to server

            print(secure_sock.recv(1024).decode('utf-8'))  # Prompt for password
            password = input("Enter password: ")  # Get password input
            secure_sock.send(password.encode('utf-8'))  # Send password to server

            # Receive authentication response
            auth_response = secure_sock.recv(1024).decode('utf-8')  # Get server response
            print(auth_response)  # Print response

            if "failed" in auth_response.lower():  # Check for failure
                print("Exiting client.")  # Exit if authentication fails
                return

            # Task processing after authentication
            while True:
                task = input("Enter task (or 'exit' to quit): ")  # Get task from user
                if task.lower() == "exit":  # Exit condition
                    print("Exiting client.")  # Print exit message
                    break
                secure_sock.send(task.encode('utf-8'))  # Send task to server
                response = secure_sock.recv(1024).decode('utf-8')  # Receive server response
                print(f"Server response: {response}")  # Print response

if __name__ == "__main__":
    start_client()  # Run the client
