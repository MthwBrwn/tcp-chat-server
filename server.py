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
            data = conn.recv(4096)
            import pdb; pdb.set_trace()
            if len(self.client_pool):
                for c in self.client_pool:
                    if c.id not in self.message_history.keys():
                        self.message_history[c.id] = []

                    # print("c = ",c , "...\n\n and type(c) = \n\n", type(c))
                    # print("type of data = ", type(data), "\n\ndata content = ", str(data), "\n\n")
                    # print("decoded data = ", data.decode(), "\n\n")
                    # output = "for client " + str(c) + "we send data to all"
                    # print(output)
                    # c.conn.sendall(data)

                    self.message_history[c.id].append(data.decode())
                    # import pdb; pdb.set_trace()
                    if data == b'/quit\n':
                        if c.id == id:
                            c.conn.close()
                    else:
                        c.conn.sendall(data)
            # [c.conn.sendall(data) for c in self.client_pool if len(self.client_pool)]

            # ?rather than a list comprehension, call a parse() method that handles
            # all of the message parsing and client communications

    def parse(in_info):
        """
        this function shall handles all of the message parsing and client communications
        """
        # if
        pass


    def run(self):
        """ """
        print(f'Server running on {self.host}{self.port}.')

        while True:
            conn, addr = self.server.accept()
            client = Client(conn=conn, addr=addr)
            self.client_pool.append(client)
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
