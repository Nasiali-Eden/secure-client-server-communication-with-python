import socket
import ssl

# Server configuration
HOST = '127.0.0.1'
PORT = 12345
CERT_FILE = "server.crt"  # Path to the server's certificate file (to verify server identity)

def start_client():
    # Create a socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Wrap the socket with SSL
    client = ssl.wrap_socket(client, cert_reqs=ssl.CERT_REQUIRED, ca_certs=CERT_FILE)

    try:
        # Connect to the server
        client.connect((HOST, PORT))
        print(f"Connected to secure server at {HOST}:{PORT}")

        while True:
            # Get task input from the user
            task = input("Enter a task (or type 'exit' to quit): ")
            if task.lower() == "exit":
                print("Exiting client...")
                break

            # Send task to the server
            client.send(task.encode('utf-8'))

            # Receive response from the server
            response = client.recv(1024).decode('utf-8')
            print(f"Response from server: {response}")
    finally:
        client.close()

if __name__ == "__main__":
    start_client()
