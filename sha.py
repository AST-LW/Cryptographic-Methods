# still onGoing...
# sha-1 is completed

class SHA(): 

    __constants_SHA_1=['5a827999','6ed9eba1','8f1bbcdc','ca62c1d6']
    __initial_hash_SHA_1=['67452301','efcdab89','98badcfe','10325476','c3d2e1f0']

    __look_up_BinToHex={'0000':'0','0001':'1','0010':'2','0011':'3','0100':'4',
                      '0101':'5','0110':'6','0111':'7','1000':'8','1001':'9',
                      '1010':'a','1011':'b','1100':'c','1101':'d','1110':'e',
                      '1111':'f'}
    
    __look_up_HexToBin={'0':'0000','1':'0001','2':'0010','3':'0011','4':'0100',
                      '5':'0101','6':'0110','7':'0111','8':'1000','9':'1001',
                      'a':'1010','b':'1011','c':'1100','d':'1101','e':'1110',
                      'f':'1111'}

    def __init__(self,message): 
        self.message=message

    def __check_for_8_bit(self,binary_string): 
        binary_8_bit_format=binary_string
        if len(binary_8_bit_format)<8: 
            binary_8_bit_format=(binary_8_bit_format[::-1]+''.join(['0' for i in range(8-len(binary_8_bit_format))]))[::-1]
        return binary_8_bit_format
    
    def __check_for_32_bits(self,binary_string): 
        binary_32_bit_format=binary_string
        if len(binary_string)<32: 
            binary_32_bit_format=(binary_32_bit_format[::-1]+''.join(['0' for i in range(0,32-len(binary_32_bit_format))]))[::-1]
        return binary_32_bit_format
    
    def __check_for_64_bits(self,binary_string): 
        binary_64_bit_format=binary_string
        if len(binary_64_bit_format)<64: 
            binary_64_bit_format=(binary_64_bit_format[::-1]+''.join(['0' for i in range(64-len(binary_64_bit_format))]))[::-1]
        return binary_64_bit_format
    
    def __check_for_128_bits(self,binary_string): 
        binary_128_bit_format=binary_string
        if len(binary_128_bit_format)<128: 
            binary_128_bit_format=(binary_128_bit_format[::-1]+''.join(['0' for i in range(128-len(binary_128_bit_format))]))[::-1]
        return binary_128_bit_format

    def __convert_decimal_to_binary(self,number,number_of_bits=32): 
        if number_of_bits==32: 
            return self.__check_for_32_bits(bin(number)[2:])
        else: 
            return self.__check_for_64_bits(bin(number)[2:])
    
    def __convert_binary_to_decimal(self,binary_string): 
        return int('0b'+binary_string,2)
    
    def __convert_binary_to_hex(self,binary_string): 
        hex_output=''
        for i in range(0,len(binary_string),4): 
            hex_output+=self.__look_up_BinToHex[binary_string[i:i+4]]
        return hex_output
    
    def __convert_hex_to_binary(self,hex_string): 
        binary_output=''
        for i in hex_string: 
            binary_output+=self.__look_up_HexToBin[i]
        return binary_output

    def __modulo_addition(self,operand_1,operand_2,modulo_power=32):   # perform the addition on integer format
        return (operand_1+operand_2)%pow(2,modulo_power)

    def __rotate_left_shift(self,element,number_of_times,default=32): 
        return (element<<number_of_times)|(element>>(default-number_of_times))

    def __message_to_binary_format(self): 
        binary_format=''
        for i in self.message: 
            binary_format+=self.__check_for_8_bit(bin(ord(i))[2:])
        return binary_format

    def __append_padding_bits(self,binary_string,number_of_bits=512):
        length_of_message=len(binary_string)
        i=1
        while True: 
            if(number_of_bits*i<length_of_message): 
                i+=1
                continue
            else: 
                break
        if number_of_bits==512: 
            subtract_bits=64
        else: 
            subtract_bits=128
        append_zero_bits=''.join(['0' for i in range(1,number_of_bits*i-subtract_bits-length_of_message)])
        binary_string=binary_string+'1'+append_zero_bits
        return binary_string

    def __append_length(self,binary_string,number_of_bits=512): 
        length_of_message_bits=len(self.message)*8
        binary_format=self.__convert_decimal_to_binary(length_of_message_bits)
        if number_of_bits==512:
            return binary_string+self.__check_for_64_bits(binary_format)
        if number_of_bits==1024: 
            return binary_string+self.__check_for_128_bits(binary_format)
        
    def __possible_blocks(self,binary_string,number_of_bits=512): 
        result=[]
        for i in range(0,len(binary_string),number_of_bits): 
            result.append(binary_string[i:i+number_of_bits])
        return result

    def __split_into_blocks(self,binary_string,slice_into=32): 
        result=[]
        for i in range(0,len(binary_string),slice_into): 
            result.append(binary_string[i:i+slice_into])
        return result

    def __functions(self,first_term,second_term,third_term,function_type=None,standard=None):
        if standard=='sha':
            if function_type=='ch': 
                return (first_term & second_term) ^ (~first_term & third_term)
            if function_type=='parity': 
                return first_term ^ second_term ^ third_term
            if function_type=='maj': 
                return (first_term & second_term) ^ (first_term & third_term) ^ (second_term & third_term)
    
    def __sha(self,message_blocks):
        hash_output=''
        __constants=self.__constants_SHA_1
        for i in __constants:
            __constants[__constants.index(i)]=int('0b'+self.__convert_hex_to_binary(i),2)            
        buffer_a=int('0b'+self.__convert_hex_to_binary(self.__initial_hash_SHA_1[0]),2)
        buffer_b=int('0b'+self.__convert_hex_to_binary(self.__initial_hash_SHA_1[1]),2)
        buffer_c=int('0b'+self.__convert_hex_to_binary(self.__initial_hash_SHA_1[2]),2)
        buffer_d=int('0b'+self.__convert_hex_to_binary(self.__initial_hash_SHA_1[3]),2)
        buffer_e=int('0b'+self.__convert_hex_to_binary(self.__initial_hash_SHA_1[4]),2)
        hex_constats=[buffer_a,buffer_b,buffer_c,buffer_d,buffer_e]
        function_output=None
        flag=False
        for i in message_blocks: 
            message_32_bit_blocks=self.__split_into_blocks(i)
            if flag==True:
                buffer_a,buffer_b,buffer_c,buffer_d,buffer_e=hex_constants 
            for j in message_32_bit_blocks: 
                message_32_bit_blocks[message_32_bit_blocks.index(j)]=int('0b'+j,2)
            temp=[]
            for l in range(4*20): 
                if 0<=l<16: 
                    temp.append(message_32_bit_blocks[l])
                if 16<=l<80:
                    temp.append((self.__rotate_left_shift(temp[l-3]^temp[l-8]^temp[l-14]^temp[l-16],1))%pow(2,32)) # the value should be in range 2**32
            message_32_bit_blocks=temp
            for k in range(4*20):
                if 0<=k<20: 
                    function_output=self.__functions(buffer_b,buffer_c,buffer_d,function_type='ch',standard='sha')
                    constant=__constants[0]
                if 20<=k<40: 
                    function_output=self.__functions(buffer_b,buffer_c,buffer_d,function_type='parity',standard='sha')
                    constant=__constants[1]
                if 40<=k<60: 
                    function_output=self.__functions(buffer_b,buffer_c,buffer_d,function_type='maj',standard='sha')
                    constant=__constants[2]
                if 60<=k<80: 
                    function_output=self.__functions(buffer_b,buffer_c,buffer_d,function_type='parity',standard='sha')
                    constant=__constants[3]
                temp=self.__rotate_left_shift(buffer_a,5)
                temp=self.__modulo_addition(function_output,temp)
                temp=self.__modulo_addition(temp,buffer_e)
                temp=self.__modulo_addition(temp,constant)
                temp=self.__modulo_addition(temp,message_32_bit_blocks[k])
                buffer_e=buffer_d
                buffer_d=buffer_c
                buffer_c=self.__rotate_left_shift(buffer_b,30)
                buffer_b=buffer_a
                buffer_a=temp
            flag=True
            hex_constats[0]=(buffer_a+hex_constats[0])%pow(2,32)
            hex_constats[1]=(buffer_b+hex_constats[1])%pow(2,32)
            hex_constats[2]=(buffer_c+hex_constats[2])%pow(2,32)
            hex_constats[3]=(buffer_d+hex_constats[3])%pow(2,32)
            hex_constats[4]=(buffer_e+hex_constats[4])%pow(2,32)
        for i in hex_constats: 
            hash_output+=self.__convert_decimal_to_binary(i)
        hash_output=self.__convert_binary_to_hex(hash_output)
        return hash_output
            
    def SHA_Standard(self): 
        message_in_binary_format=self.__message_to_binary_format()
        message_in_binary_format=self.__append_padding_bits(message_in_binary_format)
        message_in_binary_format=self.__append_length(message_in_binary_format)
        message_possible_blocks=self.__possible_blocks(message_in_binary_format)
        return self.__sha(message_possible_blocks)     


obj=SHA('')
print(obj.SHA_Standard())