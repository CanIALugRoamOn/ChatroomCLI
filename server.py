import socket
import threading
import json
import sys
from datetime import datetime
from db import Message
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# server
host = '127.0.0.1'
port = 5000

# init server on socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# database
engine = create_engine("sqlite:///my_db.db")
session = sessionmaker(bind=engine)()

# client and user lists
clients = []
usernames = []

def broadcast(message):
    """
    send messages to all clients that are listening
    """
    for client in clients:
        client.send(message)

def handle(client):
    """
    handle incoming client messages
    """
    while True:
        try:
            message = client.recv(1024)
            # write message into the data base
            try:
                message_meta = json.loads(message.decode('ascii'))
                new_msg = Message(message_meta['timestamp'], message_meta['username'], message_meta['message'])
                session.add(new_msg)
                session.commit()
            except Exception as e:
                print("[Server] Unexpected error:", sys.exc_info())
            # broadcast
            broadcast(message)
        except:
            index = clients.index(client)
            
            clients.remove(client)
            client.close()
            username = usernames[index]

            # left notification
            message = json.dumps({'timestamp': datetime.now().strftime('%H:%M %d/%m/%y'), 'username': '', 'message': '{} left!'.format(username)})
            broadcast(message.encode('ascii'))
            usernames.remove(username)
            break

def receive():
    """
    handle client joined/left notifications
    """
    while True:
        client, address = server.accept()
        print('Connected with {}'.format(str(address)))     

        # request for username
        client.send(json.dumps({'user_tag': 'username'}).encode('ascii'))

        # receive username
        username = json.loads(client.recv(1024).decode('ascii'))['username']
        usernames.append(username)
        clients.append(client)
        print('Username is {}'.format(username))

        # notifications
        message = json.dumps({'timestamp': datetime.now().strftime('%H:%M %d/%m/%y'), 'username': '', 'message': '{} joined!'.format(username)})
        broadcast(message.encode('ascii'))
        
        status = json.dumps({'timestamp': datetime.now().strftime('%H:%M %d/%m/%y'), 'username': '', 'message': 'Connected to server!'})
        client.send(status.encode('ascii'))
        
        # start thread
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
