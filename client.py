import socket
import logging

# Creating a log for client's activity
logging.basicConfig(filename='client_activity.log', level=logging.INFO, format='%(asctime)s %(message)s')

# Server's info
HOST = 'localhost'
PORT = 9090

def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
 #if any operation (like sending or receiving data) takes longer than 5 seconds, the socket will raise a socket.timeout exception
            s.settimeout(10)  
            print("=====================================================")
            print(f"| CLIENT CONNECTED WITH PORT {PORT} |")
            print("=====================================================")

            while True:
                message = input("Enter a command: ")
                if message.lower() == 'exit':
                    print("Closing connection...")
                    break

                # Send the user's message to the server in form of bytes through encoding
                s.sendall(message.encode())

                try:
                    # Receive server's response
                    data = s.recv(1024)
                    response = data.decode()
                    print(f"Received from server: {response}")

                    # Log client activity
                    logging.info(f"Sent command: {message}")
                    logging.info(f"Received response: {response}")

                    # Handle blocked message
                    if "IP blocked" in response:
                        print("Your IP is blocked. Please try again later.")
                        break

                except socket.timeout:
                    print("Server response timeout. Please try again.")
                except Exception as e:
                    print(f"Error receiving data from server: {e}")

    except ConnectionRefusedError:
        print("Connection failed. Make sure the server is running.")
    except KeyboardInterrupt:
        print("\nExiting client...")
    finally:
        print("Client closed.")

if __name__ == "__main__":
    main()
