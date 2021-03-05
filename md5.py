class Md5:
    # __A, __B, __C, __D are written in little endian manner in computation process
    # little endian example:-
    # 01 23 45 67 
    # output:- 67 45 23 01 

    __A='01234567'
    __B='89abcdef'
    __C='fedcba98'
    __D='76543210'

    __look_up_BinToHex={'0000':'0','0001':'1','0010':'2','0011':'3','0100':'4',
                      '0101':'5','0110':'6','0111':'7','1000':'8','1001':'9',
                      '1010':'a','1011':'b','1100':'c','1101':'d','1110':'e',
                      '1111':'f'}
    
    __look_up_HexToBin={'0':'0000','1':'0001','2':'0010','3':'0011','4':'0100',
                      '5':'0101','6':'0110','7':'0111','8':'1000','9':'1001',
                      'a':'1010','b':'1011','c':'1100','d':'1101','e':'1110',
                      'f':'1111'}
    
    # constants are not written in little endian format, so no need to apply the conversion 

    __K=['d76aa478', 'e8c7b756', '242070db', 'c1bdceee',
       'f57c0faf', '4787c62a', 'a8304613', 'fd469501',
       '698098d8', '8b44f7af', 'ffff5bb1', '895cd7be',
       '6b901122', 'fd987193', 'a679438e', '49b40821',
       'f61e2562', 'c040b340', '265e5a51', 'e9b6c7aa',
       'd62f105d', '02441453', 'd8a1e681', 'e7d3fbc8',
       '21e1cde6', 'c33707d6', 'f4d50d87', '455a14ed',
       'a9e3e905', 'fcefa3f8', '676f02d9', '8d2a4c8a',
       'fffa3942', '8771f681', '6d9d6122', 'fde5380c',
       'a4beea44', '4bdecfa9', 'f6bb4b60', 'bebfbc70',
       '289b7ec6', 'eaa127fa', 'd4ef3085', '04881d05',
       'd9d4d039', 'e6db99e5', '1fa27cf8', 'c4ac5665',
       'f4292244', '432aff97', 'ab9423a7', 'fc93a039',
       '655b59c3', '8f0ccc92', 'ffeff47d', '85845dd1',
       '6fa87e4f', 'fe2ce6e0', 'a3014314', '4e0811a1',
       'f7537e82', 'bd3af235', '2ad7d2bb', 'eb86d391']

    # number of times to be shifted (predefined) 
    __S=[7,12,17,22,7,12,17,22,7,12,17,22,7,12,17,22,
         5, 9,14,20,5, 9,14,20,5, 9,14,20,5, 9,14,20,
         4,11,16,23,4,11,16,23,4,11,16,23,4,11,16,23,
         6,10,15,21,6,10,15,21,6,10,15,21,6,10,15,21]
    
    def __init__(self,message): 
        self.message=message

    # if inputs are in hex format...
    def __conversion_little_endian(self,elements):  
        for i in elements: 
            temp=[]
            for j in range(0,len(i),2): 
                temp.append(i[j:j+2])
            temp=temp[::-1]
            temp=''.join(temp)
            elements[elements.index(i)]=temp
        return elements
    
    # method for converting, from hex format to binary
    def __hex_to_binary(self,element): 
        binary_output=''
        for i in element: 
            binary_output+=self.__look_up_HexToBin[i]
        return binary_output

    # method for converting, from binary to hex
    def __binary_to_hex(self,element): 
        hex_output=''
        for i in range(0,len(element),4): 
            hex_output+=self.__look_up_BinToHex[element[i:i+4]]
        return hex_output

    # method for performing internal operations    
    def __function(self,first_term,second_term,third_term,function_type=None): # default arguments should be placed at last
        if function_type=='f': 
            return (first_term & second_term)|(~first_term & third_term)
        if function_type=='g':
            return (first_term & third_term)|(second_term & ~third_term)
        if function_type=='h': 
            return first_term ^ second_term ^ third_term
        if function_type=='i': 
            return second_term ^ (first_term | ~third_term)

    # method for left shift(input is in base 10 format)   
    def __rotate_left_shift(self,element,number_of_times): 
        return (element<<number_of_times)|(element>>(32-number_of_times))

    # method for addition ( addition modulo 2^32)
    def __modular_add(self,operand_1,operand_2):
        return (operand_1+operand_2)%pow(2,32)

    # method for converting, from ascii to binary format
    def __convert_to_binary_format(self):   # protected methods
        self.__binary_format='' # protected members, outside the class not available
        for i in self.message: 
            value=bin(ord(i))[2:]
            if len(value)<8: 
                value=(value[::-1]+''.join(['0' for i in range(0,8-len(value))]))[::-1]
            self.__binary_format+=value
    
    # method for appending the bits of length 512*n-64 
    def __append_padding_bits(self):
        self.__appending_bits='1'
        self.__length_of_message=len(self.__binary_format)
        i=1 
        while True: 
            if(512*i<self.__length_of_message): 
                i+=1 
                continue 
            else:  
                break       
        self.__appending_bits+=''.join(['0' for i in range(1,512*i-64-self.__length_of_message)])
        self.__append_bits=self.__binary_format+self.__appending_bits  # the length should be multiple of 512
        # converting to little-endian 
        temp=''
        for i in range(0,len(self.__append_bits),8): 
            temp+=self.__append_bits[i:i+8][::-1]
        self.__append_bits=temp
        
    # method for appending additional length so that the total length will become equal to multiple of 512        
    def __append_length(self):
        temp=''
        binary_format=bin(len(self.message)*8)[2:]
        if len(binary_format)<64: 
            binary_format=(binary_format[::-1]+''.join(['0' for i in range(64-len(binary_format))]))[::-1]
        # converting to little endian for 8 bit
        for i in range(0,len(binary_format),32): 
            temp+=binary_format[i:i+32][::-1]
        # converting to little endian for 32 bit
        temp=temp[32:]+temp[:32]   
        self.__final_message_format=self.__append_bits+temp

    # method for splitting into 512-bit message length
    def __possible_blocks(self):  # text this with large block
        self.__blocks=[] 
        for i in range(0,len(self.__final_message_format),512): 
            self.__blocks.append(self.__final_message_format[i:i+512])
        
    # method for splitting the 512-bit into 32-bit length 
    def __split_to_32_bits(self,string): 
        result=[]
        for i in range(0,len(string),32): 
            result.append(string[i:i+32])
        return result

    # method where main operation is performed
    def __inner_operation(self):
        temp_list=self.__conversion_little_endian([self.__A,self.__B,self.__C,self.__D])
        constants_list=self.__K
        for i in  constants_list: 
            constants_list[constants_list.index(i)]=int('0b'+self.__hex_to_binary(i),2)
        buffer_a=int('0b'+self.__hex_to_binary(temp_list[0]),2)
        buffer_b=int('0b'+self.__hex_to_binary(temp_list[1]),2)
        buffer_c=int('0b'+self.__hex_to_binary(temp_list[2]),2)
        buffer_d=int('0b'+self.__hex_to_binary(temp_list[3]),2)
        buffer_list=[buffer_a,buffer_b,buffer_c, buffer_d] 
        function_output=None
        message_in_32_bit_format=[]   # there will be 16 elements
        for i in self.__blocks:
            message_in_32_bit_format.append(self.__split_to_32_bits(i))
        flag=False # first time execution of loop
        for elements in message_in_32_bit_format: 
            function_output=None
            binary_to_integer_format=[]
            if flag==True: 
                buffer_list=[self.__A,self.__B,self.__C,self.__D] # second we will have in base 10 format 
                buffer_a=temp_list[0]
                buffer_b=temp_list[1]
                buffer_c=temp_list[2]
                buffer_d=temp_list[3]
            for i in elements: 
                binary_to_integer_format.append(int('0b'+i[::-1],2))
            for i in range(4*16): # 4 rounds, each of 16 operations
                if i<16: 
                    k=i
                    function_output=self.__function(buffer_b,buffer_c,buffer_d,'f')
                if 16<=i<32: 
                    k=((i*5)+1)%16
                    function_output=self.__function(buffer_b,buffer_c,buffer_d,'g')
                if 32<=i<48:
                    k=((i*3)+5)%16
                    temp_1=k
                    function_output=self.__function(buffer_b,buffer_c,buffer_d,'h')
                if 48<=i<64:      
                    k=(i*7)%16
                    function_output=self.__function(buffer_b,buffer_c,buffer_d,'i')
                buffer_addition=self.__modular_add(function_output,binary_to_integer_format[k])
                buffer_addition=self.__modular_add(buffer_addition,constants_list[i])
                buffer_addition=self.__modular_add(buffer_addition,buffer_a)
                buffer_addition=self.__rotate_left_shift(buffer_addition,self.__S[i])
                buffer_addition=self.__modular_add(buffer_addition,buffer_b)
                buffer_a=buffer_d
                buffer_d=buffer_c
                buffer_c=buffer_b
                buffer_b=buffer_addition
            flag= True
            self.__A=self.__modular_add(buffer_a,buffer_list[0])
            self.__B=self.__modular_add(buffer_b,buffer_list[1])
            self.__C=self.__modular_add(buffer_c,buffer_list[2])
            self.__D=self.__modular_add(buffer_d,buffer_list[3])

    # method that performs final manipulations
    def __final_conversion(self): 
        hash_output=''
        buffer_list=[self.__A,self.__B,self.__C,self.__D]
        for i in buffer_list: 
            temp=bin(i)[2:]
            if len(temp)<32: 
                temp=(temp[::-1]+''.join(['0' for i in range(32-len(temp))]))[::-1]
            temp=''.join([temp[j:j+8]  for j in range(0,len(temp),8)][::-1])
            
            hash_output+=self.__binary_to_hex(temp)
        return hash_output 
 
    def hash(self): 
        self.__convert_to_binary_format()
        self.__append_padding_bits() 
        self.__append_length()
        self.__possible_blocks()
        self.__inner_operation()
        return self.__final_conversion()
         
# obj=Md5('Hello, world!')
# print(obj.hash())

       