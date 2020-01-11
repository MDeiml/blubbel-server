import socket
import select

# maximum number of clients connected at the same time
MAX_CLIENTS = 100

# maximum number of bytes to read from a client in one pass
BUFFER_SIZE = 1024

KEY_LENGTH = 1024
PORT = 8000

# Class containing all relevant data for handling requests
class RequestHandler:

    def __init__(self):
        # dict from socket.fileno() to public key
        self.public_keys = dict()
        # dict from public key to socket
        self.sockets = dict()

    # This gets called for every received request
    def handle_request(self, sender_socket, request_type, msg):
        print(request_type, msg)
        if request_type == 0x01:
            if len(msg) != KEY_LENGTH // 8:
                # Key length mismatch
                # TODO: Respond with error
                pass
            elif sender_socket.fileno() in self.public_keys:
                # User already logged in
                # TODO: Respond with error
                pass
            elif msg in self.sockets:
                # Public key already in use
                # TODO: Respond with error
                pass
            else:
                print("{} logged in".format(msg))
                self.public_keys[sender_socket.fileno()] = msg
                self.sockets[msg] = sender_socket
                # Send "Login accepted"
                sender_socket.sendall(b"\x01\x00\x00\x00\x00")
        else:
            if sender_socket.fileno() not in self.public_keys:
                # Sender not logged in
                # TODO: Respond with error
                pass
            elif len(msg) < KEY_LENGTH // 8:
                # Message invalid
                # TODO: Respond with error
                pass
            elif msg[:KEY_LENGTH // 8] not in self.sockets:
                # Recipient not loggged in
                # TODO: Respond with error
                pass
            else:
                # Find recipient
                recipient_socket = self.sockets[msg[:KEY_LENGTH // 8]]
                # Replace recipient's key with sender's key
                new_msg = bytes([request_type]) + self.public_keys[sender_socket.fileno()] + msg[KEY_LENGTH // 8:]
                # Forward message to recipient
                recipient_socket.sendall(new_msg)

if __name__ == '__main__':

    print('Starting server...')

    # Create server at port 8000
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(MAX_CLIENTS)

    # List of active sockets
    read_list = [server_socket]

    # List from fileno to active requests (request type, remaining length, message)
    active_requests = dict()

    # Create RequestHandler instance
    handler = RequestHandler()

    while True:
        # Find all sockets that can be read from currently
        reads, _, _ = select.select(read_list, [], [])
        for s in reads:

            if s == server_socket:
                # Accept new client and add to list of active sockets
                client, addr = s.accept()
                read_list.append(client)
                print('{} connected'.format(addr))
            else:
                # Reads BUFFER_SIZE bytes from each socket so that other clients won't have to wait too long
                data = s.recv(BUFFER_SIZE)
                request_type, length, msg = active_requests[s.fileno()] if s.fileno() in active_requests else (None, -5, b'')
                index = 0
                while index < len(data):
                    if length == -5:
                        request_type = data[index]
                        index += 1
                        length += 1
                    elif length < 0:
                        new_index = min(len(data), index + (4 - len(msg)))
                        msg += data[index:new_index]
                        index = new_index
                        length = len(msg) - 4
                        if length == 0:
                            length = int.from_bytes(msg, byteorder='big')
                            msg = b''
                    else:
                        new_index = min(len(data), index + length)
                        msg += data[index:new_index]
                        length -= new_index - index
                        index = new_index
                        if length == 0:
                            handler.handle_request(s, request_type, msg)
                            msg = b''
                            length = -5
                            request_type = None
                active_requests[s.fileno()] = (request_type, length, msg)
