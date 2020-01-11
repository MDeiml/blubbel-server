# blubbel-server
Server application for an open-source, secure, peer-to-peer messenger.
See the wiki for more details: https://github.com/MDeiml/blubbel-server/wiki

## Protocol

Requests / responses always have the following layout
`[request type / response type (1 byte)][message length (4 bytes)][message (X bytes]`

Where `request type` can be one of:
* 0x01 (Login)
* 0x02 (Start session)
* 0x03 (Accept session)
* 0x04 (Message)

and `response type` can be one of:
* 0x01 (Login accepted)
* 0x02 (Session requested)
* 0x03 (Session accepted)
* 0x04 (Message)

### Request types

#### Login

A login must be requested after connecting before any other request type is allowed.
The login message payload consists only of the users public key.

#### Start session

A "Start session" request initiates the key exchange between two clients.
The message consists of the other clients public key and `g^a mod p` encrypted with this clients public key, where `g` and `p` are the base and modulus of the DH key exchange and `a` is this clients secret.

#### Accept session

A "Accept session" request from the other client must follow a "Start session" request. After this request a communication session should be open.
The message consists of the public key of the client which initiated the request and `g^b mod p` encrypted with this clients public key. `b` is this clients secret.

#### Message

A message can only be send to a client this client has a open session with.
The message payload is the other client's public key followed by the message text.

### Response types

The server does not inspect the contents of request with type "Session requested", "Session accepted" and "Message", but only refers the message to the requested recipient and exchanges the sender's public key for the recipient's public key.

#### Login accepted

The reponse for the "Login" request. This response contains no message.
