from math import gcd
from collections import Counter
from time import *

# Some helper functions provided:
def c2i(c, alphabet):
    """Returns the index of c in the string alphabet, starting at 0"""
    return alphabet.index(c)


def i2c(i, alphabet):
    """Returns the character at index i in alphabet"""
    return alphabet[i]

def prepare_string(s, alphabet):
    """removes characters from s not in alphabet, returns new string"""
    s = s.upper()
    finalString = ""
    for i in s:
      if i in alphabet:
        finalString += i
    return finalString

def make_cosets(text, n):
    """Makes cosets out of a ciphertext given a key length; should return an array of strings"""

    cosets = []
  
    for index in range(n):
      i = 0
      nextword = ""
      while (i + index) <= (len(text) - 1):
        nextword += text[i + index]
        i += n
      
      cosets.append(nextword)
    
    return cosets


def rotate_list(old_list):  
    """Takes the given list, removes the first element, and appends it to the end of the list, then returns the
    new list"""
    new_list = old_list[:]
    new_list.append(old_list[0])
    del new_list[0]
    return new_list

def find_total_difference(list1, list2):
    """Takes two lists of equal length containing numbers, finds the difference between each pair of matching
    numbers, sums those differences, and returns that sum"""
    
    finalSum = 0
    i = 0
    while i < len(list1):
      finalSum += abs(list2[i] - list1[i])
      i += 1
    
    return finalSum  




def vigenere_encrypt(plaintext, key, alphabet):
    """Returns ciphertext encrypted by vigenere cipher using key"""
    # WRITE YOUR CODE HERE!
    # first of all, padding the key
    lp = len(plaintext)
    lk = len(key)
    m = lp // lk
    key_padding = ''
    for i in range(m):
        key_padding += key
    key_padding += key[:(lp%lk)]

    # then change the plaintext and keyword to upper class
    key_padding = prepare_string(key_padding, alphabet)
    plaintext = prepare_string(plaintext, alphabet)
    
    # finally use the key_padding to encipher the plaintext
    ciphertext = ''
    for j in range(len(plaintext)):
        p = c2i(plaintext[j], alphabet)
        k = c2i(key_padding[j], alphabet)
        p = (p+k)%26
        c = i2c(p, alphabet)
        ciphertext += c
    
    return ciphertext




def vigenere_decrypt(ciphertext, key, alphabet):
    """Returns plaintext decrypted by vigenere cipher using key"""
    # WRITE YOUR CODE HERE!
    # first of all, padding the key
    lc = len(ciphertext)
    lk = len(key)
    m = lc // lk
    key_padding = ''
    for i in range(m):
        key_padding += key
    key_padding += key[:(lc%lk)]

    # then change the plaintext and keyword to upper class
    key_padding = prepare_string(key_padding, alphabet)
    ciphertext = prepare_string(ciphertext, alphabet)
    
    # finally use the key_padding to encipher the plaintext
    plaintext = ''
    for j in range(len(ciphertext)):
        c = c2i(ciphertext[j], alphabet)
        k = c2i(key_padding[j], alphabet)
        c = (c-k)%26
        p = i2c(c, alphabet)
        plaintext += p
    
    return plaintext






def kasiski_test(ciphertext):  #Code partially provided
    """Finds gcd of most common distances between repeated trigraphs
    Recommended strategy: loop through the ciphertext, keeping a list of trigraphs and a list of distances in this way:
    1) When encountering a new trigraph add it to the trigraph list
    2) When encountering a repeat add the distance from current index to first index of that trigraph to the list of distances"""

    trigraphs = []
    distances = []
    
    # WRITE YOUR CODE HERE!
    for i in range(len(ciphertext)-2):
        trigraph = ciphertext[i:i+3]
        #print(trigraph)
        for j in range(len(trigraphs)):
            if trigraph == trigraphs[j][0]:
                distances.append(i-trigraphs[j][1])
                break
        trigraphs.append((trigraph, i))
    if len(distances) == 0:
        distances.append(len(ciphertext))
    #print('distances: ',distances)
        
    # Code is provided to find the gcd of any common distances appearing at least twice
    dCount = Counter(distances)
    topCount = dCount.most_common(6)
    #print('top: ', topCount)
    my_gcd = topCount[0][0]
    for index in range(1, len(topCount)):
        if topCount[index][1] > 1:
            my_gcd = gcd(my_gcd, topCount[index][0])
    return my_gcd 



def index_of_coincidence(ciphertext, alpha):
    """Caculates index of coincidnece of ciphertext"""
    common = Counter(ciphertext)
    ioc = 0
    # WRITE YOUR CODE HERE!
    s = 0
    l = len(ciphertext)
    for key in common.keys():
        s += common[key]*(common[key]-1)
    ioc = s / (l*(l-1))
    return ioc

def friedman_test(ciphertext, alpha):
    l = 0
    
    n = len(ciphertext)
    i = index_of_coincidence(ciphertext, alpha)
    ## change the code below to calculate the int value
    l = n * (0.027) // ((n-1)*i + 0.0655 - 0.0385 * n)
    l = int(l)
    return l



def run_key_tests(ciphertext, alphabet): 
    """Runs Kasiski and Friedman tests and outputs results"""
    kasiski = kasiski_test(ciphertext)
    friedman = friedman_test(ciphertext, alphabet)
    
    out =  "Kasiski test gives this as the most likely: " + str(kasiski) +  "\n Friedman test gives: " + str(friedman)
    #print(out)
    return out

    
def find_likely_letters(coset, alpha, eng_freq):
    """Finds the most likely shifts for each coset and prints them
    Recommended strategy: make a list of the frequencies of each letter in the coset, in order, A to Z.
    Then, alternate using the find total difference method (on your frequencies list and the standard english
    frequencies list) and the rotate list method to fill out a new list of differences.  This makes a list of
    the total difference for each possible encryption letter, A to Z, in order.
    Then, find the indices of the smallest values in the new list, and i2c them for the most likely letters."""
    
    coset_freq = []
    differences = []
    # WRITE YOUR CODE HERE!
    coset_prepared = prepare_string(coset, alpha)
    coset_freq = [0 for _ in range(26)]
    l = len(coset_prepared)
    for i in range(len(coset_prepared)):
        index = c2i(coset_prepared[i], alpha)
        coset_freq[index] += 1/l
    
    diff0 = find_total_difference(coset_freq, eng_freq)
    differences.append(diff0)
    for i in range(25):
        coset_freq = rotate_list(coset_freq)
        diff = find_total_difference(coset_freq, eng_freq)
        differences.append(diff) 
    firstletter = 0
    secondletter = 1
    # WRITE YOUR CODE HERE!
    sorted_diff = sorted(differences)
    firstletter = differences.index(sorted_diff[0])
    secondletter = differences.index(sorted_diff[1])
    letter1 = alpha[firstletter]
    letter2 = alpha[secondletter]
    
    return "the most likely letter is: " + letter1 + " followed by: " + letter2
    


def crack(ciphertext, alpha, eng_freq): 
    """Main crack function"""
    print("Your cipher text is: " + ciphertext)
    out = run_key_tests(ciphertext, alpha)
    print(out)
    x = int(input("Choose the key length you'd like to try: "))
    
    cosets = make_cosets(ciphertext, x)
    for index in range(len(cosets)):
        print("For coset " + str(index + 1) + ", " + find_likely_letters(cosets[index], alpha, eng_freq) + ".")
    s = input("Type the key you would like to use to decipher: ")
    print(vigenere_decrypt(ciphertext, s, alpha))
    print()




alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

eng_freq = [.0817, .0149, .0278, .0425, .1270, .0223, .0202, .0609, .0697, .0015, .0077, .0403, .0241, .0675, .0751,
            .0193, .0010, .0599, .0633, .0906, .0276, .0098, .0236, .0015, .0197, .0007]

if __name__ == "__main__":
    odd = "DWFOSZPFWGVVMVOBXTBMGIILECURUWKGZGNMUHUHMKDTNUWDRMGHPTQABVVKOTVOAMKHCGJWGUGMEWQGIOAGSCLVSLGIQKFDIEUQXUHWCSWVGGARMMVVFWAJKICMUROBLYVQYFBAGGGFUMFYCZXTEXNZMAPCZJTWENWLVHZNOATEHQBOABVGBVMTLWTNRSAYTCUGIMBPVMEFVMYSIXOMLUSABGBAGHZHTBUCGMQNWWGZKBNXEGHMYZVHPFMIFZLKPTRUZTPGIPUQHPGIEFVHVFMNMTRRCAFJJEGGQADMYKBIADQTNWVFUQMWHQBOAVCBVBUIOQWLZFLBCHQAHLBUDCGFAMJSKBTBHHAMQJIMKCVVOKKGOARTBKCBANDBBQBKBTBLNWUVUQGIHPRNQGKACZQZTEHQPBTMTOVFBKMKCVFJHXCBLPVBMKBOBGNMJSXBTABDWTVUGYQFAZBTEEOAHBTMTOVFBKMKCVFBVWVVMEFQLCPZBBLXTQWFUQGVVMYPALQTIOJTBVMBBNIDGBWASMOGFAVCTXROGZFVMUTWEOWGTSDRSABDZMFFZOKQMFXQMJHPRQWLUWJVMQMACNEFDXTGIYUPXPSMQGWKVFCFUAITSIQTUXTQPNOBLOIAGCMPCFGBGBAGWZPVAMQAMETPTUGTVOOMJSUSPZFQFMVONHTAIGJWGVVIAUPXAKWHMLHVVMEXQLGBMREIVGFBNJVIGFKROBTISWSGZTWRQFBKVGDBREILWBIIPQWCPTRUPXUSKBTBLCBLCBGFGBBHOKXTHIVOBBGGKNOJXCJWVEMWKBXRSAHPPGHTQGIDPLTQVCZKHSZXPQGOVBGQAMPIIGKGURYQLVGBBNIDGDILNMGVGWIFZTECUZVVBEOBVPVLEVIAOMEYWBUPCMCHZHTBXFDIEUG"
    #even = "ZMJXCGLHBGIPSPMPSOUQEOQYIFRYWCYVBWBVQKICRMWUEDXYCVAMRRYMCSRFMBGRNTLGTXRVJQKENAIFQZIIIJTATEHMUMVYZCZWPVHGLQUAOQDMVTBWBQAFJOXKVNQQTENVWACXBZRITVROUWLKJMBVRFWJXQYPWTKOIEFXKFLSBFKTTXVVFLVZKVMGQREEXQPPSEHBYIAVIBOHCJIFBVGHFPTSOFMFPLICERITWPDBZSPLIGEHUFXGVIGUGQJTGGASEVIEHEHUDHWMIXGKUWADTJMPMCFAVCTLCIXZVFIKMQGAQEHIKICGMSQIWIRGPBMCHAFJEKGDGROIERAQQFBAKIOLEVVFPDMPBUWMHBYIPXKSFVQKCQYASPXZVOGRLWFWZZFWMQCAFPRRPXTGNQLJYRITMGKMVUWBDOYHVKSHTEFVWBVRUBOBNWCIICMBVRVIDIVBUSGKMFVGMQQNOLVZGEWDZHVKWKGQBSRZDEVBWBGKMFVATVRPRUGYVXZGPLMEGGLPCJSZFQKLMCSSZFZKWQBTSZFZCUTMFHKLVGVZMCWWJCUMMAFFPRRIBVUGKQJEPVQSAWIIXKGBCNVKZIPVMHUHLVZGEWDZHVKSHVWACXBVVEHVHERTCIFVWAZXVZGCMQCAQMKAQKSGCUWEWGLMTSRZKPGLAOAGQEIZIMBFLDVGQGBOPWJVXYXMBCHWGPGHZQBPXLXGKACARXGSUBBSFLLVWQYBVRZWIPFKMDYDKZRIFWGGPIZPCGLANQGVBENZGVRVJAKMPHROMTSOFCBVFIKMQGATBUURRATXDYLKRXKHVGGKMJIEHVHNFBJQWLBPRPIUIUXKIEHIXEKGAHORBYICOMGQUWGTKGOOAGBYIKGRSPWQFRQYQZYHOZXKFIHRPMJWCZMGNWXIIUXVHU"
    crack(odd, alpha, eng_freq)
    #crack(even, alpha, eng_freq)

    
    
    


