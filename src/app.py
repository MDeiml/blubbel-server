import socketserver

class BlubbelHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print('test')
        # Receive 1024 bytes of data
        data = self.request.recv(1024)

        # For now just print the data and echo it
        print(data)
        self.request.sendall(data)

if __name__ == '__main__':
    # Create server at port 8000
    server = socketserver.TCPServer(('0.0.0.0', 8000), BlubbelHandler)

    print('Starting server...')

    # Run server until application is terminated
    server.serve_forever()
