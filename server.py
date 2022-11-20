import socket
import threading

HOST='127.0.0.1'
PORT=9090

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))

server.listen()

clients=[]
nicknames=[]

def broadcast(msg):
    for client in clients:
        client.send(msg)

def handle(client):
    while True:
        try:
            msg=client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {msg}")
            broadcast(msg)
        except:
            index=clients.index(client)
            clients.remove(client)
            client.close()
            nickname =nicknames[index]
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client,addr=server.accept()
        print(f"Connected with {str(addr)}")
        client.send("NICK".encode('utf-8'))
        nName=client.recv(1024).decode('utf-8')

        clients.append(client)
        nicknames.append(nName)

        print(f"{nName} Joined")
        broadcast(f"{nName} Joined the Server!\n".encode('utf-8'))
        client.send("Connected to the server".encode('utf-8'))

        thread=threading.Thread(target=handle,args=(client,))
        thread.start()

print("Server Running")
receive()


