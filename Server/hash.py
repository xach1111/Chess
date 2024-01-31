## SHA256 algorithm coded from scratch

def XOR(*strings): ## multiple 32 bit strings
    sum = 0
    for number in strings:
        sum = sum ^ int(number,2)
    sum = str(bin(sum))[2:]
    while len(sum) < 32:
        sum = "0" + sum
    return sum

def Add(*strings): ## multiple 32 bit strings
    sum = 0
    for number in strings:
        sum = sum + int(number,2)
    sum = str(bin(sum))[2:]
    while len(sum) < 32:
        sum = "0" + sum
    
    while len(sum) > 32:
        sum = sum[1:]
    return sum
    
def rotate(string,n):
    Rfirst = string[0 : len(string)-n]
    Rsecond = string[len(string)-n : ]
    return Rsecond + Rfirst

def rshift(string,n):
    newstring = list(rotate(string, n))
    for i in range(n):
        newstring[i] = "0"
    return "".join(newstring)

def sigma0(string32): ## recieves 32 bits and returns addition of 7 rotation, 18 rotation, and right shift 3
    Rot7 = rotate(string32, 7)
    Rot18 = rotate(string32, 18)
    Rsh3 = rshift(string32, 3)
    return XOR(Rot7, Rot18, Rsh3)

def sigma1(string32): ## recieves 32 bits and returns addition of 17 rotation, 19 rotation, and right shift 10
    Rot17 = rotate(string32, 17)
    Rot19 = rotate(string32, 19)
    Rsh10 = rshift(string32, 10)
    return XOR(Rot17, Rot19, Rsh10)

def SIGMA0(String32): ## recieves 32 bits and returns addition of 2 rotation, 13 rotation, and 22 rotation
    return XOR(rotate(String32, 2), rotate(String32, 13), rotate(String32, 22))

def SIGMA1(String32): ## recieves 32 bits and returns addition of 6 rotation, 11 rotation, and 25 rotation
    return XOR(rotate(String32, 6), rotate(String32, 11), rotate(String32, 25))

def Ch(s1, s2, s3):
    string = ""
    for i in range(32):
        if s1[i] == "0":
            string = string + s3[i]
        else:
            string = string + s2[i]
    return string

def Maj(s1, s2, s3): ## returns majority, 000, 001, 011, 111
    string = ""
    for i in range(32):
        if int(s1[i]) + int(s2[i]) + int(s3[i]) >= 2:
            string = string + "1"
        else:
            string = string + "0"
    return string

def hash(string):
    OriginalString = ''.join(format(ord(i), '08b') for i in string)
    OriginalStringLength = "{0:b}".format(len(OriginalString))
    OriginalString = OriginalString + "1"
    while (len(OriginalString) + 64) % 512 != 0:
        OriginalString = OriginalString + "0"
    for i in range(64 - len(OriginalStringLength)):
        OriginalString = OriginalString + "0"
    OriginalString = OriginalString + OriginalStringLength
    hashList = [OriginalString[i:i+round(len(OriginalString)/(len(OriginalString)/512))] for i in range(0, len(OriginalString),round(len(OriginalString)/(len(OriginalString)/512)))]
    for block in range(len(hashList)):
        rows = [hashList[block][i:i+round(len(hashList[block])/16)] for i in range(0, len(hashList[block]),round(len(hashList[block])/16))]
        hashList[block] = rows 

    ## hashlist contains 2d array with the first element being each 512 bit block, and the second being the 16, 32 bit lines
    
    ## Initial hash values
    ## Hn = the hexadecimal value of the first 32 bits of the digits after the decimal point of the square root of the first nth prime number
    H0 = "01101010000010011110011001100111"
    H1 = "10111011011001111010111010000101"
    H2 = "00111100011011101111001101110010"
    H3 = "10100101010011111111010100111010"
    H4 = "01010001000011100101001001111111"
    H5 = "10011011000001010110100010001100"
    H6 = "00011111100000111101100110101011"
    H7 = "01011011111000001100110100011001"

    ## K values - first 32 bits of the digits after the decimal point of a cube root of the first 64 prime numbers
    K = ["01000010100010100010111110011000", "01110001001101110100010010010001", "10110101110000001111101111001111", "11101001101101011101101110100101", "00111001010101101100001001011011", "01011001111100010001000111110001", "10010010001111111000001010100100", "10101011000111000101111011010101", 
         "11011000000001111010101010011000", "00010010100000110101101100000001", "00100100001100011000010110111110", "01010101000011000111110111000011", "01110010101111100101110101110100", "10000000110111101011000111111110", "10011011110111000000011010100111", "11000001100110111111000101110100", 
         "11100100100110110110100111000001", "11101111101111100100011110000110", "00001111110000011001110111000110", "00100100000011001010000111001100", "00101101111010010010110001101111", "01001010011101001000010010101010", "01011100101100001010100111011100", "01110110111110011000100011011010", 
         "10011000001111100101000101010010", "10101000001100011100011001101101", "10110000000000110010011111001000", "10111111010110010111111111000111", "11000110111000000000101111110011", "11010101101001111001000101000111", "00000110110010100110001101010001", "00010100001010010010100101100111", 
         "00100111101101110000101010000101", "00101110000110110010000100111000", "01001101001011000110110111111100", "01010011001110000000110100010011", "01100101000010100111001101010100", "01110110011010100000101010111011", "10000001110000101100100100101110", "10010010011100100010110010000101", 
         "10100010101111111110100010100001", "10101000000110100110011001001011", "11000010010010111000101101110000", "11000111011011000101000110100011", "11010001100100101110100000011001", "11010110100110010000011000100100", "11110100000011100011010110000101", "00010000011010101010000001110000", 
         "00011001101001001100000100010110", "00011110001101110110110000001000", "00100111010010000111011101001100", "00110100101100001011110010110101", "00111001000111000000110010110011", "01001110110110001010101001001010", "01011011100111001100101001001111", "01101000001011100110111111110011",
         "01110100100011111000001011101110", "01111000101001010110001101101111", "10000100110010000111100000010100", "10001100110001110000001000001000", "10010000101111101111111111111010", "10100100010100000110110011101011", "10111110111110011010001111110111", "11000110011100010111100011110010"]

    for chunk in range(len(hashList)):
        w = [row for row in hashList[chunk]] ## w[n] = M[n] where m is a a single row of 32 bits from the hashlist and 0 ≤ n ≤ 15

        for i in range(48): ## t is used because notation follows w[t] for each row where 0 ≤ t ≤ 63 and because 16 rows are filled, it must loop 48 times
            t = i + 16
            w.append(Add(sigma1(w[t - 2]), w[t - 7], sigma0(w[t-15]), w[t-16]))
        
        a = H0
        b = H1
        c = H2
        d = H3
        e = H4
        f = H5
        g = H6
        h = H7

        for t in range(64):
            T1 = Add(h, SIGMA1(e), Ch(e,f,g), K[t], w[t])
            T2 = Add(SIGMA0(a), Maj(a,b,c))
            h=g
            g=f
            f=e
            e=Add(d, T1)
            d=c
            c=b
            b=a
            a=Add(T1, T2)

        H0 = Add(a, H0)
        H1 = Add(b, H1)
        H2 = Add(c, H2)
        H3 = Add(d, H3)
        H4 = Add(e, H4)
        H5 = Add(f, H5)
        H6 = Add(g, H6)
        H7 = Add(h, H7)
    
    finalBitPattern = H0 + H1 + H2 + H3 + H4 + H5 + H6 + H7
    return str(hex(int(finalBitPattern, 2)))[2:]

print(hash("Password_123"))