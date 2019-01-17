import itertools
import timeit
import collections

#-*- coding: utf8 -*-

#Initial permut matrix for the datas
PI = [58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7]

#Initial permut made on the key
CP_1 = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]

#Permut applied on shifted key to get Ki+1
CP_2 = [14, 17, 11, 24, 1, 5, 3, 28,
        15, 6, 21, 10, 23, 19, 12, 4,
        26, 8, 16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55, 30, 40,
        51, 45, 33, 48, 44, 49, 39, 56,
        34, 53, 46, 42, 50, 36, 29, 32]

#Expand matrix to get a 48bits matrix of datas to apply the xor with Ki
E = [32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1]

#SBOX ja trocadas
S_BOX=[
[['1111', '0001', '1000', '1110', '0110', '1011', '0011', '0100', '1001', '0111', '0010', '1101', '1100', '0000', '0101', '1010'],
['0011', '1101', '0100', '0111', '1111', '0010', '1000', '1110', '1100', '0000', '0001', '1010', '0110', '1001', '1011', '0101'],
['0000', '1110', '0111', '1011', '1010', '0100', '1101', '0001', '0101', '1000', '1100', '0110', '1001', '0011', '0010', '1111'],
['1101', '1000', '1010', '0001', '0011', '1111', '0100', '0010', '1011', '0110', '0111', '1100', '0000', '0101', '1110', '1001'],
],

[['1110', '0100', '1101', '0001', '0010', '1111', '1011', '1000', '0011', '1010', '0110', '1100', '0101', '1001', '0000', '0111'],
['0000', '1111', '0111', '0100', '1110', '0010', '1101', '0001', '1010', '0110', '1100', '1011', '1001', '0101', '0011', '1000'],
['0100', '0001', '1110', '1000', '1101', '0110', '0010', '1011', '1111', '1100', '1001', '0111', '0011', '1010', '0101', '0000'],
['1111', '1100', '1000', '0010', '0100', '1001', '0001', '0111', '0101', '1011', '0011', '1110', '1010', '0000', '0110', '1101'],
],

[['1010', '0000', '1001', '1110', '0110', '0011', '1111', '0101', '0001', '1101', '1100', '0111', '1011', '0100', '0010', '1000'],
['1101', '0111', '0000', '1001', '0011', '0100', '0110', '1010', '0010', '1000', '0101', '1110', '1100', '1011', '1111', '0001'],
['1101', '0110', '0100', '1001', '1000', '1111', '0011', '0000', '1011', '0001', '0010', '1100', '0101', '1010', '1110', '0111'],
['0001', '1010', '1101', '0000', '0110', '1001', '1000', '0111', '0100', '1111', '1110', '0011', '1011', '0101', '0010', '1100'],
],

[['0111', '1101', '1110', '0011', '0000', '0110', '1001', '1010', '0001', '0010', '1000', '0101', '1011', '1100', '0100', '1111'],
['1101', '1000', '1011', '0101', '0110', '1111', '0000', '0011', '0100', '0111', '0010', '1100', '0001', '1010', '1110', '1001'],
['1010', '0110', '1001', '0000', '1100', '1011', '0111', '1101', '1111', '0001', '0011', '1110', '0101', '0010', '1000', '0100'],
['0011', '1111', '0000', '0110', '1010', '0001', '1101', '1000', '1001', '0100', '0101', '1011', '1100', '0111', '0010', '1110'],
],

[['0010', '1100', '0100', '0001', '0111', '1010', '1011', '0110', '1000', '0101', '0011', '1111', '1101', '0000', '1110', '1001'],
['1110', '1011', '0010', '1100', '0100', '0111', '1101', '0001', '0101', '0000', '1111', '1010', '0011', '1001', '1000', '0110'],
['0100', '0010', '0001', '1011', '1010', '1101', '0111', '1000', '1111', '1001', '1100', '0101', '0110', '0011', '0000', '1110'],
['1011', '1000', '1100', '0111', '0001', '1110', '0010', '1101', '0110', '1111', '0000', '1001', '1010', '0100', '0101', '0011'],
],

[['1100', '0001', '1010', '1111', '1001', '0010', '0110', '1000', '0000', '1101', '0011', '0100', '1110', '0111', '0101', '1011'],
['1010', '1111', '0100', '0010', '0111', '1100', '1001', '0101', '0110', '0001', '1101', '1110', '0000', '1011', '0011', '1000'],
['1001', '1110', '1111', '0101', '0010', '1000', '1100', '0011', '0111', '0000', '0100', '1010', '0001', '1101', '1011', '0110'],
['0100', '0011', '0010', '1100', '1001', '0101', '1111', '1010', '1011', '1110', '0001', '0111', '0110', '0000', '1000', '1101'],
],

[['0100', '1011', '0010', '1110', '1111', '0000', '1000', '1101', '0011', '1100', '1001', '0111', '0101', '1010', '0110', '0001'],
['1101', '0000', '1011', '0111', '0100', '1001', '0001', '1010', '1110', '0011', '0101', '1100', '0010', '1111', '1000', '0110'],
['0001', '0100', '1011', '1101', '1100', '0011', '0111', '1110', '1010', '1111', '0110', '1000', '0000', '0101', '1001', '0010'],
['0110', '1011', '1101', '1000', '0001', '0100', '1010', '0111', '1001', '0101', '0000', '1111', '1110', '0010', '0011', '1100'],
],

[['1101', '0010', '1000', '0100', '0110', '1111', '1011', '0001', '1010', '1001', '0011', '1110', '0101', '0000', '1100', '0111'],
['0001', '1111', '1101', '1000', '1010', '0011', '0111', '0100', '1100', '0101', '0110', '1011', '0000', '1110', '1001', '0010'],
['0111', '1011', '0100', '0001', '1001', '1100', '1110', '0010', '0000', '0110', '1010', '1101', '1111', '0011', '0101', '1000'],
['0010', '0001', '1110', '0111', '0100', '1010', '1000', '1101', '1111', '1100', '1001', '0000', '0011', '0101', '0110', '1011']
]
]

#Permut made after each SBox substitution for each round
P = [16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25]

#Final permut for datas after the 16 rounds
PI_1 = [40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25]

#Matrix that determine the shift for each round of chaves
SHIFT = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]


def bit_array_to_string(array):
    res = ''.join(str(e) for e in array)
    return res

def nsplit(s, n):
    return [s[k:k+n] for k in xrange(0, len(s), n)]

def hexKey2Bin(key):
        tmp=list(bin(int(key,16))[2:])
        tmp=map(int,tmp)
        while len(tmp) != 64:
            tmp.insert(0,0)
        return tmp

def gerarNchaves(n):
    uns='1'*(64-n)
    lst = list(itertools.product([0, 1], repeat=n))
    print(1)
    size=len(lst)
    chavestmp= [None]*size
    for i in range(0,size):
        chavestmp[i]=''.join(str(e) for e in lst[i])
        chavestmp[i]=uns+chavestmp[i]
    return chavestmp

def binary_search(arr,value):
    left = 0
    right = len(arr) - 1
    while(left <= right):
        mid = (left + right) // 2
        #print(mid)
        if arr[mid]==value:
            return mid
        elif value < arr[mid]:
            right = mid - 1
        elif value > arr[mid]:
            left = mid + 1

    return -1

ENCRYPT=1
DECRYPT=0

class des():
    def __init__(self):
        self.password = None
        self.text = None
        self.chaves = list()
        
    def run(self, key, text, dic, action=ENCRYPT):
        self.password = key
        self.text = text
        self.generatechaves()

        result = list()
        block=self.text

        block = self.permut(block,PI)

        g, d = nsplit(block, 32)
        tmp = None
        for i in range(16):
            d_e = self.expand(d, E)
            if action == ENCRYPT:
                tmp = self.xor(self.chaves[i], d_e)
            else:
                tmp = self.xor(self.chaves[15-i], d_e)
            tmp = self.substitute(tmp)
            tmp = self.permut(tmp, P)
            tmp = self.xor(g, tmp)
            g = d
            d = tmp
        result += self.permut(d+g, PI_1)

        dic.update({bit_array_to_string(result):bit_array_to_string(key)})
        #return final_res

    def substitute(self, d_e):
        subblocks = nsplit(d_e, 6)
        result = list()
        for i in range(len(subblocks)):
            block = subblocks[i]
            row = int(str(block[0])+str(block[5]),2)
            column = int(''.join([str(x) for x in block[1:][:-1]]),2)
            bin = S_BOX[i][row][column]
            result += [int(x) for x in bin]
        return result

    def permut(self, block, table):
        return [block[x-1] for x in table]

    def expand(self, block, table):
        return [block[x-1] for x in table]
    
    def xor(self, t1, t2):
        return [x^y for x,y in zip(t1,t2)]
    
    def generatechaves(self):
        self.chaves = []
        key=self.password
        key = self.permut(key, CP_1)

        g, d = nsplit(key, 28)
        for i in range(16):
            g, d = self.shift(g, d, SHIFT[i])
            tmp = g + d
            self.chaves.append(self.permut(tmp, CP_2))

    def shift(self, g, d, n):
        return g[n:] + g[:n], d[n:] + d[:n]
    
    def encrypt(self, key, text,dic):
        return self.run(key, text, dic,ENCRYPT)
    
    def decrypt(self, key, text,dic):
        tmp= self.run(key, text, dic, DECRYPT)
        return tmp

def main():
    start = timeit.default_timer()

    m1=hexKey2Bin("9fb49435f7c627d8")
    c1=hexKey2Bin("0b61fe6b1bc56daf")
    n=28
    size=2**n

    stop = timeit.default_timer()

    cifras={}
    decifras={}
    #processes = []

    for i in xrange(0,size):
        chaves=bin(i)[2:]
        chaves="0"*(n-len(chaves))+chaves
        chaves="1"*(64-n)+chaves
        chaves=map(int,chaves)

        d=des()
        d.encrypt(chaves,m1,cifras)
        d.decrypt(chaves,c1,decifras)

    stop = timeit.default_timer()
    print("Ordenando ",stop-start)

    d=collections.OrderedDict(sorted(decifras.items()))
    stop = timeit.default_timer()
    print("Ordenacao Decifra ",stop-start)

    #Key=Cipher / Val=Chave
    chavesDecript=d.keys()
    valDecript=d.values()


    for x,y in cifras.iteritems():
        tmp=binary_search(chavesDecript,x)
        if tmp!=-1:
            print(y,valDecript[tmp])

    stop = timeit.default_timer()
    print("Terminou",stop-start)


if __name__== "__main__":
    main()