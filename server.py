from client import Client
import socket
import threading


PORT = 9876


class ChatServer(threading.Thread):
    def __init__(self, port, host='localhost'):
        super().__init__(daemon=True)
        self.port = port
        self.host = host
        self.server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_TCP,
        )
        self.client_pool = []
        self.message_history = {}

        try:
            self.server.bind((self.host, self.port))
        except socket.error:
            print(f'Bind failed. {socket.error}')

        self.server.listen(10)


    def run_thread(self, id, nick, conn, addr):
        """ """
        print(f'{nick}Connected rcvd for {addr[0]}{addr[1]}')

        while True:
            try:
                data = conn.recv(4096)
                # import pdb; pdb.set_trace()

                # process user's input
                self.parse(id, data)

                # this line will keep prompt user
                conn.sendall(b'>>>')
                # [c.conn.sendall(data) for c in self.client_pool if len(self.client_pool)]

                # ?rather than a list comprehension, call a parse() method that handles
                # all of the message parsing and client communications
            except OSError:
                # [c.conn.close() for c in server.client_pool if len(server.client_pool)]
                break
                # pass

    def parse(self, id, in_info):
        """
        this function shall handles all of the message parsing and client communications
        """
        if len(self.client_pool):
            for c in self.client_pool:
                # check whether this is a new user
                if c.id not in self.message_history.keys():
                    self.message_history[c.id] = []

                # save user's chat into dic
                self.message_history[c.id].append(in_info.decode())

                # case for /quit
                if in_info == b'/quit\n':
                    if c.id == id:
                        c.conn.close()
                        self.client_pool.remove(c)
                        self.server.listen(10)
                        # import pdb; pdb.set_trace()
                        print(f'{ c.nick }Connected rcvd for { c.addr[0] }{ c.addr[1] } closed.')

                # case for list all connected users
                elif in_info == b'/list\n':
                    if c.id == id:
                        for i in range(len(self.client_pool)):
                            # hum...somehow self.client_pool[i].nick was understood as a string
                            nickname = self.client_pool[i].nick
                            if isinstance(nickname, bytes):
                                nickname = nickname.decode()
                            # import pdb; pdb.set_trace()
                            c.conn.sendall(f'{ i+1 }:   name = { nickname }; id = { self.client_pool[i].id }\n'.encode())

                elif in_info[:9].lower() == b'/nickname':
                    if c.id == id:
                        c.change_nickname(in_info[10:-1])

                # /dm <to-username> <message>
                elif in_info[:3].lower() == b'/dm':
                    tmp = in_info.decode().split(' ')
                    to_username, to_message = tmp[1], tmp[2:]
                    to_message = (" ".join(to_message))
                    if c.nick == to_username.encode():
                        c.conn.sendall(to_message.encode())
                else:
                    c.conn.sendall(in_info)


    def run(self):
        """ """
        print(f'Server running on {self.host}{self.port}.')

        while True:
            conn, addr = self.server.accept()
            client = Client(conn=conn, addr=addr)
            self.client_pool.append(client)

            # this >>> only show up once user connects to the server.
            client.conn.sendall(b'>>>')
            threading.Thread(
                target=self.run_thread,
                args=(client.id, client.nick, client.conn, client.addr),
                daemon=True,
            ).start()


if __name__ == '__main__':
    server = ChatServer(PORT)

    # server.run()
    try:
        server.run()
    except KeyboardInterrupt:
        pass


                        # print("c = ",c , "...\n\n and type(c) = \n\n", type(c))
                        # print("type of data = ", type(data), "\n\ndata content = ", str(data), "\n\n")
                        # print("decoded data = ", data.decode(), "\n\n")
                        # output = "for client " + str(c) + "we send data to all"
                        # print(output)
                        # c.conn.sendall(data)

    # saved run_thread, worked for /quit
    # def run_thread(self, id, nick, conn, addr):
    #     """ """
    #     print(f'{nick}Connected rcvd for {addr[0]}{addr[1]}')

    #     while True:
    #         try:
    #             data = conn.recv(4096)
    #             # import pdb; pdb.set_trace()
    #             if len(self.client_pool):
    #                 for c in self.client_pool:
    #                     # check whether this is a new user
    #                     if c.id not in self.message_history.keys():
    #                         self.message_history[c.id] = []

    #                     # save user's chat into dic
    #                     self.message_history[c.id].append(data.decode())

    #                     # process user's input
    #                     # self.parse(data)
    #                     if data == b'/quit\n':
    #                         if c.id == id:
    #                             c.conn.close()
    #                             self.client_pool.remove(c)
    #                             self.server.listen(10)
    #                             print(f'{nick}Connected rcvd for {addr[0]}{addr[1]} closed.')
    #                     else:
    #                         c.conn.sendall(data)
    #                 # [c.conn.sendall(data) for c in self.client_pool if len(self.client_pool)]

    #                 # ?rather than a list comprehension, call a parse() method that handles
    #                 # all of the message parsing and client communications
    #         except OSError:
    #             # [c.conn.close() for c in server.client_pool if len(server.client_pool)]
    #             break
    #             # pass
