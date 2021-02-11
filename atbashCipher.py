# just reverse the character set

lookUp={'A':'Z','B':'Y','C':'X','D':'W','E':'V','F':'U','G':'T',
          'H':'S','I':'R','J':'Q','K':'P','L':'O','M':'N','N':'M',
          'O':'L','P':'K','Q':'J','R':'I','S':'H','T':'G','U':'F',
          'V':'E','W':'D','X':'C','Y':'B','Z':'A'}

def atbashCipher(messageOrCipher,method=None): 
    messageOrCipher=messageOrCipher.upper()
    if method=='encrypt': 
        cipherText=''
        for i in messageOrCipher: 
            cipherText+=lookUp[i]
        return cipherText
    if method=='decrypt': 
        plainText=''
        lookUpReversed={value:key for (key,value) in lookUp.items()}
        for i in messageOrCipher: 
            plainText+=lookUp[i]
        return plainText
    
print('cipher text -> '+atbashCipher('HELLOWORLD','encrypt'))
print('plain text -> '+atbashCipher('SVOOLDLIOW','decrypt'))

# outputs:-
# cipher text -> SVOOLDLIOW
# plain text -> HELLOWORLD

             
    