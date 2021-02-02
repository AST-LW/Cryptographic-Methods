from math import sqrt

lookUp={'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,
          'H':7,'I':8,'J':9,'K':10,'L':11,'M':12,'N':13,
          'O':14,'P':15,'Q':16,'R':17,'S':18,'T':19,'U':20,
          'V':21,'W':22,'X':23,'Y':24,'Z':25}

lookUpReversed={value:key for (key,value) in lookUp.items()} 

def checkEven(number): 
    if number==pow(int(sqrt(number)),2): 
        return True
    else: 
        return False

def matrixConverter(string,flag=False,dimension=None): 
    if flag==False:  # for message
        finalMatrix=[]
        i,count=0,0
        temp=[]
        while i<len(string): 
            if count<dimension: 
                temp.append(lookUp[string[i]])
                i+=1
                count+=1
            else: 
                finalMatrix.append(temp)
                temp=[] 
                count=0
        if len(temp)!=dimension:
            temp.append(lookUp['X'])  # filler letter if length is odd
        finalMatrix.append(temp)
        return finalMatrix  
    if flag==True:   # for key 
        if checkEven(len(string))==True: 
            dimension=len(string)//int(sqrt(len(string)))
            finalMatrix=[]
            for i in range(0,dimension): 
                temp=[]
                for j in range(0,dimension): 
                    temp.append(lookUp[string[j]])
                finalMatrix.append(temp)
                string=string[dimension:]
            return finalMatrix

def matrixTranspose(matrix): 
    tMatrix=[] 
    i,j=0,0
    temp=[]
    while j<len(matrix):  # for non square matries (m*n, m!=n) use j<=len(matrix)
        if i<len(matrix): 
            temp.append(matrix[i][j])
            i+=1 
        else: 
            tMatrix.append(temp)
            i=0
            j+=1
            temp=[]
    return tMatrix

def multiplicationOperation(keyMatrix,plainMatrix): 
    result=''
    for row in keyMatrix: 
        sum_=0
        temp=[] 
        for i in range(len(row)): 
            sum_+=row[i]*plainMatrix[i]
        temp.append(sum_)
        for i in temp: 
            if i<0: 
                result+=lookUpReversed[i+26]
            if i>25: 
                result+=lookUpReversed[i%26]
            else: 
                result+=lookUpReversed[i]
    return result

def hillCipher(plainText,key):
    plainText=plainText.upper()
    key=key.upper()
    keyMatrix=matrixConverter(key,True)
    plainMatrix=matrixConverter(plainText,False,len(keyMatrix))
    cipherText=''
    for i in plainMatrix: 
        cipherText+=multiplicationOperation(keyMatrix,i)
    return cipherText

print(hillCipher('GFG','HILLMAGIC'))   # SWK

       