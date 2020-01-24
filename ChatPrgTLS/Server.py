#!/usr/bin/env python
'''
Created on Mar 7, 2019

@author: lilsean
'''
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM, SOL_SOCKET, SHUT_RDWR
import ssl, base64, sys
from threading import Thread
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA



def encrpyt(raw):
    cipher = AES.new('This is a key123', AES.MODE_CFB, "This is an IV456")
    return (cipher.encrypt(raw))
 
def decrypt(enc):
    cipher = AES.new('This is a key123', AES.MODE_CFB, "This is an IV456")
    return (cipher.decrypt(enc))
 
def prompt():
    sys.stdout.write('<You> \n')
    sys.stdout.flush()

def accept_incoming_connections(SERVER):
    """Sets up handling for incoming clients."""
    while True:

        """"form a connection with a client"""
        clientSocket, client_address = SERVER.accept()
        
        wrappedServer = context.wrap_socket(clientSocket, server_side=True)

        "confirm that they are connected"
        print("%s:%s has connected." % client_address)

        "tell the client that they have connected"
        wrappedServer.send(bytes("enter what name you wanted to be called Sir/Mam", "utf8"))

        "Stores that client into client dictionary, store the client address into the addresses list at index client"
        addresses[wrappedServer] = client_address

        "Make thread for a client "
        Thread(target=handle_client, args=(wrappedServer,)).start()


def handle_client(wrappedServer):  # Takes client socket as argument.
    """Handles a single client connection."""


    name = wrappedServer.recv(bufferSize).decode("utf8")

    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name

    wrappedServer.send(bytes(welcome, "utf8"))

    msg = "%s has joined the chat!" % name

    broadcast(bytes(msg, "utf8"))

    clientList[wrappedServer] = name

    while True:
        msg = wrappedServer.recv(bufferSize)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            wrappedServer.send(bytes("{quit}", "utf8"))
            wrappedServer.close()
            del clientList[wrappedServer]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clientList:
        sock.send(bytes(prefix, "utf8")+msg)





"Holds all the current clients"
clientList = {}

"Holds all the current IP addresses from clients"
addresses = {}

HOST = ''
PORT = 33000
bufferSize = 1024
server_cert = 'domain.crt'
server_key = 'domain.key'
client_certs = 'client.crt'
ADDR = (HOST, PORT)

#create context
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)


context.verify_mode = ssl.CERT_REQUIRED

#Load key and cert files for both client and server
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
context.load_verify_locations(cafile=client_certs)

"Create keys"


SERVER = socket(AF_INET, SOCK_STREAM)

"Now wrap the socket using an SSL socket"



# Server




SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")

    

    "Make thread"
    AcceptThread = Thread(target=accept_incoming_connections(SERVER))
    AcceptThread.start()
    AcceptThread.join()
    SERVER.close()