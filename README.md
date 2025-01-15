# Host-Based-Intrusion-Detection-System
# Server-Side Features:

Establishes and manages TCP connections with clients.
Logs activities and intrusive commands in separate files.
Handles multiple clients concurrently using threads.
Detects and tracks intrusive commands, blocking IPs after  5 intrusive commands are entered.


# Client-Side Features:

Connects to the server and sends commands.
Logs sent commands and received responses.
Implements a timeout for server responses.
Provide flexibility to type exit to close the connection.
Continuously prompts the user for commands and handles server responses.
