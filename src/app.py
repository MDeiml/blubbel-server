import socket
import select

# Class containing all relevant data for handling requests
class RequestHandler:

    def __init__(self):
        pass

    # This gets called for every received request
    def handle_request(self, sender_id, request_type, msg):
        # for now just print request
        print(request_type, msg)

# maximum number of clients connected at the same time
MAX_CLIENTS = 100
BUFFER_SIZE = 1024

if __name__ == '__main__':

    print('Starting server...')

    # Create server at port 8000
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", 8000))
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
                data = s.recv(BUFFER_SIZE)
                request_type, length, msg = active_requests[s.fileno()] if s.fileno() in active_requests else (None, -5, b'')
                index = 0
                while index < len(data):
                    if length == -5:
                        request_type = int(data[index])
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
                            handler.handle_request(socket.fileno(), request_type, msg)
                            msg = b''
                            length = -5
                            request_type = None
                active_requests[s.fileno()] = (request_type, length, msg)
