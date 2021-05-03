"""the client side of our chatroom"""
#created and modified using tkinter
 
import socket
from threading import Thread
import tkinter
from tkinter import Widget
from tkinter import *
 
 
#setup the same as the server.py
host = input("Enter host ip address: ")
port = input("Enter port to connect: ")
my_chatroom = input("Enter room to connect: ")
 

#Takes in our port number
if not port:
    port = 8080
else:
    port = int(port)
 
 
buffer = 1024

#creates our valid tuple 
vaild_addr = (host, port)
 
#create our socket using the socket module, as we are using TCP, we need the AF_INET and SOCK_STREAM
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(vaild_addr)
 
 
 
#we need a function to send messages to our clients
#aslong as the message is not {exit} we broadcast the message 
#to all other clients
 
def send_message(event=None):
    msg = my_msg.get()
    my_msg.set("")
    #this then sends the message to every client in the server
    client_sock.send(bytes(msg, "utf8"))
 
    #close the client thread if the user chooses to leave
    if msg == "{exit}":
        client_sock.close()
        graphic_interface.destroy()
 
    #close the client thread if the user chooses to leave
    if msg == "{exit}":
        client_sock.close()
        graphic_interface.destroy()

#Our function to send an exit message
def on_exit(event=None):
    my_msg.set("{exit}")
    send_message()
 
 #This function takes in our message and decodes it using the recv function
def recieve_message():
    while True: 
        try:
            msgB = client_sock.recv(buffer).decode("utf8")
            m_list.insert(tkinter.END, msgB)
        except OSError:
            break
 
 
 

graphic_interface = tkinter.Tk()
    
graphic_interface.title("Niall's Chatroom")
    
    
graphic_frame = tkinter.Frame(graphic_interface)
my_msg = tkinter.StringVar()
my_msg.set("Type your messages here.")


##This creates a scrolling feature
scroll = tkinter.Scrollbar(graphic_frame)

#we then create the box which will present our messages
m_list = tkinter.Listbox(graphic_frame, height=30, width=100, bg = "black", fg ="#afe9ff", font = "none 10 bold", yscrollcommand=scroll.set)
scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)

#create a scrollbar to scroll through messages

scroll.config(command=m_list.yview)
m_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)

#we can then add this to our GUI
m_list.pack()
graphic_frame.pack()
    
    
#This section covers the latter side of the GUi, including where you type messages and 
#the button widget to send them
message_field = tkinter.Entry(graphic_interface, textvariable=my_msg)
message_field.bind("<Return>", send_message)
message_field.configure(width = 25, justify="center", bg= "#afe9ff")
message_field.pack()    
send_button = tkinter.Button(graphic_interface, text="Send", width=10, bg = "#856ff8", fg = "#feffbe", font = "none 9 bold", command=send_message)
send_button.pack()
    
    
graphic_interface.protocol("WM_DELETE_WINDOW", on_exit)
    
    
receive_thread = Thread(target=recieve_message)
receive_thread.start()
tkinter.mainloop()  # Starts tkinter execution.
    



send_message.__doc__("This is our client side function to broadcast our messages to the server, \
    it uses the client socket to broadcast our message")

recieve_message.__doc__("This function takes a message in and decodes it, presenting it on our GUI")
 
on_exit.__doc__("Closes down the client side socket if {exit} is used")
 
 
 
 
 
 
 
 
 
 
 
 
