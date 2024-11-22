import socket

# Server configuration
HOST = '127.0.0.1'
PORT = 12345

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print(f"Connected to server at {HOST}:{PORT}")

    try:
        while True:
            # Get task input from the user
            task = input("Enter a sentence to process (or type 'exit' to quit): ")
            if task.lower() == "exit":
                print("Exiting client...")
                break

            # Send task to server
            client.send(task.encode('utf-8'))

            # Receive result from server
            result = client.recv(1024).decode('utf-8')
            print(f"Result from server: {result}")
    finally:
        client.close()

if __name__ == "__main__":
    start_client()
