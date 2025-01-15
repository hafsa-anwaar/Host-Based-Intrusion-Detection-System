#socket module helps the python program to communicate between server and client
import socket
#logging module helps to keep track of the event
import logging
#threading module helps the serever to handle multiple clients simultaneously by creating single threads for each client
import threading
#datetime module helps to keep track of time in logging activities and the time for blocking of ip
from datetime import datetime, timedelta

#Whenever an intrusive command is detected, the logger 'intrusive' will record a log entry.
intrusive_logger = logging.getLogger('intrusive')
intrusive_handler = logging.FileHandler('intrusive_events.log')
#These logs will be stored in intrusive_events.log
intrusive_logger.addHandler(intrusive_handler)

# Define a list of intrusive commands
intrusive_commands = [
    "sudo", "su", "root", "rm -rf", "rm -r", "del /f /q /s", "format", "shutdown", "reboot",
    "drop table", "truncate table", "delete from", "insert into", "update", "alter table",
    "grant all privileges", "net user", "whoami /priv", "tasklist /v", "ipconfig /all",
    "ping", "traceroute", "telnet", "netcat", "nmap"
]


#This dictionary will keep track of the number of intrusive commands detected for each IP address and the time until which the IP is blocked.
ip_tracker = {}
#When an IP exceeds the allowed number of intrusive commands, it will be blocked for 2 minutes
block_duration = timedelta(minutes=2)
#one ip can address only 5 intrusive commands, after that the IP will be blocked
max_intrusive_commands = 5

#conn is the socket object for the connection, and addr is the address of the client.
def handle_client(conn, addr):
    ip = addr[0]
    print(f"\n\n==============================> Connection established with {addr} <==============================")
#creates a log file for the client's activities identified by its ip address
    activity_logger = logging.getLogger(ip)
    activity_handler = logging.FileHandler(f'{ip}_activity.log')
    activity_logger.addHandler(activity_handler)

    try:
        while True:
            #it will take the data from client upto 1024 bytes at one time and then decode it from byte to string to check for intrusive commands
            data = conn.recv(1024).decode()

            #if no data is received
            if not data:
                break

            print(f"Received command: {data}")
            activity_logger.info(f'Received command: {data}')

            # Check if the IP is blocked
            if ip in ip_tracker and ip_tracker[ip]['blocked_until'] > datetime.now():
                conn.sendall(b'IP blocked. Try again later.\n')
                continue

            #initializing a flag to detect intrusive command
            is_intrusive = any(command in data.lower() for command in intrusive_commands)

            if is_intrusive:
                #creates the intrusive_events file and save the events there
                intrusive_logger.warning(f'Intrusive command detected from {addr}: {data}')
                activity_logger.warning(f'Intrusive command detected: {data}')

                #If the IP is not in the tracker, add it with a count of 0 and not blocked
                if ip not in ip_tracker:
                    ip_tracker[ip] = {'count': 0, 'blocked_until': datetime.min}
                ip_tracker[ip]['count'] += 1

                # Block IP if max intrusive commands are exceeded
                if ip_tracker[ip]['count'] > max_intrusive_commands:
                    ip_tracker[ip]['blocked_until'] = datetime.now() + block_duration
                    conn.sendall(b"Too many intrusive commands. IP blocked .\n")
                    print(f"IP {ip} blocked until {ip_tracker[ip]['blocked_until']}")
                else:
                    conn.sendall(b'Intrusive command.\n')
            else:
                # Respond for non-intrusive commands
                conn.sendall(b'Command executed successfully\n')
                print(f"Sent response: Command executed successfully to {addr}")
    except Exception as e:
        logging.error(f'Error handling client {addr}: {e}')
    finally:
        conn.close()
        print(f"\n\n=========================> Connection closed with {addr} <=========================")

def start_server(host, port):
    #This creates a new socket using the Internet address family AF_INET (IPv4) and the SOCK_STREAM socket type i.e it will be a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #it will make a connection through this info of server, initialized before
        s.bind((host, port))
        #server will take incoming connection requests. By default, it can queue up to 5 connection requests if they are waiting to connect
        s.listen(5)
        print(f"\n\n==============================> Server listening on {host}:{port} <==============================")
        while True:
            #This allows the server to handle the client's communication in parallel with other client connections
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

def main():
    #This sets the server's hostname to localhost (127.0.0.1)
    host = 'localhost'
    #port 9090 is used as an alternative for port 80 and 443 as a server's port
    port = 9090
    start_server(host, port)

if __name__ == '__main__':
    main()        
