def multiplicative_inverse(e, phi):
    '''
    extended Euclid's algorithm for finding the multiplicative inverse 
    '''
    # WRITE YOUR CODE HERE!
    b = phi
    c = e%phi
    if(c==1):
        re = 1
    else:
        s0=1
        s1=0
        t0=0
        t1=1
        while (b%c!=0):
            q=b//c  
            r=b%c  
            b=c  
            c=r  
            s=s0-q*s1 
            s0=s1 
            s1=s  
            t=t0-q*t1  
            t0=t1  
            t1=t  
            if r==1:
                re = (t+phi)%phi
    return re


#print(multiplicative_inverse(1001, 3837))
def gcd(a,b):
    if(a%b==0):
        return b
    else:
        return gcd(b, a%b)


import random
def key_generation(p, q):
    # WRITE YOUR CODE HERE!
    n = p*q
    phi = (p-1)*(q-1)
    e = random.randint(2, phi-1)
    #print('e is: ',e)
    while(gcd(e, phi)!=1):
        #print('gcd is: ',gcd(e, phi))
        e = random.randint(2, phi+1)
        #print(e)
    return {'pk':(e, n),'sk':(multiplicative_inverse(e, phi), n),'phi':phi}


#print(key_generation(13, 11))


#ascii_to_hex
def a2hex(raw_str):
    hex_str = ''
    for ch in raw_str:
        hex_str += hex(ord(ch))[2:]
    return hex_str


#hex_to_ascii
def hex2a(raw_str):
    asc_str = ''
    #print(raw_str)
    for i in range(0,len(raw_str),2):
        #print(raw_str[i:i+2])
        asc_str += chr(int(raw_str[i:i+2],16))
        #print(chr(int(raw_str[i:i+2],16)))
    return asc_str


def MRF(b,n,m):
    a=1
    x=b;y=n;z=m
    binstr = bin(n)[2:][::-1]	
    #print(len(binstr))
    for item in binstr:
        if item == '1':
            a = (a*b)%m
            b = (b**2)%m
        elif item == '0':
            b = (b**2)%m
    return a


#print('mrf',MRF(11, 23, 187))

# there are three possible padding methods in RSA:
# 1. RSA_PKCS1_PADDING blocklen = RSA_size(rsa) – 11 (bytes), the output length should be the same with key
# 2. RSA_PKCS1_OAEP_PADDING blocklen = RSA_size(rsa) – 41 (bytes), the output length should be the same with key
# 3. RSA_NO_PADDING blocklen = RSA_size(rsa) (bytes), the output length should be the same with the key
# for all the three above methods, if the encrypted block length is less than 
def encrypt(pk, plaintext, padding='RSA_PKCS1_PADDING'):
    # WRITE YOUR CODE HERE!
    e = pk[0]
    n = pk[1]
    # here I do not really use 'big number', in case that n is too small, set minimum blocklen to 4
    # each character in the message can be transferred to 2 hex characters, which are equal to 8 bit(1 byte)
    # therefore, one character in the message will take up 1 byte when expressed in binary string
    binstr = bin(n)[2:][::-1]
    if padding == 'RSA_PKCS1_PADDING':
        blocklen = max((len(binstr)//8-11), 4)
    elif padding == 'RSA_PKCS1_OAEP_PADDING':
        blocklen = max((len(binstr)//8-41), 4)
    else:
        blocklen = len(binstr)//8
    
    cipher = ""
    nlength = len(str(hex(n))[2:])  
    message = plaintext          

    for i in range(0,len(message),blocklen):
        if i==len(message)//blocklen*blocklen:
            m = int(a2hex(message[i:]),16)  
        m = int(a2hex(message[i:i+blocklen]),16)
        #print(message[i:i+8])
        c = MRF(m,e,n)
        cipher1 = str(hex(c))[2:]
        if len(cipher1)!=nlength:
            cipher1 = '0'*(nlength-len(cipher1))+cipher1    
        cipher += cipher1
    return cipher
    

def decrypt(sk, ciphertext, padding='RSA_PKCS1_PADDING'):
    # WRITE YOUR CODE HERE!
    d = sk[0]
    n = sk[1]

    cipher = ciphertext
    message = ""
    nlength = len(str(hex(n))[2:])
    for i in range(0,len(cipher),nlength):
        c = int(cipher[i:i+nlength],16)     
        m = MRF(c,d,n)
        info = hex2a(str(hex(m))[2:])
        message += info
    return message




# complete the RSA to a pipeline
import cmath
def isprime(n):
    for i in range(2, (int)(n**0.5)+1):
        if(n%i==0):
            return False
    return True



def generate_rand():
    
    l = random.sample(range(10**11, 10**15), 2)
    p = l[0]
    q = l[1]
    while(isprime(p)==0 or isprime(q)==0):
        l = random.sample(range(10**11, 10**15), 2)
        p = l[0]
        q = l[1]
    return p, q

import time 
'''
if __name__ == "__main__":
    times = []
    for i in range(10):
        begin1 = time.time()
        p, q = generate_rand()
        end1 = time.time()
        time1 = end1 - begin1
        times.append(time1)
        begin2 = time.time()
        keys = key_generation(p,q)
        end2 = time.time()
        time2 = end2 - begin2
        e = keys['pk'][0]
        n = keys['pk'][1]
        d = keys['sk'][0]
        phi = keys['phi']
        m = 'iamjuke'
        pk = (e, n)
        sk = (d, n)
        begin3 = time.time()
        cipher = encrypt(pk, m)
        end3 = time.time()
        time3 = end3 - begin3
        begin4 = time.time()
        plain = decrypt(sk, cipher)
        end4 = time.time()
        time4 =end4 - begin4
        print(cipher)
        print(plain)
        print('time for random generation: ', time1)
        print('time for key generation: ', time2)
        print('time for encryption: ', time3)
        print('time for decryption: ', time4)
        print('\n')
    
    sum = 0.0
    for i in range(len(times)):
        sum += times[i]
    print('avg time for random generation: ', sum/10)

'''    




