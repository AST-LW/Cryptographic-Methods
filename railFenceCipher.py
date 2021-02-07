# rail cipher is transposition method
# this method introduces permutation of characters
# if key is greater or equal to len of string then no re-arranging happens...


# create a matrix of length=key*len(message)
# putting the elements with the message in upramp and downramp fashion
# note down the cipher text by going along rows (each row visited once)

# create a matrix of length=key*len(message)
# replace the elements with the filler character in upramp and downramp fashion
# now replace the fille elements with cipher text in row fashion
# now get the elements along upramp and downramp fashion

def helperFunction(matrix,string,method=None): 
    direction=False
    row,column=0,0
    if method=='put':   # used during encryption
        for i in range(len(string)): 
            if row==0 or row==len(matrix)-1: 
                 direction=not direction
            matrix[row][column]=string[i]
            column+=1 
            if direction==True: 
                row+=1 
            if direction==False: 
                row-=1 
        return matrix
    if method=='replace':   # used during decryption 
        for i in range(len(string)):
            if row==0 or row==len(matrix)-1: 
                direction=not direction
            matrix[row][column]='_'
            column+=1 
            if direction==True: 
                row+=1 
            if direction==False: 
                row-=1
        return matrix
    if method=='get':   # used during decryption
        result=''
        for i in range(len(string)): 
            if row==0 or row==len(matrix)-1: 
                direction=not direction
            result+=matrix[row][column]
            column+=1 
            if direction==True: 
                row+=1 
            if direction==False: 
                row-=1
        return result

def railFenceCipherEncrypt(plainText,key): 
    if type(key)!=int: 
        return 'KEY IS NOT A NUMBER, PROVIDE A POSITIVE NUMBER >=2'
    plainText=plainText.upper()
    matrix=[] 
    cipherText=''
    for i in range(key): 
        temp=[]
        for j in range(len(plainText)): 
            temp.append(0)
        matrix.append(temp)
    matrix=helperFunction(matrix,plainText,'put')
    for i in range(key): 
        for j in range(len(plainText)): 
            if matrix[i][j]!=0: 
                cipherText+=matrix[i][j]
            else: 
                continue
    return cipherText

def railFenceCipherDecrypt(cipherText,key): 
    if type(key)!=int: 
        return 'KET IS NOT A NUMBER, PROVIDE A POSITIVE NUMBER>=2'
    ciperText=cipherText.upper()
    matrix=[] 
    plainText=''
    for i in range(key): 
        temp=[]
        for j in range(len(cipherText)): 
            temp.append(0)
        matrix.append(temp)
    matrix=helperFunction(matrix,cipherText,'replace')
    index=0
    for i in range(key): 
        for j in range(len(cipherText)): 
            if matrix[i][j]=='_': 
                matrix[i][j]=cipherText[index]
                index+=1
    plainText=helperFunction(matrix,cipherText,'get')
    return plainText

print('cipher text -> '+railFenceCipherEncrypt('wearehome',4)) 
print('plain text -> '+railFenceCipherDecrypt('WOEHMAEER',4))

# outputs:
# cipher text -> WOEHMAEER
# plain text -> WEAREHOME