import socket
import chat_client_handler
from KeyGenerator import *
from silent_disco_database import *
from song_server import *

CONNECTED_USERS = {}  # will contain the connected users information ({username: socket})
MESSAGES = ''  # will contain the chatting history, for the new users to receive.
SONG_LIST = []


class Server(object):
    def __init__(self):
        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', 4500))
        self.server_socket.listen(10)

        # for encryption:
        self.rsa = Cryptonew()  # creating a new Cryptonew object to encrypt and decrypt with RSA
        self.public_key = self.rsa.get_public()  # getting the public RSA key
        self.private_key = self.rsa.get_private()  # getting the private RSA key

    def accept(self):
        return self.server_socket.accept()


def main():
    server = Server()
    song_server = SongServer()

    chat_socket, chat_address = server.accept()  # accepting the dj socket (only one accept)
    client_hand = chat_client_handler.ClientHandler(None, None, chat_address, chat_socket,
                                                    server.public_key, server.private_key, server.rsa, Database())
    client_hand.start()

    while True:
        chat_socket, chat_address = server.accept()
        print 'accept 1'
        song_socket, song_address = song_server.accept()
        print 'accept 2'

        client_hand = chat_client_handler.ClientHandler(song_socket, song_address, chat_address, chat_socket,
                                                        server.public_key, server.private_key, server.rsa, Database())
        client_hand.start()


if __name__ == '__main__':
    main()
