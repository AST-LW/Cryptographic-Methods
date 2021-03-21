
DNA_Base={'00': 'A', '01': 'C', '10': 'G', '11': 'T'}
DNA_Complemetary_List=['A','C','G','T']
   
def convert_to_ascii(string):
    ascii_output=''
    for i in string: 
        value=bin(ord(i))[2:]
        if len(value)!=8:
            value=(value[::-1]+''.join(['0' for j in range(8-len(value))]))[::-1]
        ascii_output+=value
    return ascii_output

def dna_base_conversion(binary_string): 
    dna_code=''
    for i in range(0,len(binary_string),2): 
        dna_code+=DNA_Base[binary_string[i:i+2]]
    return dna_code

def dna_complementary_rule(dna_base_string): 
    dna_base_after_complementing=''
    for i in dna_base_string: 
        dna_base_after_complementing+=DNA_Complemetary_List[(DNA_Complemetary_List.index(i)+1)%4]
    return dna_base_after_complementing

def dnaVariationCipher1(string,method=None):

    if method=='encrypt':
        cipher_text=''
        message_in_binary_format=convert_to_ascii(string)
        dna_base=dna_base_conversion(message_in_binary_format)
        print(dna_base)
        dna_complementary=dna_complementary_rule(dna_base)
        print(dna_complementary)
        return dna_complementary

    if method=='decrypt': 
        plaintext=''
        dna_complementary=dna_complementary_rule(string)
        print(dna_complementary)
        # print(dna_base)
  
print(dnaVariationCipher1('TURN','encrypt')) 
print(dnaVariationCipher1('GGGCGGGGGGCTGCAT', 'decrypt'))