# before going into the flow, go through what is playfair cipher...

def helperFunction(key):  # converting 1D to 2D key
    key=key.replace('J','I')
    keyLookUp=['A','B','C','D','E','F','G','H',
                'I','K','L','M','N','O','P','Q',
                'R','S','T','U','V','W','X','Y','Z']
    keyMatrix=[]
    keyLength=len(key)
    keyString=''
    for i in key: 
        if i not in keyString: 
            keyString+=i 
    for i in keyLookUp: 
        if i not in keyString: 
            keyString+=i
    for i in range(0,5): 
        temp=[]
        for j in range(0,5): 
            temp.append(keyString[j])
        keyMatrix.append(temp)
        keyString=keyString[5:26]
    return keyMatrix

def search(matrix2D,element): # searching element in 2D matrix
    for i in range(len(matrix2D)): 
        for j in range(len(matrix2D[i])):
            if matrix2D[i][j]==element: 
                return [i,j]  # returns row and column
    return None

def pairOfTwo(string):  # to modify the plain text format
    finalArray=[] 
    i=0
    temp=''
    while i<len(string): 
        if len(temp)!=2: 
            if string[i] not in temp: 
                temp+=string[i]
                i+=1
            else: 
                temp+='X'
        else: 
            finalArray.append(temp)
            temp=''
    if len(temp)==1: 
        temp+='X'
    finalArray.append(temp)
    return finalArray           
 
def playFair(plainText,key,flag=False):  # algorithm starts here... 
    plainText=plainText.upper()
    key=key.upper()
    keyMatrix=helperFunction(key)
    plainText=pairOfTwo(plainText)
    cipherText=''
    for i in plainText:
        rowCol1=search(keyMatrix,i[0])
        rowCol2=search(keyMatrix,i[1])
        if rowCol1[0]==rowCol2[0] and flag==False:  # encrypt condition
            newCol1=(rowCol1[1]+1)%5
            newCol2=(rowCol2[1]+1)%5
            cipherText+=keyMatrix[rowCol1[0]][newCol1]
            cipherText+=keyMatrix[rowCol2[0]][newCol2]
        if rowCol1[0]==rowCol2[0] and flag==True:   # decrypt condition
            newCol1=(rowCol1[1]-1)%5
            newCol2=(rowCol2[1]-1)%5
            cipherText+=keyMatrix[rowCol1[0]][newCol1]
            cipherText+=keyMatrix[rowCol2[0]][newCol2]
        elif rowCol1[1]==rowCol2[1] and flag==False: # encrypt condition
            newRow1=(rowCol1[0]+1)%5
            newRow2=(rowCol2[0]+1)%5
            cipherText+=keyMatrix[newRow1][rowCol1[1]]
            cipherText+=keyMatrix[newRow2][rowCol2[1]]
        elif rowCol1[1]==rowCol2[1] and flag==True:  # decrypt condition
            newRow1=(rowCol1[0]-1)%5
            newRow2=(rowCol2[0]-1)%5
            cipherText+=keyMatrix[newRow1][rowCol1[1]]
            cipherText+=keyMatrix[newRow2][rowCol2[1]]
        else:                                        # common condition in both encrypt and decrypt
            cipherText+=keyMatrix[rowCol1[0]][rowCol2[1]]        
            cipherText+=keyMatrix[rowCol2[0]][rowCol1[1]]
    if flag==True:  # removing the filler letters
        cipherText=cipherText.replace('X','')
    return cipherText

print(playFair('Hello','playfairexample'))  # DMYRAN
# flag is used to determine whether encryption or decrytion operation...
# flag=False for encryption and True for decryption
print(playFair('DMYRAN','playfairexample',flag=True)) # HELLO
