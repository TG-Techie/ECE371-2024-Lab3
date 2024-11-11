from socket import socket, gethostbyname, gethostname, AF_INET, SOCK_DGRAM
import sys
import re
import RSA as rsa
import json

PORT_NUMBER = 5000
SIZE = 1024

hostName = gethostbyname(gethostname())
# hostName = gethostbyname("DE1_SoC")
# hostName = gethostbyname( 'DESKTOP-A30LB1P' )

mySocket = socket(AF_INET, SOCK_DGRAM)
mySocket.bind((hostName, PORT_NUMBER))

PUBLIC_KEY_START_DELIM = "(public_key"
PUBLIC_KEY_END_DELIM = "public_key)"

print("Test server listening on port {0}\n".format(PORT_NUMBER))
client_public_key = None  # type: int | None
msg_decoded = ""  # type: str
while True:
    (data, addr) = mySocket.recvfrom(SIZE)
    data = data.decode()
    maybe_key_start = data.find(PUBLIC_KEY_START_DELIM)
    if -1 != maybe_key_start:  # client has sent their public key\
        ###################################your code goes here#####################################
        # retrieve public key and private key from the received message (message is a string!)

        key_end = data.find(PUBLIC_KEY_END_DELIM)
        print("key_end", key_end)
        assert -1 != key_end

        key_payload = data[maybe_key_start + len(PUBLIC_KEY_START_DELIM) : key_end]
        print("key_payload=", key_payload)

        public_key = json.loads(key_payload)  # type: dict[str, int]

        public_key_e = public_key["e"]
        public_key_n = public_key["n"]
        client_public_key = (public_key_e, public_key_n)
        print("public key is : %d, %d" % client_public_key)
    else:
        assert isinstance(client_public_key, tuple)

        cipher = int(data)
        print("received cipher = ", cipher)

        ###################################your code goes here#####################################
        # data_decoded is the decoded character based on the received cipher, calculate it using functions in RSA.py

        data_decoded = rsa.decrypt(client_public_key, cipher)
        msg_decoded += data_decoded

        print(cipher, ":", data_decoded)

        if "\n" == data_decoded:
            print("decoded mesage = ", repr(msg_decoded))
            # reset the message for next time
            msg_decoded = ""

sys.ext()
# What could I be doing wrong?
