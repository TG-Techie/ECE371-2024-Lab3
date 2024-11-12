from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM, gethostname
import RSA as rsa
import des

import json


PORT_NUMBER = 5000
SIZE = 8192

hostName = gethostbyname(gethostname())
# hostName = gethostbyname("192.168.1.3")
# hostName = gethostbyname("DE1_SoC")

mySocket = socket(AF_INET, SOCK_DGRAM)
mySocket.bind((hostName, PORT_NUMBER))

PUBLIC_KEY_START_DELIM = b"(public_key"
PUBLIC_KEY_END_DELIM = b"public_key)"

DES_KEY_START_DELIM = b"(des_key"
DES_KEY_END_DELIM = b"des_key)"

print("Test server listening on port {0}\n".format(PORT_NUMBER))
client_public_key = None  # type: str | None
des_key = None  # type: str | None
encrypted_image_data = b""

while True:
    (raw_data, addr) = mySocket.recvfrom(SIZE)

    maybe_public_key_start = raw_data.find(PUBLIC_KEY_START_DELIM)
    maybe_des_key_start = raw_data.find(DES_KEY_START_DELIM)

    if -1 != maybe_public_key_start:  # client has sent their public key\
        ###################################your code goes here#####################################
        # retrieve public key and private key from the received message (message is a string!)

        pub_key_end = raw_data.find(PUBLIC_KEY_END_DELIM)
        print("pub_key_end", pub_key_end)
        assert -1 != pub_key_end

        data = raw_data.decode()

        pub_key_payload = data[
            maybe_public_key_start + len(PUBLIC_KEY_START_DELIM) : pub_key_end
        ]
        print("pub_key_payload=", pub_key_payload)

        public_key = json.loads(pub_key_payload)  # type: dict[str, int]

        public_key_e = public_key["e"]
        public_key_n = public_key["n"]
        client_public_key = (public_key_e, public_key_n)
        print("public key is : %d, %d" % client_public_key)

    elif -1 != maybe_des_key_start:  # client has sent their DES key
        ###################################your code goes here####################
        # read the next 8 bytes for the DES key by running (data,addr) = mySocket.recvfrom(SIZE) 8 times and then decrypting with RSA

        if client_public_key is None:
            raise RuntimeError(
                "cannot decrypt DES key without public RSA key, the RSA key has not been exchanged yet"
            )

        des_key_end = raw_data.find(DES_KEY_END_DELIM)
        print("des_key_end", des_key_end)
        assert -1 != des_key_end

        data = raw_data.decode()

        des_key_payload = data[
            maybe_des_key_start + len(DES_KEY_START_DELIM) : des_key_end
        ]

        print("des_key_payload=", repr(des_key_payload))

        des_key_endcoded = json.loads(des_key_payload)  # type: list[int]
        assert isinstance(des_key_endcoded, list)
        assert all(isinstance(key_chunk, int) for key_chunk in des_key_endcoded)

        des_key = "".join(
            rsa.decrypt(client_public_key, chunk) for chunk in des_key_endcoded
        )

        print("des_key = ", repr(des_key))

        # # now we will receive the image from the client
        # (data, addr) = mySocket.recvfrom(SIZE)
        # # decrypt the image
        # ###################################your code goes here####################
        # # the received encoded image is in data
        # # perform des decryption using des.py
        # # coder=des.des()
        # # the final output should be saved in a byte array called rr_byte
        # rr_byte = bytearray()
        # # write to file to make sure it is okay
        # file2 = open(r"penguin_decrypted.jpg", "wb")
        # file2.write(bytes(rr_byte))
        # file2.close()

    elif 0 == len(raw_data):
        # we've hit the end condition for streaming the image data

        assert des_key is not None

        print("# ---- END PACKET RECEIVED ----")

        # decrypt the image
        ###################################your code goes here####################
        # the received encoded image is in data
        # perform des decryption using des.py
        # coder=des.des()

        image_data = des.des().decrypt(
            des_key, encrypted_image_data.decode(), cbc=False
        )

        with open("penguin_decrypted.jpg", "wb") as imgout:
            imgout.truncate(0)
            imgout.write(bytes(map(ord, image_data)))

        print("decypting image completed")
        break
    else:

        # print(f"{raw_data=}")

        encrypted_image_data += raw_data

        continue
        # python2: print data ,
