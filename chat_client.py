import sys
from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname, gethostname
import RSA as rsa
import json

# SERVER_IP = gethostbyname("DE1_SoC")
SERVER_IP = gethostbyname(gethostname())
PORT_NUMBER = 5000
SIZE = 1024
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
# hint: use generate_keypair() function from RSA.py

# returns  ((e, n), (d, n))
public_key, private_key = rsa.generate_keypair(p, q)

pub_e, pub_n = public_key
message = """(public_key{"e": %d, "n": %d}public_key)""" % (pub_e, pub_n)
print("sending", repr(message))
mySocket.sendto(message.encode(), (SERVER_IP, PORT_NUMBER))

print("\n\n")
while True:
    message = input("input mesasge to send: ")
    message += "\n"

    ###################################your code goes here#####################################
    # message is a string input received from the user, encrypt it with RSA character by character and save in message_encoded
    # message encoded is a list of integer ciphertext values in string format e.g. ['23131','352135','54213513']
    # hint: encrypt each character in message using RSA and store in message_encoded

    # message_encoded = ["1", "135", "53"]
    message_encoded = [str(rsa.encrypt(private_key, char)) for char in message]

    for code in message_encoded:
        print("sending code =", code)
        mySocket.sendto(code.encode(), (SERVER_IP, PORT_NUMBER))

    print("sent mesage = ", repr(message))

    # [
    #     mySocket.sendto(code.encode(), (SERVER_IP, PORT_NUMBER))
    #     for code in message_encoded
    # ]  # do not change [sends message through socket]
sys.exit()
