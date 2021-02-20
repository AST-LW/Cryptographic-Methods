# baconian cipher is a subsitution cipher
# the advantage of baconian cipher is that it helps in hiding the fact that secret message is being sent
# the disadvantage is that we have same encode characters for I/J and U/V
# this cipher is not resistent to cipher attack

lookUp={'A':'aaaaa','I':'abaaa','R':'baaaa',
        'B':'aaaab','K':'abaab','S':'baaab',
        'C':'aaaba','L':'ababa','T':'baaba',
        'D':'aaabb','M':'ababb','U':'baabb',
        'E':'aabaa','N':'abbaa','W':'babaa',
        'F':'aabab','O':'abbab','X':'babab',
        'G':'aabba','P':'abbba','Y':'babba',
        'H':'aabbb','Q':'abbbb','Z':'babbb'}
    
lookUpReversed={value:key for key,value in lookUp.items()}

def baconianCipher(messageOrCiphertext,method=None):
    if method=='encrypt': 
        messageOrCiphertext=messageOrCiphertext.upper()
        cipherText=''
        for i in messageOrCiphertext: 
            cipherText+=lookUp[i]
        return cipherText
    if method=='decrypt':
        plainText=''
        for i in range(0,len(messageOrCiphertext),5): 
            plainText+=lookUpReversed[messageOrCiphertext[i:i+5]]
        return plainText
    
print('the cipher text -> '+baconianCipher('helloworld','encrypt'))
print('the plain text -> '+baconianCipher('aabbbaabaaababaababaabbabbabaaabbabbaaaaababaaaabb','decrypt')) 

# outputs:

# the cipher text -> aabbbaabaaababaababaabbabbabaaabbabbaaaaababaaaabb
# the plain text -> HELLOWORLD
