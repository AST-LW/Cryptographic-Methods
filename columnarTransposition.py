# columnar transposition cipher uses permutations of characters in message

def changeKeyFormat(key): 
    lookUp={}
    changedFormat=[]
    for i,j in zip(sorted([i for i in key]),range(len(key))):
        lookUp[i]=j
    for i in key: 
        changedFormat.append(lookUp[i])
    return changedFormat

def matrixFormation(string,keyLength): 
    if len(string)%keyLength!=0: 
        numberOfBuffers=keyLength-(len(string)-(len(string)//keyLength)*keyLength)
        for i in range(numberOfBuffers): 
            string+='X'
    rows=len(string)//keyLength
    columns=keyLength
    matrix=[] 
    index=0
    for i in range(rows): 
        temp=[] 
        for j in range(columns): 
            temp.append(string[index])
            index+=1 
        matrix.append(temp)
    return matrix

def getIndex(array,target): 
    return array.index(target)

def matrixTranspose(matrix): 
    tMatrix=[]
    rows=len(matrix)
    columns=len(matrix[0])
    for i in range(columns): 
        temp=[]
        for j in range(rows): 
            temp.append(0)
        tMatrix.append(temp)
    for i in range(columns): 
        for j in range(rows): 
            tMatrix[i][j]=matrix[j][i]
    return tMatrix 

def columnarTranspositionEncrypt(plainText,key): 
    plainText=plainText.upper()
    key=key.upper()
    keyFormat=changeKeyFormat(key)
    matrix=matrixFormation(plainText,len(key))
    cipherText=''
    for i in sorted(keyFormat): 
        index=getIndex(keyFormat,i)
        for j in matrix: 
            cipherText+=j[index]
    return cipherText

def columnarTranspositionDecrypt(cipherText,key): 
    cipherText=cipherText.upper()
    key=key.upper()
    keyFormat=changeKeyFormat(key)
    plainText=''
    matrix=matrixFormation(cipherText,len(cipherText)//len(key))
    matrix=matrixTranspose(matrix)
    finalMatrix=[] 
    for i in keyFormat:  # during decryption no need to sort the key format...
        temp=[]
        for j in matrix: 
            temp.append(j[i])
        finalMatrix.append(temp)
    finalMatrix=matrixTranspose(finalMatrix)
    for i in finalMatrix: 
        for j in i: 
            plainText+=j
    return plainText.replace('X','')

print('cipher text -> '+columnarTranspositionEncrypt('HIMYNAMEISASTLW','AEDCB'))
print('plain text -> '+columnarTranspositionDecrypt('HAANSWYILMETIMS','AEDCB'))

# outputs: 
# cipher text -> HAANSWYILMETIMS
# plain text -> HIMYNAMEISASTLW 