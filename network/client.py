#!/usr/bin/env python3

#----- A simple TCP client program in Python using send() function -----

import socket
import logging
import datetime

date = datetime.datetime.now()
print (date)
print (date.strftime("%Y-%m-%d %H:%M:%S"))
logging.basicConfig(
        filename='./logs/client.log',
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO)

 

# Create a client socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

 

# Connect to the server

clientSocket.connect(("127.0.0.1",9090));

 

# Send data to server

data = "Hello Server!";

clientSocket.send(data.encode());

 

# Receive data from server

dataFromServer = clientSocket.recv(1024);

 

# Print to the console

print(dataFromServer.decode());
