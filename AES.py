# understanding:- 
# class based programming makes the performace better than functional prgramming
# each instance has its own variables
# i can the function which is declared after using it in another function
# eg: class A:
#       def a(self): 
#           self.b()
        
#       def b(self): 
#        print('hello world...')
# In AES, the message and key are arranged in column matrix,
# if message is abcd, then it is arranged in [[a,c],[b,d]] not like [[a,b],[c,d]]
# the arrangement does not matter in sub-bytes and shift-row stage, but
# matters in mix-columns and key expansion

# process:-
# instantiate the object with message to be encrypted and key/password as 
# arguments to the class
# object.convert_plaintext_to_hexformat(), returns string of hex characters
# object.state_matrix(string), returns the matrix of 4x4 (lists within list)
# object.key_expansion(), returns none but creates all the key-expansions... 
# object.mixColumns(matrix) - returns matrix 
# object.sub_bytes(matrix) - returns matrix
# object.shift_rows(matrix) - returns matrix
# object.two_matrix_xor_operation(matrix_1,matrix_2) returns matrix

# steps:-
# take the message in plain text and  convert to hex text using the function-
# convert_plaintext_to_hexformat() returns string
# after that execute key_expansion() to generate all the keys required for the
# subsequent rounds, and store it in the list (before storing tanspose the matrix)
# take the hex format and convert it to matrix-form using the function -
# state_matrix(string), returns matrix
# then change the rows -> columns using the function - matrix_transpose(matrix)
# returns matrix
# pass the changed matrix to function sub_bytes as an argument to make the
# s-box substitution, returns matrix
# then pass it to the shift_rows function as an argument to make row_permutation, returns matrix
# then pass it to the mixColumns function to make column permutation
# at last perform the xor with round key using two_matrix_xor_operation, return matrix
# continue it the last round...

from time import time,sleep 
import sys
from md5 import Md5

# AES algorithm:-

# task-1:- take plain text as input and convert into hex format - success 
#          (convert_plaintext_to_hexformat())
# task-2:- hex format convert into 4x4 matrix, in other words convert into 2-D
#          array - success (state_matrix())
# task-3:- function to calculate the xor operation - success xor_operation()
# task-4:- finding all the key expansion values - success key_expansion()
# task-5:- performing the mix columns function... - success mixColumns()
# task-6:- substitution matrix - success sub_bytes()
# task-7:- shift rows - success shift_rows() 
# task-8:- funciton to calculate xor between the matrices - success 
#          two_matrix_xor_operation()

# AES class:-

class AES: 
    
    look_up_BinToHex={'0000':'0','0001':'1','0010':'2','0011':'3','0100':'4',
                      '0101':'5','0110':'6','0111':'7','1000':'8','1001':'9',
                      '1010':'a','1011':'b','1100':'c','1101':'d','1110':'e',
                      '1111':'f'}
    
    look_up_HexToBin={'0':'0000','1':'0001','2':'0010','3':'0011','4':'0100',
                      '5':'0101','6':'0110','7':'0111','8':'1000','9':'1001',
                      'a':'1010','b':'1011','c':'1100','d':'1101','e':'1110',
                      'f':'1111'}
    
    s_box_look_up={'0':{'0':'63','1':'7c','2':'77','3':'7b','4':'f2','5':'6b',
                        '6':'6f','7':'c5','8':'30','9':'01','a':'67','b':'2b',
                        'c':'fe','d':'d7','e':'ab','f':'76'},
                   '1':{'0':'ca','1':'82','2':'c9','3':'7d','4':'fa','5':'59',
                        '6':'47','7':'f0','8':'ad','9':'d4','a':'a2','b':'af',
                        'c':'9c','d':'a4','e':'72','f':'c0'},
                   '2':{'0':'b7','1':'fd','2':'93','3':'26','4':'36','5':'3f',
                        '6':'f7','7':'cc','8':'34','9':'a5','a':'e5','b':'f1',
                        'c':'71','d':'d8','e':'31','f':'15'},
                   '3':{'0':'04','1':'c7','2':'23','3':'c3','4':'18','5':'96',
                        '6':'05','7':'9a','8':'07','9':'12','a':'80','b':'e2',
                        'c':'eb','d':'27','e':'b2','f':'75'},
                   '4':{'0':'09','1':'83','2':'2c','3':'1a','4':'1b','5':'6e',
                        '6':'5a','7':'a0','8':'52','9':'3b','a':'d6','b':'b3',
                        'c':'29','d':'e3','e':'2f','f':'84'},
                   '5':{'0':'53','1':'d1','2':'00','3':'ed','4':'20','5':'fc',
                        '6':'b1','7':'5b','8':'6a','9':'cb','a':'be','b':'39',
                        'c':'4a','d':'4c','e':'58','f':'cf'},
                   '6':{'0':'d0','1':'ef','2':'aa','3':'fb','4':'43','5':'4d',
                        '6':'33','7':'85','8':'45','9':'f9','a':'02','b':'7f',
                        'c':'50','d':'3c','e':'9f','f':'a8'},
                   '7':{'0':'51','1':'a3','2':'40','3':'8f','4':'92','5':'9d',
                        '6':'38','7':'f5','8':'bc','9':'b6','a':'da','b':'21',
                        'c':'10','d':'ff','e':'f3','f':'d2'},
                   '8':{'0':'cd','1':'0c','2':'13','3':'ec','4':'5f','5':'97',
                        '6':'44','7':'17','8':'c4','9':'a7','a':'7e','b':'3d',
                        'c':'64','d':'5d','e':'19','f':'73'},
                   '9':{'0':'60','1':'81','2':'4f','3':'dc','4':'22','5':'2a',
                        '6':'90','7':'88','8':'46','9':'ee','a':'b8','b':'14',
                        'c':'de','d':'5e','e':'0b','f':'db'},
                   'a':{'0':'e0','1':'32','2':'3a','3':'0a','4':'49','5':'06',
                        '6':'24','7':'5c','8':'c2','9':'d3','a':'ac','b':'62',
                        'c':'91','d':'95','e':'e4','f':'79'},
                   'b':{'0':'e7','1':'c8','2':'37','3':'6d','4':'8d','5':'d5',
                        '6':'4e','7':'a9','8':'6c','9':'56','a':'f4','b':'ea',
                        'c':'65','d':'7a','e':'ae','f':'08'},
                   'c':{'0':'ba','1':'78','2':'25','3':'2e','4':'1c','5':'a6',
                        '6':'b4','7':'c6','8':'e8','9':'dd','a':'74','b':'1f',
                        'c':'4b','d':'bd','e':'8b','f':'8a'},
                   'd':{'0':'70','1':'3e','2':'b5','3':'66','4':'48','5':'03',
                        '6':'f6','7':'0e','8':'61','9':'35','a':'57','b':'b9',
                        'c':'86','d':'c1','e':'1d','f':'9e'},
                   'e':{'0':'e1','1':'f8','2':'98','3':'11','4':'69','5':'d9',
                        '6':'8e','7':'94','8':'9b','9':'1e','a':'87','b':'e9',
                        'c':'ce','d':'55','e':'28','f':'df'},
                   'f':{'0':'8c','1':'a1','2':'89','3':'0d','4':'bf','5':'e6',
                        '6':'42','7':'68','8':'41','9':'99','a':'2d','b':'0f',
                        'c':'b0','d':'54','e':'bb','f':'16'}}
    
    s_box_inverse_look_up={'0':{'0':'52','1':'09','2':'6a','3':'d5','4':'30',
                               '5':'36','6':'a5','7':'38','8':'bf','9':'40',
                               'a':'a3','b':'9e','c':'81','d':'f3','e':'d7',
                               'f':'fb'},
                          '1':{'0':'7c','1':'e3','2':'39','3':'82','4':'9b',
                               '5':'2f','6':'ff','7':'87','8':'34','9':'8e',
                               'a':'43','b':'44','c':'c4','d':'de','e':'e9',
                               'f':'cb'},
                          '2':{'0':'54','1':'7b','2':'94','3':'32','4':'a6',
                               '5':'c2','6':'23','7':'3d','8':'ee','9':'4c',
                               'a':'95','b':'0b','c':'42','d':'fa','e':'c3',
                               'f':'4e'},
                          '3':{'0':'08','1':'2e','2':'a1','3':'66','4':'28',
                               '5':'d9','6':'24','7':'b2','8':'76','9':'5b',
                               'a':'a2','b':'49','c':'6d','d':'8b','e':'d1',
                               'f':'25'},
                          '4':{'0':'72','1':'f8','2':'f6','3':'64','4':'86',
                               '5':'68','6':'98','7':'16','8':'d4','9':'a4',
                               'a':'5c','b':'cc','c':'5d','d':'65','e':'b6',
                               'f':'92'},
                          '5':{'0':'6c','1':'70','2':'48','3':'50','4':'fd',
                               '5':'ed','6':'b9','7':'da','8':'5e','9':'15',
                               'a':'46','b':'57','c':'a7','d':'8d','e':'9d',
                               'f':'84'},
                          '6':{'0':'90','1':'d8','2':'ab','3':'00','4':'8c',
                               '5':'bc','6':'d3','7':'0a','8':'f7','9':'e4',
                               'a':'58','b':'05','c':'b8','d':'b3','e':'45',
                               'f':'06'},
                          '7':{'0':'d0','1':'2c','2':'1e','3':'8f','4':'ca',
                               '5':'3f','6':'0f','7':'02','8':'c1','9':'af',
                               'a':'bd','b':'03','c':'01','d':'13','e':'8a',
                               'f':'6b'},
                          '8':{'0':'3a','1':'91','2':'11','3':'41','4':'4f',
                               '5':'67','6':'dc','7':'ea','8':'97','9':'f2',
                               'a':'cf','b':'ce','c':'f0','d':'b4','e':'e6',
                               'f':'73'},
                          '9':{'0':'96','1':'ac','2':'74','3':'22','4':'e7',
                               '5':'ad','6':'35','7':'85','8':'e2','9':'f9',
                               'a':'37','b':'e8','c':'1c','d':'75','e':'df',
                               'f':'6e'},
                          'a':{'0':'47','1':'f1','2':'1a','3':'71','4':'1d',
                               '5':'29','6':'c5','7':'89','8':'6f','9':'b7',
                               'a':'62','b':'0e','c':'aa','d':'18','e':'be',
                               'f':'1b'},
                          'b':{'0':'fc','1':'56','2':'3e','3':'4b','4':'c6',
                               '5':'d2','6':'79','7':'20','8':'9a','9':'db',
                               'a':'c0','b':'fe','c':'78','d':'cd','e':'5a',
                               'f':'f4'},
                          'c':{'0':'1f','1':'dd','2':'a8','3':'33','4':'88',
                               '5':'07','6':'c7','7':'31','8':'b1','9':'12',
                               'a':'10','b':'59','c':'27','d':'80','e':'ec',
                               'f':'5f'},
                          'd':{'0':'60','1':'51','2':'7f','3':'a9','4':'19',
                               '5':'b5','6':'4a','7':'0d','8':'2d','9':'e5',
                               'a':'7a','b':'9f','c':'93','d':'c9','e':'9c',
                               'f':'ef'},
                          'e':{'0':'a0','1':'e0','2':'3b','3':'4d','4':'ae',
                               '5':'2a','6':'f5','7':'b0','8':'c8','9':'eb',
                               'a':'bb','b':'3c','c':'83','d':'53','e':'99',
                               'f':'61'},
                          'f':{'0':'17','1':'2b','2':'04','3':'7e','4':'ba',
                               '5':'77','6':'d6','7':'26','8':'e1','9':'69',
                               'a':'14','b':'63','c':'55','d':'21','e':'0c',
                               'f':'7d'}}
    
    E_box_look_up={'0':{'0':'01','1':'03','2':'05','3':'0f','4':'11','5':'33','6':'55',
                '7':'ff','8':'1a','9':'2e','a':'72','b':'96','c':'a1','d':'f8',
                'e':'13','f':'35'},
           '1':{'0':'5f','1':'e1','2':'38','3':'48','4':'d8','5':'73','6':'95',
                '7':'a4','8':'f7','9':'02','a':'06','b':'0a','c':'1e','d':'22',
                'e':'66','f':'aa'},
           '2':{'0':'e5','1':'34','2':'5c','3':'e4','4':'37','5':'59','6':'eb',
                '7':'26','8':'6a','9':'be','a':'d9','b':'70','c':'90','d':'ab',
                'e':'e6','f':'31'},
           '3':{'0':'53','1':'f5','2':'04','3':'0c','4':'14','5':'3c','6':'44',
                '7':'cc','8':'4f','9':'d1','a':'68','b':'b8','c':'d3','d':'6e',
                'e':'b2','f':'cd'},
           '4':{'0':'4c','1':'d4','2':'67','3':'a9','4':'e0','5':'3b','6':'4d',
                '7':'d7','8':'62','9':'a6','a':'f1','b':'08','c':'18','d':'28',
                'e':'78','f':'88'},
           '5':{'0':'83','1':'9e','2':'b9','3':'d0','4':'6b','5':'bd','6':'dc',
                '7':'7f','8':'81','9':'98','a':'b3','b':'ce','c':'49','d':'db',
                'e':'76','f':'9a'},
           '6':{'0':'b5','1':'c4','2':'57','3':'f9','4':'10','5':'30','6':'50',
                '7':'f0','8':'0b','9':'1d','a':'27','b':'69','c':'bb','d':'d6',
                'e':'61','f':'a3'},
           '7':{'0':'fe','1':'19','2':'2b','3':'7d','4':'87','5':'92','6':'ad',
                '7':'ec','8':'2f','9':'71','a':'93','b':'ae','c':'e9','d':'20',
                'e':'60','f':'a0'},
           '8':{'0':'fb','1':'16','2':'3a','3':'4e','4':'d2','5':'6d','6':'b7',
                '7':'c2','8':'5d','9':'e7','a':'32','b':'56','c':'fa','d':'15',
                'e':'3f','f':'41'},
           '9':{'0':'c3','1':'5e','2':'e2','3':'3d','4':'47','5':'c9','6':'40',
                '7':'c0','8':'5b','9':'ed','a':'2c','b':'74','c':'9c','d':'bf',
                'e':'da','f':'75'},
           'a':{'0':'9f','1':'ba','2':'d5','3':'64','4':'ac','5':'ef','6':'2a',
                '7':'7e','8':'82','9':'9d','a':'bc','b':'df','c':'7a','d':'8e',
                'e':'89','f':'80'},
           'b':{'0':'9b','1':'b6','2':'c1','3':'58','4':'e8','5':'23','6':'65',
                '7':'af','8':'ea','9':'25','a':'6f','b':'b1','c':'c8','d':'43',
                'e':'c5','f':'54'},
           'c':{'0':'fc','1':'1f','2':'21','3':'63','4':'a5','5':'f4','6':'07',
                '7':'09','8':'1b','9':'2d','a':'77','b':'99','c':'b0','d':'cb',
                'e':'46','f':'ca'},
           'd':{'0':'45','1':'cf','2':'4a','3':'de','4':'79','5':'8b','6':'86',
                '7':'91','8':'a8','9':'e3','a':'3e','b':'42','c':'c6','d':'51',
                'e':'f3','f':'0e'},
           'e':{'0':'12','1':'36','2':'5a','3':'ee','4':'29','5':'7b','6':'8d',
                '7':'8c','8':'8f','9':'8a','a':'85','b':'94','c':'a7','d':'f2',
                'e':'0d','f':'17'},
           'f':{'0':'39','1':'4b','2':'dd','3':'7c','4':'84','5':'97','6':'a2',
                '7':'fd','8':'1c','9':'24','a':'6c','b':'b4','c':'c7','d':'52',
                'e':'f6','f':'01'}}
    
    L_box_look_up={'0':{'0':'','1':'00','2':'19','3':'01','4':'32','5':'02','6':'1a',
                '7':'c6','8':'4b','9':'c7','a':'1b','b':'68','c':'33','d':'ee',
                'e':'df','f':'03'},
           '1':{'0':'64','1':'04','2':'e0','3':'0e','4':'34','5':'8d','6':'81',
                '7':'ef','8':'4c','9':'71','a':'08','b':'c8','c':'f8','d':'69',
                'e':'1c','f':'c1'},
           '2':{'0':'7d','1':'c2','2':'1d','3':'b5','4':'f9','5':'b9','6':'27',
                '7':'6a','8':'4d','9':'e4','a':'a6','b':'72','c':'9a','d':'c9',
                'e':'09','f':'78'},
           '3':{'0':'65','1':'2f','2':'8a','3':'05','4':'21','5':'0f','6':'e1',
                '7':'24','8':'12','9':'f0','a':'82','b':'45','c':'35','d':'93',
                'e':'da','f':'8e'},
           '4':{'0':'96','1':'8f','2':'db','3':'bd','4':'36','5':'d0','6':'ce',
                '7':'94','8':'13','9':'5c','a':'d2','b':'f1','c':'40','d':'46',
                'e':'83','f':'38'},
           '5':{'0':'66','1':'dd','2':'fd','3':'30','4':'bf','5':'06','6':'8b',
                '7':'62','8':'b3','9':'25','a':'e2','b':'98','c':'22','d':'88',
                'e':'91','f':'10'},
           '6':{'0':'7e','1':'6e','2':'48','3':'c3','4':'a3','5':'b6','6':'1e',
                '7':'42','8':'3a','9':'6b','a':'28','b':'54','c':'fa','d':'85',
                'e':'3d','f':'ba'},
           '7':{'0':'2b','1':'79','2':'0a','3':'15','4':'9b','5':'9f','6':'5e',
                '7':'ca','8':'4e','9':'d4','a':'ac','b':'e5','c':'f3','d':'73',
                'e':'a7','f':'57'},
           '8':{'0':'af','1':'58','2':'a8','3':'50','4':'f4','5':'ea','6':'d6',
                '7':'74','8':'4f','9':'ae','a':'e9','b':'d5','c':'e7','d':'e6',
                'e':'ad','f':'e8'},
           '9':{'0':'2c','1':'d7','2':'75','3':'7a','4':'eb','5':'16','6':'0b',
                '7':'f5','8':'59','9':'cb','a':'5f','b':'b0','c':'9c','d':'a9',
                'e':'51','f':'a0'},
           'a':{'0':'7f','1':'0c','2':'f6','3':'6f','4':'17','5':'c4','6':'49',
                '7':'ec','8':'d8','9':'43','a':'1f','b':'2d','c':'a4','d':'76',
                'e':'7b','f':'b7'},
           'b':{'0':'cc','1':'bb','2':'3e','3':'5a','4':'fb','5':'60','6':'b1',
                '7':'86','8':'3b','9':'52','a':'a1','b':'6c','c':'aa','d':'55',
                'e':'29','f':'9d'},
           'c':{'0':'97','1':'b2','2':'87','3':'90','4':'61','5':'be','6':'dc',
                '7':'fc','8':'bc','9':'95','a':'cf','b':'cd','c':'37','d':'3f',
                'e':'5b','f':'d1'},
           'd':{'0':'53','1':'39','2':'84','3':'3c','4':'41','5':'a2','6':'6d',
                '7':'47','8':'14','9':'2a','a':'9e','b':'5d','c':'56','d':'f2',
                'e':'d3','f':'ab'},
           'e':{'0':'44','1':'11','2':'92','3':'d9','4':'23','5':'20','6':'2e',
                '7':'89','8':'b4','9':'7c','a':'b8','b':'26','c':'77','d':'99',
                'e':'e3','f':'a5'},
           'f':{'0':'67','1':'4a','2':'ed','3':'de','4':'c5','5':'31','6':'fe',
                '7':'18','8':'0d','9':'63','a':'8c','b':'80','c':'c0','d':'f7',
                'e':'70','f':'07'}}
    
    rcon_words=[['01','00','00','00'],
                ['02','00','00','00'],
                ['04','00','00','00'],
                ['08','00','00','00'],
                ['10','00','00','00'],
                ['20','00','00','00'],
                ['40','00','00','00'],
                ['80','00','00','00'],
                ['1b','00','00','00'],
                ['36','00','00','00']]
    
    def __init__(self):
        self.message=''
        self.key=''
        self.key_list=[]
        self.key_decrypt_list=[]
        self.encrypt=False
# mathematical operation functions:-

    def xor_operation(self,value_1,value_2): 
        value_1=[self.look_up_HexToBin[i] for i in value_1]
        value_2=[self.look_up_HexToBin[i] for i in value_2]
        xor_list=[]
        for i,j in zip(value_1,value_2): 
            nibble=''
            for k,l in zip(i,j): 
                nibble+=str(int(k)^int(l))
            xor_list.append(nibble)
        return ''.join([self.look_up_BinToHex[i] for i in xor_list])
    
    # the product here uses something called as GALOIS FIELD concept
    # galois field is nothing but whenever we perform any operation 
    # addition, subtraction, multiplication, division we get the result 
    # within the boundary...
    # in AES we gf(2^8)=gf(256), i.e, we will have 256 different values...
    
    def product_function(self,polynomial_1,polynomial_2): 
        product=[0 for i in range(len(polynomial_1)+len(polynomial_2)-1)]
        for i in range(len(polynomial_1)):
            for j in range(len(polynomial_2)):
                # the addition here is XOR operation...
                product[i+j]=product[i+j]^polynomial_1[i]*polynomial_2[j]
        if product[6]==0: 
            value=''.join([str(i) for i in product[7:]])
            return self.hex_lookup(value)
        else:
            # this is the condition where the degree of the polynomial 
            # is greater than the gf(2^8)
            # so we use irreducible polynomial to reduce the polynomial
            # in AES we x^8+x^4+x^3+x+1 
            # Note:- by changing the irreducible polynomial we have to change 
            # the s-box also...
            manipulation=[]
            for i,j in zip(product[6:],[1,0,0,0,1,1,0,1,1]):
                manipulation.append(i^j)
            value=''.join([str(i) for i in manipulation[1:]])
            return self.hex_lookup(value)
        
    def matrix_transpose(self,matrix): 
        t_matrix=[]
        row_1,row_2,row_3,row_4=[],[],[],[]
        for i in range(len(matrix)): 
            row_1.append(matrix[i][0])
            row_2.append(matrix[i][1])
            row_3.append(matrix[i][2])
            row_4.append(matrix[i][3])
        t_matrix.append(row_1)
        t_matrix.append(row_2)
        t_matrix.append(row_3)
        t_matrix.append(row_4)
        return t_matrix
        
# plain-text to hex-text conversion:-
  
    def hex_lookup(self,value): 
        first_half=self.look_up_BinToHex[value[0:len(value)//2]]
        second_half=self.look_up_BinToHex[value[len(value)//2:]]
        return first_half+second_half
        
    def convert_to_hexformat(self,value): 
        value=bin(value)[2:]
        if len(value)==8: 
            return self.hex_lookup(value)
        else: 
            temp=value[::-1]
            for i in range(8-len(temp)): 
                temp+='0'
            value=temp[::-1]
            return self.hex_lookup(value)
        
    def convert_plaintext_to_hexformat(self): # main method-1
        final_hexformat=''
        for i in self.message: 
            ascii_value=ord(i)
            final_hexformat+=self.convert_to_hexformat(ascii_value)
        return final_hexformat 
    
# taking the hex string and forming batches of 16-bytes 
# then converting them to matrix form 

    def hex_string_batches(self,string):  # code can be improved...
        batches=list()
        for i in range(0,len(string),32):
            batches.append(string[i:i+32])
        for i in batches: 
            if len(i)==32: 
                continue
            else: 
                temp=i
                index=batches.index(i)
                length_to_be_padded=hex(((32-len(temp))//2))[2:]
                if len(length_to_be_padded)<2: 
                    length_to_be_padded=(length_to_be_padded[::-1]+'0')[::-1]
                temp=temp+length_to_be_padded*((32-len(i))//2)
                batches[index]=temp
            # print(batches)
        return batches 
    
    # string can contain upto 3125 characters and it may take 0.003 appro
    # to make batches
    def state_matrix(self,hex_string): # main method-2
        string_batches=self.hex_string_batches(hex_string)
        matrix_format=list()
        for i in string_batches: 
            temp_list=[]
            temp_innerlist=[]
            for j in range(0,32,2): 
                temp_innerlist.append(i[j:j+2])
            temp_element=[]
            for k in temp_innerlist: 
                if len(temp_element)==4: 
                    temp_list.append(temp_element)
                    temp_element=[]
                    temp_element.append(k)
                else: 
                     temp_element.append(k)
            temp_list.append(temp_element)
            matrix_format.append(temp_list)
        return matrix_format 
        
# key expansion:-

    # key is taken and in row matrix, so we need to transpose it using 
    # matrix_traspose to change to column matrix...

    def rotate_function(self,word,value): 
        return word[value:]+word[:value]
    
    def inverse_rotate(self,word,value):
        return word[-value:]+word[:-value]
    
    def s_box_substitution(self,word): 
        sub_word=list()
        for i in word: 
            temp=''
            _x,_y=i[0],i[1]
            temp=self.s_box_look_up[_x][_y]
            sub_word.append(temp)
        return sub_word

    # operates on words... 16-bytes
    
    def xor_function(self,first_word,second_word): 
        g_word=list()
        for i,j in zip(first_word,second_word): 
            g_word.append(self.xor_operation(i,j))
        return g_word
            
    def g_word_function(self,word,index): 
        # cyclic left shift by one byte 
        # we get rot word x1
        # s-box substitution, after that we get y1
        # xor with round list (rcon_words reference)
        
        rot_word=self.rotate_function(word,1)
        sub_word=self.s_box_substitution(rot_word)
        g_word=self.xor_function(sub_word,self.rcon_words[index])
        return g_word
        
    def convert_key_to_hexformat(self,key=None): 
        final_hexformat=''
        if self.encrypt==True:
            for i in self.key: 
                ascii_value=ord(i)
                final_hexformat+=self.convert_to_hexformat(ascii_value)
            return final_hexformat
        else:
            for i in key: 
                ascii_value=ord(i)
                final_hexformat+=self.convert_to_hexformat(ascii_value)
            return final_hexformat
        
    def key_expansion(self,key=None): # default key=None     # main-method 3 
        if self.encrypt==True: 
            # key_hexformat=self.convert_key_to_hexformat()
            key_hexformat=self.key
            key_matrix=self.state_matrix(key_hexformat)
            self.key_list.extend(key_matrix) # not append, but use extend
            i=0
            while i<10: 
                temp=[]
                word_1,word_2,word_3,word_4=self.key_list[i]            
                word_g=self.g_word_function(word_4,i)  
                word_11=self.xor_function(word_1,word_g)
                word_22=self.xor_function(word_11,word_2)
                word_33=self.xor_function(word_22,word_3)
                word_44=self.xor_function(word_33,word_4)
                temp.append(word_11)
                temp.append(word_22)
                temp.append(word_33)
                temp.append(word_44)
                word_11,word_22,word_33,word_44=None,None,None,None
                self.key_list.append(temp)  # error made here 
                temp=[]
                i+=1
            temp_1=[]
            for i in self.key_list:
                temp_1.append(self.matrix_transpose(i))
            self.key_list=temp_1
        else:
            # key_hexformat=self.convert_key_to_hexformat(key)
            # print('key on decryption:- '+key)
            key_hexformat=key
            key_matrix=self.state_matrix(key_hexformat)
            self.key_decrypt_list.extend(key_matrix)
            i=0
            while i<10: 
                temp=[]
                word_1,word_2,word_3,word_4=self.key_decrypt_list[i]            
                word_g=self.g_word_function(word_4,i)  
                word_11=self.xor_function(word_1,word_g)
                word_22=self.xor_function(word_11,word_2)
                word_33=self.xor_function(word_22,word_3)
                word_44=self.xor_function(word_33,word_4)
                temp.append(word_11)
                temp.append(word_22)
                temp.append(word_33)
                temp.append(word_44)
                word_11,word_22,word_33,word_44=None,None,None,None
                self.key_decrypt_list.append(temp)
                temp=[]
                i+=1     
            temp_1=[]
            for i in self.key_decrypt_list:
                temp_1.append(self.matrix_transpose(i))
            self.key_decrypt_list=temp_1
            
    # all the keys for all the rounds are stored in key_list
    
# sub-bytes (substitution):-
    
    # the function below s_box_substitution_inverse was written coz, while key expansion
    # we use s_box look up not inverse s_box...

    def s_box_substitution_inverse(self,word): 
            sub_word=list()
            for i in word:
                temp=''
                _x,_y=i[0],i[1]
                temp=self.s_box_inverse_look_up[_x][_y]
                sub_word.append(temp)
            return sub_word

    def sub_bytes(self,matrix):        # main method-4
        if self.encrypt==True:
            substituted_matrix=list()
            for i in matrix: 
                substituted_matrix.append(self.s_box_substitution(i))
            return substituted_matrix
        else:
            substituted_matrix=list()
            for i in matrix: 
                substituted_matrix.append(self.s_box_substitution_inverse(i))
            return substituted_matrix

# shift_rows:-
    
    def shift_rows(self,matrix):   # main method-5
        shifted_matrix=list()
        if self.encrypt==True:
            for i in range(len(matrix)):
                shifted_matrix.append(self.rotate_function(matrix[i],i))
            return shifted_matrix
        else:
            for i in range(len(matrix)): 
                shifted_matrix.append(self.inverse_rotate(matrix[i],i))
            return shifted_matrix
        
# mix columns method for encryption:-
    
    def helper_function(self,hex_string):
        value_1=hex_string[0]
        value_2=hex_string[1]
        binary_format=self.look_up_HexToBin[value_1]+self.look_up_HexToBin[value_2]
        binary_format=[int(i) for i in binary_format]
        return binary_format
    
    def helper_function_xor(self,temp): 
        xor_result_1=self.xor_operation(temp[0],temp[1])
        xor_result_2=self.xor_operation(temp[2],temp[3])
        return self.xor_operation(xor_result_1,xor_result_2)
        
    def mixColumns(self,matrix):     # main method-6
        # the multiplicaiton matrix used in AES-128 bit key during encryption
        # 02 03 01 01
        # 01 02 03 01 
        # 01 01 02 03
        # 03 01 01 02 
        
        if self.encrypt==True:
            multiplication_matrix=[['02','03','01','01'],
                                   ['01','02','03','01'],
                                   ['01','01','02','03'],
                                   ['03','01','01','02']]
            final_result=[]
            matrix=self.matrix_transpose(matrix)
            for i in matrix: 
                temp=[]
                inner_list=[]
                for j in multiplication_matrix:                 
                    product_1=self.product_function(self.helper_function(j[0]),self.helper_function(i[0]))
                    product_2=self.product_function(self.helper_function(j[1]),self.helper_function(i[1]))
                    product_3=self.product_function(self.helper_function(j[2]),self.helper_function(i[2]))
                    product_4=self.product_function(self.helper_function(j[3]),self.helper_function(i[3]))
                    temp.append(product_1)
                    temp.append(product_2)
                    temp.append(product_3)
                    temp.append(product_4)
                    inner_list.append(self.helper_function_xor(temp))
                    temp=[]
                final_result.append(inner_list)
                inner_list=[]  
            return self.matrix_transpose(final_result) #error made here ...
        
            # during decryption i was getting error in ireducible polynomial
            # so i searched for various resources,and found look_up table 
            # for galois field multiplicaiton...
            # the same look_up tables can be used for encryption also...
        
    def hex_decimal(self,element):  # hex number to decimal number
        value=''.join([self.look_up_HexToBin[i] for i in element])[::-1]
        sum_=0
        for i in range(len(value)): 
            sum_+=pow(2,i)*int(value[i])
        return sum_
    
    def hex_operation(self,operand_1,operand_2,flag=False):  # addition and subtraction
        value_1=''.join([self.look_up_HexToBin[i] for i in operand_1])[::-1]
        value_2=''.join([self.look_up_HexToBin[i] for i in operand_2])[::-1]
        decimal_1,decimal_2=0,0
        for i in range(len(value_1)): 
            decimal_1+=pow(2,i)*int(value_1[i])
        for i in range(len(value_2)): 
            decimal_2+=pow(2,i)*int(value_2[i])
        result=0
        if flag==True:
            result=abs(decimal_1+decimal_2)
            return hex(result)[2:]
        else:
            result=abs(decimal_1-decimal_2)
            if len(hex(result)[2:])==1: 
                return '0'+hex(result)[2:]
            else: 
                return hex(result)[2:]

    def L_box(self,element):  # l-box look up
        return self.L_box_look_up[element[0]][element[1]]

    def E_box(self,element):   # e-box look up after hex operation
        if self.hex_decimal(element)<self.hex_decimal('ff'): 
            return self.E_box_look_up[element[0]][element[1]]
        else:
            difference=self.hex_operation(element,'ff')
            return self.E_box_look_up[difference[0]][difference[1]]
        
    def helper_function_for_inverse(self,block_1,block_2): 
        temp=[]
        for i,j in zip(block_1,block_2): 
            L_value1=self.L_box(i)
            if j=='00':             # max time spent 7 hrs when anything multiplied by 0 results in 0
                temp.append('00')
                continue
            L_value2=self.L_box(j)
            addition=self.hex_operation(L_value1,L_value2,flag=True)
            checking=self.E_box(addition)
            temp.append(checking)
        return self.helper_function_xor(temp)

    def inverse_mixColumns(self,matrix):   # use for decryption process...
        matrix=self.matrix_transpose(matrix)
        multiplication_matrix=[['0e','0b','0d','09'],
                                ['09','0e','0b','0d'],
                                ['0d','09','0e','0b'],
                                ['0b','0d','09','0e']]
        final_matrix=list()
        for i in matrix:
            temp=[]
            for j in multiplication_matrix: 
                product_and_sum=self.helper_function_for_inverse(j,i)
                temp.append(product_and_sum)
            final_matrix.append(temp)
            temp=[]
        return self.matrix_transpose(final_matrix)
    
    def two_matrix_xor_operation(self,matrix_1,matrix_2):  # main method-7
        final_matrix=list()
        for i,j in zip(matrix_1,matrix_2): 
            final_matrix.append(self.xor_function(i,j))
        return final_matrix
            
# encryption:-

    # outputs the final cipher-text...
    
    def binary_to_decimal(self,value): 
        temp=[int(i) for i in value][::-1]
        sum_=0
        for i in range(len(temp)):
            sum_+=pow(2,i)*temp[i]
        return sum_
                
    def convert_hex_to_plaintext(self,matrix): 
        final_ciphertext=''
        for i in matrix: 
            for j in i: 
                decimal=self.binary_to_decimal(''.join([self.look_up_HexToBin[k] for k in j]))
                final_ciphertext+=chr(decimal)
        return final_ciphertext
    
    def matrix_to_string(self,matrix): 
        temp=''
        for i in matrix: 
            for j in i: 
                temp+=j
        return temp

    def encryption(self,message,key): 
        self.encrypt=True  # make true when encryption...
        self.message=message
        self.key=key
        hex_string=self.convert_plaintext_to_hexformat()   
        print('message in hex format:-'+hex_string)             
        input_state_matrix=list()
        for block in self.state_matrix(hex_string):
            input_state_matrix.append(self.matrix_transpose(block))
        self.key_expansion()
        key_expansion_list=self.key_list
        cipher_text=''
        for block in input_state_matrix:
            round_input=self.two_matrix_xor_operation(block,key_expansion_list[0])
            i=1
            while i<=9: 
                sub=self.sub_bytes(round_input)
                shift=self.shift_rows(sub)
                mix=self.mixColumns(shift)
                round_input=self.two_matrix_xor_operation(mix,key_expansion_list[i])
                i+=1
            round_10_sub=self.sub_bytes(round_input)
            round_10_shift=self.shift_rows(round_10_sub)
            temp=self.two_matrix_xor_operation(round_10_shift,key_expansion_list[10])
            temp=self.matrix_transpose(temp)
            temp=self.matrix_to_string(temp)
            cipher_text+=temp
            temp=''
            round_input=''
        self.key_list=[]   # resetting the key list to None 
        self.encrypt=False
        # print(self.key_decrypt_list) # this list is empty when encrypting...
        
        return cipher_text

# decryption:-
    
    def decryption(self,cipher_text,key):  # may be each person with different key...
        cipher_state_matrix=[]
        for block in self.state_matrix(cipher_text):
            cipher_state_matrix.append(self.matrix_transpose(block))
        self.key_expansion(key)
        key_expansion_list=self.key_decrypt_list
        message=''
        for block in cipher_state_matrix: 
            mix=self.two_matrix_xor_operation(block,key_expansion_list[10])
            shift=self.shift_rows(mix)
            sub=self. sub_bytes(shift)
            round_input=self.two_matrix_xor_operation(sub, key_expansion_list[9])
            i=8
            while i>=0:                 
                mix=self.inverse_mixColumns(round_input)                
                shift=self.shift_rows(mix)                
                sub=self.sub_bytes(shift)                
                round_input=self.two_matrix_xor_operation(sub,key_expansion_list[i])
                i-=1  
            shift=self.shift_rows(mix)
            sub=self.sub_bytes(shift)
            round_input=self.two_matrix_xor_operation(sub,key_expansion_list[0])
            temp=self.matrix_transpose(round_input)
            temp=self.matrix_to_string(temp)
            message+=temp
            self.key_decrypt_list=[]  # resetting the key to None...
        return message    
        
def encryption():
    crypto=AES()
    message='hellop'
    # key=Md5('hello').hash()
    # print('key:-'+key) 
    # print(crypto.encryption(message,key))
 
def decryption(): 
    crypto=AES()
    message='hi how are' 
    key=Md5('helloworld')
    key1=key.hash()
    # print(key1)
    # print(crypto.decryption(crypto.encryption('',key1),key1))
    encrypted_cipher=crypto.encryption(message,key1)
    print('encrypted cipher:- '+encrypted_cipher)
    print('decrypted cipher:- '+crypto.decryption(encrypted_cipher,key1))
    
    
    # print(crypto.decryption(crypto.encryption(message,key),'abcdefghijklmnop'))

def main():
#    MESSAGE=input('Enter the message: ')
#    KEY=input('Enter the unique code')
    # encryption()
    decryption() 
start=time()

main()

end=time()

print(end-start)        
 
# the main problem is the key
# generate the key using hash function (128 bit key size)