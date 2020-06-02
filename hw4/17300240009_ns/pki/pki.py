from socket import socket, AF_INET, SOCK_STREAM
import sys, os
sys.path.append("..")
from helpers import *
from helpers.rsa import *

def extract():
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.bind((PKI_HOST, PKI_PORT))
        while True:
            sock.listen()
            conn, addr = sock.accept()
            with conn:
                print('PKI: connection from address', addr)
                while True:
                    # A, B --->  
                    # <--- {K_PB, B}(K_PA)
                    # WRITE YOUR CODE HERE!
                    data = conn.recv(1024)
                    a, b = data.split(b',')
                    a = str(a, encoding='utf8')
                    b = str(b, encoding='utf8')
                    a_file = a + '.asc'
                    b_file = b + '.asc'
                    # obtain key from file, the format is rsa key
                    key_a = import_key(a_file)
                    key_b = import_key(b_file)
                    # rsa key to bytes
                    #key_a = export_public_key(key_a)
                    key_b = export_public_key(key_b)
                    # key_b to str
                    key_b = str(key_b, encoding='utf8')
                    message = key_b + ',' + b
                    messages = rsa.big_encrypt(key_a, message)
                    m = b""
                    for message in messages:
                        #conn.sendall(message)
                        m += message
                    conn.sendall(m)
                    break
  
'''
def extract():
    """() -> NoneType
    Opens the public key infrastructure server to extract RSA public keys.
    The public keys must have already been in the server's folder.
    """
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.bind((PKI_HOST, PKI_PORT))
        sock.listen()
        conn, addr = sock.accept()
        with conn:
            print('PKI: connection from address', addr)
            while True:
                # A, B --->  
                # <--- {K_PB, B}(K_PA)
                # WRITE YOUR CODE HERE!
                data = conn.recv(1024)
                a, b = data.split(b',')
                a = str(a, encoding='utf8')
                b = str(b, encoding='utf8')
                a_file = a + '.asc'
                b_file = b + '.asc'
                # obtain key from file, the format is rsa key
                key_a = import_key(a_file)
                key_b = import_key(b_file)
                # rsa key to bytes
                #key_a = export_public_key(key_a)
                key_b = export_public_key(key_b)
                # key_b to str
                key_b = str(key_b, encoding='utf8')
                message = key_b + ',' + b
                messages = rsa.big_encrypt(key_a, message)
                m = b""
                for message in messages:
                    #conn.sendall(message)
                    m += message
                conn.sendall(m)
                break
'''             





if __name__ == "__main__":
    print("PKI: I am the Public Key Infrastructure Server!")
    print("PKI: listening for a key to be extracted")
    extract()
   