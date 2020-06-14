from concurrent.futures import ThreadPoolExecutor
import socket
import os
import pickle
import time
import json
import filelock

def p2p_start():
    global host
    global port
    host = get_myip()
    my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("Enter your port number.")
    port = int(input())
    print("Your address is :",host)
    print("Your port is :",port)
    add_core_node(host,port,0)
    #my_socket.bind((host,port))
    #my_socket.listen(10)
    print("P2P Server was successfully set up")
    
    while True:
        print("Select Command.\n")
        print("0: Pending.\n"
              "1: Request connection to peer.\n"
              "2: Remove peer.\n"
              "3: Send mail.\n"
              "100: Shutdown server.\n")
        cmd = int(input())
        if cmd == 0:
            pending()
        elif cmd == 1:
            print("input peer address")
            peer_addr = input()
            print("input peer port")
            peer_port = int(input())
            build_message(cmd,peer_addr,peer_port,host,port,0)
        elif cmd == 100:
            exit()
        
def pending():
    my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    my_socket.bind((host,port))
    my_socket.listen(10)
    while True:
        print('Waiting for connection...')
        conn, addr = my_socket.accept()
        handle_message(conn)

def handle_message(message):
    conn = message
    msg = conn.recv(1024)
    #print(msg)
    msg = msg.decode('utf-8')
    msg = json.loads(msg)
    msg_type = msg['msg_type']
    peer_addr = msg['addr']
    peer_port = msg['port']
    payload = msg['payload']
    #print(msg)
    
    if msg_type == 1:  
        print("Request for connection was called.")
        add_core_node(peer_addr,peer_port,1)
        #share_core_list()
    elif msg_type == 2:
        print("Request for Removal was called.")
        #remove_edge_node(addr,port)
    elif msg_type == 3:
        print("Request for Core node list was called.")
        #share_core_list(addr,port)
    elif msg_type == 4:
        print("Request for adding as edge node was called.")
        #add_edge_node(addr,port)
    elif msg_type == 5:
        print("Mail from a peer: ",addr,port)
        print(payload)
    else:
        print('')
        

def build_message(msg_type,addr_to,port_to,my_addr,my_port,payload):
    if payload == 0:
        payload = ''
    message = {'msg_type':msg_type,
               'addr':my_addr,
               'port':my_port,
               'payload':payload}
    message = json.dumps(message)
    my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    my_socket.connect((addr_to,port_to))
    my_socket.sendall(message.encode('utf-8'))

def get_myip():
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect(('8.8.8.8',80))
    return s.getsockname()[0]
if __name__ == '__main__':
    get_myip()

#Command Num = 1
def add_core_node(peer_addr,peer_port,p):
    with filelock.FileLock('peer_list.lock',timeout=10):
        try:
            with open('peer_list.txt','r') as file:
                peer_list = json.load(file)
        except:
            peer_list = []
        
        peer_list.append({
           'IP address':peer_addr,
           'Port':peer_port
           })
        with open('peer_list.txt','w') as file:
            json.dump(peer_list,file,indent=2)
    if p == 1:
        print("Current Peer list")
        print(peer_list)

def remove_core_node(peer_addr,peer_port):
    with filelock.FileLock('peer_list.lock',timeout=10):
        try:
            with open('peer_list.txt','r') as file:
                peer_list = json.load(file)
        except:
            peer_list = []
        peer_list.pop(peer_addr)
        peer_list.pop(peer_port)
        with open('peer_list','w') as file:
            json.dump(peer_list,file,indent=2)
    




