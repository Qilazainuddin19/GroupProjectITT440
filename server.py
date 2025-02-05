import socket
import threading #for performing various tasks at the same time

# Connection Data
host = '192.168.253.3'
port = 8888

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', port))
#waits for clients to connect
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []


# Sending Messages to all connected client about current position each client
def broadcast(message):
    for client in clients:
        print(message)

def handle(client):
    while True:
        try:
            # Broadcasting Messages
            position = client.recv(1024)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break



# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined to the snake ladder game!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening... for client to join snake ladder game")
#It starts an endless while-loop which constantly accepts new connections from clients.
receive()
