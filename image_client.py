import sys
from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname, gethostname
from RSA import generate_keypair, encrypt, decrypt

import RSA as rsa
import des

import json


SERVER_IP = gethostbyname(gethostname())
PORT_NUMBER = 5000
SIZE = 1024
des_key = "secret_k"

print(
    "Test client sending packets to IP {0}, via port {1}\n".format(
        SERVER_IP, PORT_NUMBER
    )
)

mySocket = socket(AF_INET, SOCK_DGRAM)
message = "hello"

# first generate the keypair
# get these two numbers from the excel file
p = 1297273
q = 1297651
###################################your code goes here#####################################
# generate public and private key from the p and q values
# returns  ((e, n), (d, n))
public_key, private_key = rsa.generate_keypair(p, q)

# send key
pub_e, pub_n = public_key
message = """(public_key{"e": %d, "n": %d}public_key)""" % (pub_e, pub_n)
print("sending RSA public key =", repr(message))
mySocket.sendto(message.encode(), (SERVER_IP, PORT_NUMBER))
del message

###################################your code goes here#####################################
# encode the DES key with RSA and save in DES_encoded, the value below is just an example
des_key_encoded = [rsa.encrypt(private_key, char) for char in des_key]

message = "(des_key" + json.dumps(des_key_encoded) + "des_key)"
print("sending encrypted DES key =", repr(message))

mySocket.sendto(
    message.encode(),
    (SERVER_IP, PORT_NUMBER),
)
del message

###################################your code goes here#####################################
# the image is saved in the data parameter, you should encrypt it using des.py
# set cbc to False when performing encryption, you should use the des class
# coder=des.des(), use bytearray to send the encryped image through network
# r_byte is the final value you will send through socket

coder = des.des()

# read image, encode, send the encoded image binary file
with open("penguin.jpg", "rb") as file:
    raw_image = file.read()

# print(f"{len(raw_image)=}")
ciphered_image = coder.encrypt(des_key, raw_image, cbc=False)
# print(f"{len(ciphered_image)=}", type(ciphered_image))

remaining_ciphered_image = ciphered_image.encode()
while len(remaining_ciphered_image):
    outgoing = remaining_ciphered_image[0:1024]

    sent = mySocket.sendto(outgoing, (SERVER_IP, PORT_NUMBER))
    remaining_ciphered_image = remaining_ciphered_image[sent:]


# send the terminating data packet
mySocket.sendto(b"", (SERVER_IP, PORT_NUMBER))


print("encrypted image sent!")
