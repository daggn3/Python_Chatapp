"""The server side of our chatroom"""
#I decided on using a multithreading approach as it was new to me
#and i felt it was a fun challange
 
 
 
#Import our various modules to be used
import socket
from threading import Thread
 
"""The first thing we must do is create our socket with a socket constructor
We pass in our socket family and socket type"""
 
"""as we are using TCP sockets, we use AF_INET and SOCK_STREAM"""
 
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
#we then need some variables for our server side implementation
 
clients = {}
addressdict = {}
 
#Our host is an ip address (string) and our port is a large number (int)
host = ""
port = 8080
chatroom = ""
 
vaild_addr = (host, port)
 
 
BUFFER = 1024

#We create our tuple and bind it to our server sock
server_sock.bind(vaild_addr)
 
 
 
 
#we now create an infinte loop to find and accept different clients to use our chat
 
def connection():
    #we need to take in our client addresss
    while True:
 
        #this accepts our client to our server socket
        client, client_addr = server_sock.accept()
 
        #we then add our client to our address dictionary
        print("%s:%s is now connected to the chat room." % client_addr)
 
 
        #we can send a message over tcp using the send function
        client.send(bytes("Hello and welcome to Niall's chatroom!\n"\
            +"Type in our name and click enter to join.", "utf8"))
 
        addressdict[client] = client_addr
        
        #we then create a thread with a target being our client
        Thread(target=manage_client, args=(client,)).start()
 
 
 
#we then create our function to handle the client within the server
#this includes broadcasting our message to the server and to other clients
#we then have a {exit} option to close the thread when needed
 
def manage_client(client):

        #recieve the clients name back from client.py
    client_name = client.recv(BUFFER).decode("utf8")
 
    #create our various messages to send to our client 
    hello = "Hello there %s! whenever you want to leave, type {exit}." % client_name
    message = "%s Has now joined the server, say hello!" % client_name
    
    client.send(bytes(hello, "utf8"))
    sendmessage(bytes(message,"utf8"))
 
    #we now create a loop to send messages to our server
    #aslong as the message is not {exit} we send it to the server
    #if the message is {exit} we close the thread and say goodbye
 
    clients[client] = client_name
 
    #we send the message to everyone as long as the message is not {exit}
    while True:
        message = client.recv(BUFFER)
        if message != bytes("{exit}","utf8"):
            sendmessage(message, client_name+": ")
        
        #if the message is {exit}, we remove our client from our dictionary
        #and delete close their thread
        else:
            client.send(bytes("{exit}", "utf8"))
            client.close()
            del clients[client]
            sendmessage(bytes("%s has left the chat, goodbye!" % client_name, "utf8"))
            break
 
 
#we now create our send message function, this broadcasts the message
#to everyone connected to our server
 
def sendmessage(message, prefix =""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+message)
 
 
 
#we then set up our main to create a thread of our server
if __name__ == "__main__":
    server_sock.listen(5)
    print("Waiting for someone...anyone...please...")
    create_thread = Thread(target=connection)
    create_thread.start()  # Starts the infinite loop.
    create_thread.join()
    server_sock.shutdown()
    server_sock.close()
 
 
connection.__doc__("This Is a function to take in an IP address and a port using the accept function,\
    and connect them to the server,\
    it then spawns a thread for each client connected")


manage_client.__doc__("This function is the bulk of our server, it creates a thread,\
    and broadcasts a message to our server aslong as the message is not {exit}, \
        if it is, then it closes the thread")

sendmessage.__doc__("A simple function that uses the send function to broadcast the message.")