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
print("sending", repr(message))
mySocket.sendto(message.encode(), (SERVER_IP, PORT_NUMBER))

###################################your code goes here#####################################
# encode the DES key with RSA and save in DES_encoded, the value below is just an example
des_key_encoded = [str(rsa.encrypt(private_key, char)) for char in des_key]

mySocket.sendto(
    ("(des_key" + json.dumps(des_key_encoded) + "des_key)").encode(),
    (SERVER_IP, PORT_NUMBER),
)

###################################your code goes here#####################################
# the image is saved in the data parameter, you should encrypt it using des.py
# set cbc to False when performing encryption, you should use the des class
# coder=des.des(), use bytearray to send the encryped image through network
# r_byte is the final value you will send through socket
r_byte = bytearray()

coder = des.des()


# read image, encode, send the encoded image binary file
with open("penguin.jpg", "rb") as file:
    raw_image = file.read()

print(f"{len(raw_image)=}")
ciphered_image = coder.encrypt(des_key, raw_image, cbc=False).encode()
print(f"{len(ciphered_image)=}")

# send image through socket
mySocket.sendto(ciphered_image, (SERVER_IP, PORT_NUMBER))


print("encrypted image sent!")
