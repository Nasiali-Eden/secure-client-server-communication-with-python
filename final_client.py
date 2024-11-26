import socket
import ssl

# Server configuration
HOST = '127.0.0.1'  # Server IP address
PORT = 12345        # Port for server connection
CERT_FILE = "server.crt"  # Path to the server's certificate

def start_client():
    # Start a secure client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket
    client = ssl.wrap_socket(client, cert_reqs=ssl.CERT_REQUIRED, ca_certs=CERT_FILE)  # SSL wrap

    try:
        client.connect((HOST, PORT))  # Connect to the server
        print(f"Connected to server at {HOST}:{PORT}")  # Print connection message

        while True:
            task = input("Enter task (or 'exit' to quit): ")  # Prompt user for task
            if task.lower() == "exit":  # Exit condition
                print("Exiting client.")  # Print exit message
                break
            client.send(task.encode('utf-8'))  # Send task to server
            response = client.recv(1024).decode('utf-8')  # Receive server response
            print(f"Server response: {response}")  # Print server response
    except Exception as e:  # Handle client errors
        print(f"Error: {e}")  # Print error
    finally:
        client.close()  # Close the client socket
        print("Client connection closed.")  # Print closure message

if __name__ == "__main__":
    start_client()  # Run the client
