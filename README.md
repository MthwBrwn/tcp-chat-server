# tcp - chat-  server

**Author**: Matthew Brown and Toby Huang  
**Version**: 1.0.0

## Overview
This application sets up a TCP based chat room using python sockets. Users can change their nicknames, send message to everyone, see available user on the server, and directly message other users.  


## Getting Started
To get started you will need to set up a server on the terminal using server.py.  Another terminal(s) can be used to connect using netcat and setting localhost to 9876  

So far our program only support local multi communication. You will need multiple termnials to operate the system, where one terminal operate  
```bash
python3 server.py
```
to hold the server. Then other terminals can call to participate
```bash
nc localhost 9876
```


## Architecture
This application is written in Python3.6 with built in package uuid, random, and socket.



## Change Log

12/3/18
15:30 - began work on app
16:50 - worked out issue quit disconnect
17:20  - reformatted nickname
17:50   all features present
18:50 - finished most main functions.

