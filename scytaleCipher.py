# in scytale cipher the message is written in row wise then read in column wise
# in this program number of rows are considered dynamically considered based on columns 
# number of columns for even length is half and for odd is rounded value
# message should be greater than >=4 length for permutations to be observed

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

def scytaleCipher(message,method=None,rows=None): 
    message=message.upper()
    manipulatedString=''
    length=len(message)
    if method=='decrypt': 
        columns=rows
    if method=='encrypt':
        if length%2==0: 
            columns=length//2
        else: 
            columns=round(length//2)    
    index=0
    matrix=[]
    while index<length: 
        temp=[] 
        for i in range(columns): 
            try:    # error occurs in odd message length
                temp.append(message[index])
                index+=1 
            except:  # so add buffer bit 
                temp.append('X')
        matrix.append(temp)    
    rows=len(matrix)
    tMatrix=matrixTranspose(matrix)
    for i in tMatrix: 
        for j in i: 
            manipulatedString+=j
    if method=='encrypt': 
        return manipulatedString,rows
    if method=='decrypt': 
        return manipulatedString.replace('X','')

print('cipher text -> '+scytaleCipher('HELLOWORLD','encrypt')[0]) 
print('number of rows required for decypher -> '+str(scytaleCipher('HELLOWORLD','encrypt')[1]))
print('plain text -> '+scytaleCipher('HWEOLRLLOD','decrypt',2))      

# outputs:
# cipher text -> HWEOLRLLOD
# number of rows required for decypher -> 2
# plain text -> HELLOWORLD