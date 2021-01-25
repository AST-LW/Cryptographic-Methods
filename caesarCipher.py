# caesar cipher is cryptographic method of converting the plain text into cipher text
# Algorithm states that replace the plain text letter with different letter 
# that is fixed number down the alphabet

# global variables

lookUp_1={'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,
          'H':7,'I':8,'J':9,'K':10,'L':11,'M':12,'N':13,
          'O':14,'P':15,'Q':16,'R':17,'S':18,'T':19,'U':20,
          'V':21,'W':22,'X':23,'Y':24,'Z':25}
lookUp_2={0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',
          7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',
          14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',
          21:'V',22:'W',23:'X',24:'Y',25:'Z'}

def caesarCipherEncryption(plainText,number): 
    cipherText=''
    plainText=plainText.upper()
    for i in plainText:
        cipherText+=lookUp_2[(lookUp_1[i]+number)%26] 
    return cipherText

def caesarCipherDecryption(cipherText,number): 
    plainText=''
    cipherText=cipherText.upper(); 
    for i in cipherText:
        value=26+lookUp_1[i]-number if lookUp_1[i]-number<0 else lookUp_1[i]-number
        plainText+=lookUp_2[value%26]
    return plainText

cipherText=caesarCipherEncryption('a',3)
print('cipher text -> '+cipherText)
plainText=caesarCipherDecryption(cipherText,3)
print('plain text -> '+plainText)

# outputs:- 

# cipher text -> E
# plain text -> B