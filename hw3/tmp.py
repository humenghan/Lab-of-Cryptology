import gmpy2
def bytes2num(b):
    s='0x'
    for x in b:
        tmp=str(hex(x))[2:]
        if len(tmp)==2:
            pass 
        else:
            tmp='0'+tmp
        s+=tmp
        num=int(s,16)
    return num


def num2str(n):
    tmp=str(hex(n))[2:]
    if len(tmp)%2==0:
        pass 
    else:
        tmp='0'+tmp
    s=''
    for i in range(0,len(tmp),2):
        temp=tmp[i]+tmp[i+1]
        s+=chr(int(temp,16))
    return s



#obtain n from hex-expression
n_hex = 'C2636AE5C3D8E43FFB97AB09028F1AAC6C0BF6CD3D70EBCA281BFFE97FBE30DD'
n = int(n_hex, 16)
print(n)

fi=open('/Users/macbook/Desktop/密码学/实验/hw3/secret.enc','rb') 
cipher=fi.read() 
cipher=bytes2num(cipher) 
fi.close()
print(cipher)

'''
d = 10866948760844599168252082612378495977388271279679231539839049698621994994673
p = 275127860351348928173285174381581152299
q = 319576316814478949870590164193048041239
n = p*q
'''
p = gmpy2.mpz(275127860351348928173285174381581152299)
q = gmpy2.mpz(319576316814478949870590164193048041239)
e = gmpy2.mpz(65537)
phi_n = (p - 1) * (q - 1)
d = gmpy2.invert(e, phi_n)
print ("private key:")
print (d)

c = gmpy2.mpz(cipher)
print ("plaintext:")
n = gmpy2.powmod(c,d,p*q)
#print(n)
print('re:',num2str(n))
#print(hex(n)[2:])
#print(len(hex(n)[2:]))




