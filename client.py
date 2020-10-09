import socket
import threading
import json
import argparse
from datetime import datetime
import sys

# pass username as argument
parser = argparse.ArgumentParser()
parser.add_argument('username', type=str, help='a string as username')                  
args = parser.parse_args()

# init client on socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5000))

def receive():
    """
    handles messages that the client receives
    """
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            data = json.loads(message)
            if 'user_tag' in data.keys():
                # greet new users
                json_str = json.dumps({data['user_tag']:args.username})
                client.send(json_str.encode('ascii'))
            else:
                # chat and other messages
                print('[{}] {}: {}'.format(data['timestamp'], data['username'], data['message']))
        except:
            print("[Client] Unexpected error:", sys.exc_info())
            client.close()
            break
        
def write():
    """
    handles writing messages
    """
    while True:
        message = input('')
        json_str = json.dumps({'timestamp': datetime.now().strftime('%H:%M %d/%m/%y'), 'username': args.username, 'message': message})
        client.send(json_str.encode('ascii'))

## start threads
receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()
