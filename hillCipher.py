# Ground knowledge of hill cipher is required before diving into the script

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

def matrixConverter(string,flag=False,dimension=None):  # input is string, output is matrix which is square order
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
    rows,columns=len(matrix),len(matrix[0])
    for i in range(columns): 
        temp=[] 
        for j in range(rows): 
            temp.append(0)
        tMatrix.append(temp)
    for i in range(columns): 
        for j in range(rows): 
            tMatrix[i][j]=matrix[j][i]
    return tMatrix    

def multiplicationOperation(keyMatrix,plainMatrix,flag=False):  # matrix multiplication
    if flag==False:
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
    if flag==True: 
        result=''

def multiplicativeInverse(number):   # used for finding modular inverse
    # if abs(number)<26: 
    #     return abs(number)
    for i in range(26): 
        if (number*i)%26==1: 
            return i
       
def det(matrix,flag=False):  # pass False to calculate the det value of n*n matrix, True for cofactor matrix
    if len(matrix)!=len(matrix[0]):
        return 'NOT SQUARE MATRIX'
    if len(matrix)==2: 
        return matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0]
    else:
        dimension=len(matrix)
        sum_=0
        adjValues=[]   # incase to find adjoint...
        for element,index1 in zip(matrix[0],range(len(matrix))): 
            temp=[]
            for i in range(1,len(matrix)): 
                order=sorted([(index1+j)%dimension for j in range(1,dimension)])
                temp1=[matrix[i][k] for k in order]
                temp.append(temp1)
            if flag==False:
                sum_+=pow(-1,(0+index1))*element*det(temp) # recursion...
            if flag==True: 
                # adjValues.append(pow(-1,(0+index1))*det(temp,True))
                adjValues.append(pow(-1,(0+index1))*det(temp))
        if flag==False: 
            return sum_
        if flag==True: 
            return adjValues 

def exchangeRows(matrix,whichRow):   # used for moving the rows to top
    temp=[]   # directly manipulating will cause in-memory issues
    temp.append(matrix[whichRow])
    for i in matrix: 
        if i!=temp[0]: 
            temp.append(i)
    return temp
 
def adjoint(matrix): 
    dimension=len(matrix)
    adjointMatrix=[]
    if dimension==2:  # for 2D matrix just return the adjoint as it can be calculated without any difficulty
        return [[matrix[1][1],-1*matrix[0][1]],[-1*matrix[1][0],matrix[0][0]]]
    else:              # for higher dimensions
        for i in range(dimension): 
            tempMatrix=exchangeRows(matrix,i)
            adjointMatrix.append([pow(-1,i)*j for j in det(tempMatrix,True)])   # pass True for calculating the cofator matrix 
    return matrixTranspose(adjointMatrix)   # transpose the cofactor matrix to get adjoint
  
def inverseOfMatrix(matrix): 
    adjMatrix=adjoint(matrix)   # finding the adjoint of a matrix
    for i in range(len(adjMatrix)): 
        for j in range(len(adjMatrix)): 
            adjMatrix[i][j]=(adjMatrix[i][j]*multiplicativeInverse(det(matrix)))%26 # if greater than 26 then %26
            if adjMatrix[i][j]<0:  # if any element is negative add +26 to it
                adjMatrix[i][j]+=26
    return adjMatrix

def hillCipherEncrypt(plainText,key):   # encryption
    plainText=plainText.upper()
    key=key.upper()
    keyMatrix=matrixConverter(key,True)
    plainMatrix=matrixConverter(plainText,False,len(keyMatrix))
    cipherText=''
    for i in plainMatrix: 
        cipherText+=multiplicationOperation(keyMatrix,i,False)
    return cipherText

def hillCipherDecrypt(cipherText,key):  # decryption
    cipherText=cipherText.upper()
    key=key.upper()
    keyMatrix=matrixConverter(key,True)
    inverseKeyMatrix=inverseOfMatrix(keyMatrix)   # finding the inverse of a matrix
    cipherText=matrixConverter(cipherText,False,len(inverseKeyMatrix))
    plainText=''
    for i in cipherText:
        plainText+=multiplicationOperation(inverseKeyMatrix,i,False)
    return plainText.replace('X','')

print('cipher text -> '+hillCipherEncrypt('HOWAREYOU','RRFVSVCCT'))    # the condition for key, (d*d^-1)%26=1 where d is determinant and d^-1 is inverse of determinant
print('plain text -> '+hillCipherDecrypt('ZDSXAGSGO','RRFVSVCCT'))     

# outputs:- 
# cipher text -> ZDSXAGSGO
# plain text -> HOWAREYOU

print('cipher text -> '+hillCipherEncrypt('ATTACK','CDDG'))
print('plain text -> '+hillCipherDecrypt('FKMFIO','CDDG'))

# outputs:-
# cipher text -> FKMFIO
# plain text -> ATTACK
 
# cannot take some key...
# key must be well defined so that we get the modular inverse for 26 exists...

           