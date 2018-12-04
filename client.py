import uuid
import random

class Client:
    """ """
    def __init__(self, conn=None, addr=None):
        self.id = str(uuid.uuid4())
        self.nick = f'user_{random.random()}'
        self.conn = conn
        self.addr = addr

    def __str__(self):
        output = f'this is Client with id = { self.id }, nick name = { self.nick }, \nconnection = { self.conn }, \nand address = { self.addr }.'
        return output

    def __repr__(self):
        output = f'this is Client with id = { self.id }, nick name = { self.nick }, \nconnection = { self.conn }, \nand address = { self.addr }.'
        return output
# need a way to change use nickname
    def change_nickname(self, new_nick):
        try:
            self.nick = new_nick
            return
        except:
            print("something went wrong when changing the nickname!")
            pass
