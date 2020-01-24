#!/usr/bin/env python3
'''
Created on Mar 7, 2019

@author: lilsean
'''
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from Crypto.Cipher import AES
import tkinter
import ssl, base64, sys

def encrpyt(raw):
    cipher = AES.new('This is a key123', AES.MODE_CFB, "This is an IV456")
    return (cipher.encrypt(raw))

def decrypt(enc):
    cipher = AES.new('This is a key123', AES.MODE_CFB, "This is an IV456")
    return (cipher.decrypt(enc))

def prompt():
    sys.stdout.write('<You> \n')
    sys.stdout.flush()

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = wrappedClientSocket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break

def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    wrappedClientSocket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        wrappedClientSocket.close()
        top.quit()

def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()

"################Tkinter starts here###############"
top = tkinter.Tk() # Create tkinter frame
top.title("Sean's super chat")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.

#### Makes list box, and formats properly ####
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()

messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()
top.protocol("WM_DELETE_WINDOW", on_closing)

"###########Tkinter ends here############"

HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000  # Default value.
else:
    PORT = int(PORT)
BUFSIZ = 1024
ADDR = (HOST, PORT)
server_cert = 'domain.crt'
client_cert = 'client.crt'
client_key = 'client.key'


context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
context.load_cert_chain(certfile=client_cert, keyfile=client_key)

"Create socket"
client_socket = socket(AF_INET, SOCK_STREAM)

wrappedClientSocket = context.wrap_socket(client_socket, server_side=False, server_hostname=HOST)
"Wrap Socket"

#wrapped_Client_Socket = context.wrap_socket(client_socket, ssl_version=ssl.PROTOCOL_TLSv1, ciphers="ADH-AES256-SHA")



wrappedClientSocket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.
