# c=a*(p+b)mod26 
# p=a^-1(c-b)mod26
 
lookUp={'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,
          'H':7,'I':8,'J':9,'K':10,'L':11,'M':12,'N':13,
          'O':14,'P':15,'Q':16,'R':17,'S':18,'T':19,'U':20,
          'V':21,'W':22,'X':23,'Y':24,'Z':25}
lookUpReversed={value:key for (key,value) in lookUp.items()}

def multiplicativeInverse(number,modulo):
    dividend=modulo
    divisor=number
    quoitent,remainder=None,None
    t,t1,t2=None,0,1
    while divisor!=0: 
        quoitent=dividend//divisor
        remainder=dividend%divisor
        t=t1-quoitent*t2
        t1=t2
        t2=t
        dividend=divisor
        divisor=remainder
        
    return t1+modulo if t1<0 else t1

def euclidAlgorithm(a,b): 
    if b==0:
        return a 
    else: 
        remainder=a%b
        return euclidAlgorithm(b,remainder)

def affineCipher(messageOrCiphertext,key,method=None):
    a,b=key[0],key[1]
    if euclidAlgorithm(26,a)!=1: 
        return 'constant "a" and 26 should be relative prime'
    messageOrCiphertext=messageOrCiphertext.upper()
    if method=='encrypt': 
        cipherText=''
        for i in messageOrCiphertext: 
            cipherText+=lookUpReversed[(a*lookUp[i]+b)%26]
        return cipherText
    if method=='decrypt': 
        plainText=''
        mulInverse=multiplicativeInverse(a,26)
        for i in messageOrCiphertext:
            value=mulInverse*(lookUp[i]-b)%26 if mulInverse*(lookUp[i]-b)<0 else mulInverse*(lookUp[i]-b)%26
            plainText+=lookUpReversed[value]
        return plainText

print('the cipher text -> '+affineCipher('defendtheeastwallofcastle',[5,7],'encrypt')) 
print('the plaintext -> '+affineCipher('WBGBUWYQBBHTYNHKKZGRHTYKB',[5,7],'decrypt'))

# outputs:-

# the cipher text -> WBGBUWYQBBHTYNHKKZGRHTYKB
# the plaintext -> DEFENDTHEEASTWALLOFCASTLE
