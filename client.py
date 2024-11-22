import socket

# Server configuration
HOST = '127.0.0.1'  # Server's hostname or IP address
PORT = 12345        # Server's port

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print(f"Connected to server at {HOST}:{PORT}")

    try:
        while True:
            # Get user input
            message = input("Enter message to send: ")
            if message.lower() == "exit":
                print("Exiting client...")
                break

            # Send message to server
            client.send(message.encode('utf-8'))

            # Receive response from server
            response = client.recv(1024).decode('utf-8')
            print(f"Server response: {response}")
    finally:
        client.close()

if __name__ == "__main__":
    start_client()
