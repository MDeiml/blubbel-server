# blubbel-server
Server application for an open-source, secure, peer-to-peer messenger.
The server is only responsible for the initial ip-address and port exchange, messages
are handled purely P2P.
See the wiki for more details: https://github.com/MDeiml/blubbel-server/wiki

## Protocol

Requests / responses always have the following layout:

* requests: `[type (1 byte) | id (256 bytes)]`
* responses: `[status-code (1 byte) | msg (0-X bytes)]`

Where `request type` can be one of:
* 0x01 (register id)
* 0x02 (resolve id)
* 0x03 (deny request)

and `response type` can be one of:
* 0x00 (OK) : registered id + timestamp
* 0x01 (id resolved) : resolved id + ip + port (+ timestamp)
* 0x02 (inform) : requesting id
* 0x10 (registration error) : error msg
* 0x20 (resolving error) : error msg


Each client has a [RSA](https://en.wikipedia.org/wiki/RSA_%28cryptosystem%29) public / private key pair.

TODO: implement/design authentication for network traffic

### Request types

#### register
A client registers his ip and open port at the server.
The server confirms a successfull registration with a timestamp (valid time of registration).

#### resolve
If a client A wants to start communication with client B, A sends a resolve request for id(B) to the Server. At success
the server responds with the associated ip and port.

#### deny
If a client A does want to start communication with client B (resolve request), a sends a deny request. Otherwise a resolve request.

### Response types
The server does not inspect the contents of request with type "Session requested", "Session accepted" and "Message", but only refers the message to the requested recipient and exchanges the sender's public key for the recipient's public key.

#### OK
The server responds at successfull registration with the registered id + timestamp

#### id resolved
Server responds with the requested id + ip + port

#### inform
Server informs client that his data has been requested

#### registration error
TODO

#### resolving error
TODO
