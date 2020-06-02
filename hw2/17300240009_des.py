# Permutation tables and S-boxes
import time
IP = (
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9,  1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
)
IP_INV = (
    40,  8, 48, 16, 56, 24, 64, 32,
    39,  7, 47, 15, 55, 23, 63, 31,
    38,  6, 46, 14, 54, 22, 62, 30,
    37,  5, 45, 13, 53, 21, 61, 29,
    36,  4, 44, 12, 52, 20, 60, 28,
    35,  3, 43, 11, 51, 19, 59, 27,
    34,  2, 42, 10, 50, 18, 58, 26,
    33,  1, 41,  9, 49, 17, 57, 25
)
PC1 = (
    57, 49, 41, 33, 25, 17, 9,
    1,  58, 50, 42, 34, 26, 18,
    10, 2,  59, 51, 43, 35, 27,
    19, 11, 3,  60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7,  62, 54, 46, 38, 30, 22,
    14, 6,  61, 53, 45, 37, 29,
    21, 13, 5,  28, 20, 12, 4
)
PC2 = (
    14, 17, 11, 24, 1,  5,
    3,  28, 15, 6,  21, 10,
    23, 19, 12, 4,  26, 8,
    16, 7,  27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
)
 
E  = (
    32, 1,  2,  3,  4,  5,
    4,  5,  6,  7,  8,  9,
    8,  9,  10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
)
 
Sboxes = {
    0: (
        14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7,
        0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8,
        4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0,
        15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13
    ),
    1: (
        15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10,
        3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5,
        0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15,
        13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9 
    ),
    2: (
        10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8,
        13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1,
        13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7,
        1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12 
    ),
    3: (
        7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15,
        13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9,
        10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4,
        3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14
    ),
    4: (
        2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9,
        14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6,
        4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14,
        11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3
    ),
    5: (
        12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11,
        10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8,
        9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6,
        4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13
    ),
    6: (
        4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1,
        13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6,
        1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2,
        6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12
    ),
    7: (
        13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7,
        1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2,
        7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8,
        2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11
    )
}
 
P = (
    16,  7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2,  8, 24, 14,
    32, 27,  3,  9,
    19, 13, 30,  6,
    22, 11, 4,  25
)

def padding(s, l):
    if len(s) < l:
        for i in range(l-len(s)):
            s = '0'+s
    return s


def permutation_by_table(block, block_len, table):
    '''block of length block_len permutated by table table'''
    # WRITE YOUR CODE HERE!
    block_bin = bin(block)[2:]
    block_bin = padding(block_bin, block_len)
    
    permutated_block = ""
    for i in range(len(table)):
        permutated_block += block_bin[table[i]-1]
    #print("after permutation: ", permutated_block)
    #print(len(permutated_block))
    permutated_int = int(permutated_block,2)
    permutated_hex = hex(permutated_int)[2:]
    l1 = len(permutated_hex)
    l2 = len(table)//4
    #print(l1, l2)

    permutated_hex = padding(permutated_hex, l2)
    #print(len(permutated_hex))
    return permutated_hex




def generate_round_keys(C0, D0):
    '''returns dict of 16 keys (one for each round)'''
    round_keys = dict.fromkeys(range(0,17))
    lrot_values = (1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1)
 
    # left-rotation function
    lrot = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))
 
    # initial rotation
    C0 = lrot(C0, 0, 28)
    D0 = lrot(D0, 0, 28)
    round_keys[0] = (C0, D0)
 
    # create 16 more different key pairs
    # WRITE YOUR CODE HERE!
    C_tmp = C0
    D_tmp = D0
    #print('C: ', C_tmp, 'D: ', D_tmp)
    for i in range(len(lrot_values)):
        C_tmp = lrot(C_tmp, lrot_values[i], 28)
        D_tmp = lrot(D_tmp, lrot_values[i], 28)
        #print(i+1, " ", lrot_values[i])
        #print('C: ', bin(C_tmp)[2:], 'D: ', bin(D_tmp)[2:])
        round_keys[i+1] = (C_tmp, D_tmp)
        
    # round_keys[1] for first round
    #           [16] for 16th round
    # do not need round_keys[0] anymore, remove
    del round_keys[0]
    #print(round_keys[1])
 
    #form the keys from concatenated CiDi 1<=i<=16 and by apllying PC2
    # WRITE YOUR CODE HERE!
    for i in range(1, 17):
        C_tmp = round_keys[i][0]
        D_tmp = round_keys[i][1]
        c_bin = bin(C_tmp)[2:]
        d_bin = bin(D_tmp)[2:]
        c_bin = padding(c_bin, 28)
        d_bin = padding(d_bin, 28)
        #print(c_bin, " ", d_bin)
        c_cat_d = c_bin + d_bin
        cd_int = int(c_cat_d, 2)
        key_tmp = permutation_by_table(cd_int, 56, PC2)
        #print(key_tmp)
        round_keys[i] = key_tmp
 
    return round_keys

def round_function(Ri, Ki):
    # expand Ri from 32 to 48 bit using table E
    #print(bin(Ri)[2:])
    Ri = permutation_by_table(Ri, 32, E)
    #print('len of ri: ',len(Ri))
    #print(bin(int(Ri,16))[2:])
    # xor with round key
    # WRITE YOUR CODE HERE!
    r = int(Ri, 16)
    k = int(Ki, 16)
    #print(padding(bin(r)[2:], 48))
    #print(padding(bin(k)[2:], 48))
    re = k^r
    #print(bin(re)[2:])
    #print(padding(bin(re)[2:], 48))
 
    # split Ri into 8 groups of 6 bit
    # WRITE YOUR CODE HERE!
    s_re = padding(bin(re)[2:], 48)
    re_groups = []
    for i in range(8):
        group = s_re[6*i: 6*i+6]
        #print(group)
        re_groups.append(group)


 
    # interpret each block as address for the S-boxes
    # WRITE YOUR CODE HERE!
    each_block = []
    for i in range(8):
        s_box_i = Sboxes[i]
        group = re_groups[i]
        x = group[0] + group[5]
        y = group[1:5]
        x = int(x,2)
        y = int(y,2)
        index = x*16+y
        tmp = s_box_i[index]
        #print(tmp)
        each_block.append(tmp)

    # pack the blocks together again by concatenating
    # WRITE YOUR CODE HERE!
    Ri = ""
    for i in range(len(each_block)):
        tmp_int = each_block[i]
        tmp_str = bin(tmp_int)[2:]
        tmp_str = padding(tmp_str, 4)
        Ri += tmp_str
    
    #print(Ri)
    Ri = int(Ri, 2)
    #print(len(Ri))
 
    # another permutation 32bit -> 32bit
    Ri = permutation_by_table(Ri, 32, P)
    #print(bin(int(Ri,16))[2:])
 
    return Ri



def encrypt(msg, key, decrypt=False):

    # permutate by table PC1
    key = permutation_by_table(key, 64, PC1) # 64bit -> PC1 -> 56bit
    # split up key in two halves
    # WRITE YOUR CODE HERE!
    l = len(key)
    key_left = key[:l//2]
    key_right = key[l//2:]
    C0 = int(key_left, 16)
    D0 = int(key_right, 16)

    # generate the 16 round keys
    #start1 = time.time()
    round_keys = generate_round_keys(C0, D0) # 56bit -> PC2 -> 48bit
    #end1 = time.time()
    #print('time for key: ', end1-start1)
    
    msg_block = permutation_by_table(msg, 64, IP)
    
    # WRITE YOUR CODE HERE!
    l_m = len(msg_block)
    L0 = msg_block[:l_m//2]
    R0 = msg_block[l_m//2:]
    L0 = int(L0, 16)
    R0 = int(R0, 16)
 
    # apply round function 16 times (Feistel Network):
    L_last = L0
    R_last = R0
    #time = 0.0
    # WRITE YOUR CODE HERE!
    for i in range(1, 17):
        if decrypt == False:
            K_i = round_keys[i]
        else:
            K_i = round_keys[17-i]
        #start2 = time.time()
        f = round_function(R_last, K_i)
        #end2 = time.time()
        #time += (end2-start2)
        #print('time for f: ',end2-start2)
        #print("after f: ", bin(int(f, 16))[2:])
        f = int(f, 16)
        tmp = L_last
        L_last = R_last
        R_last = tmp^f
        #print(i)
        #print(bin(L_last)[2:])
        #print(bin(R_last)[2:])
        #print("after xor: ",bin(R_last)[2:])
    #print('average time for f: ', time/16)

    R_final = padding(bin(L_last)[2:], 32)
    L_final = padding(bin(R_last)[2:], 32)
    cipher_block = L_final + R_final
    cipher_block = int(cipher_block, 2)
 
    # final permutation
    cipher_block = permutation_by_table(cipher_block, 64, IP_INV)
 
    return cipher_block
    

def decrypt(cipher_text, key):
    start3 = time.time()
    plain_text = encrypt(cipher_text, key, decrypt=True)
    end3 = time.time()
    print('time for encrypt: ', end3-start3)
    print('Plain Text: '+ bytearray.fromhex(plain_text).decode())






import binascii
key = int(binascii.hexlify(b'FudanNiu') , 16)
#print(hex(key))


cipher_text_odd = 0x9b99d07d9980305e
#print(hex(cipher_text_odd))
#cipher_text_even = 0x6f612748df99a70c

decrypt(cipher_text_odd,key)
#decrypt(cipher_text_even,key)
