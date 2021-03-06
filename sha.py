# sha-1 andc sha-256

class SHA(): 

    # predefined constants

    __constants_SHA_1=['5a827999','6ed9eba1','8f1bbcdc','ca62c1d6']
    __initial_hash_SHA_1=['67452301','efcdab89','98badcfe','10325476','c3d2e1f0']

    __constants_SHA_256=['428a2f98','71374491','b5c0fbcf','e9b5dba5','3956c25b','59f111f1','923f82a4','ab1c5ed5',
                        'd807aa98','12835b01','243185be','550c7dc3','72be5d74','80deb1fe','9bdc06a7','c19bf174',
                        'e49b69c1','efbe4786','0fc19dc6','240ca1cc','2de92c6f','4a7484aa','5cb0a9dc','76f988da',
                        '983e5152','a831c66d','b00327c8','bf597fc7','c6e00bf3','d5a79147','06ca6351','14292967',
                        '27b70a85','2e1b2138','4d2c6dfc','53380d13','650a7354','766a0abb','81c2c92e','92722c85',
                        'a2bfe8a1','a81a664b','c24b8b70','c76c51a3','d192e819','d6990624','f40e3585','106aa070',
                        '19a4c116','1e376c08','2748774c','34b0bcb5','391c0cb3','4ed8aa4a','5b9cca4f','682e6ff3',
                        '748f82ee','78a5636f','84c87814','8cc70208','90befffa','a4506ceb','bef9a3f7','c67178f2']
    __initial_hash_SHA_256=['6a09e667','bb67ae85','3c6ef372','a54ff53a','510e527f','9b05688c','1f83d9ab','5be0cd19']

    # look up table for conversion of Bin -> Hex and Hex -> Bin

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

    # method to check 8-bit 
        
    def __check_for_8_bit(self,binary_string): 
        binary_8_bit_format=binary_string
        if len(binary_8_bit_format)<8: 
            binary_8_bit_format=(binary_8_bit_format[::-1]+''.join(['0' for i in range(8-len(binary_8_bit_format))]))[::-1]
        return binary_8_bit_format

    # method to check 32-bit 
    
    def __check_for_32_bits(self,binary_string): 
        binary_32_bit_format=binary_string
        if len(binary_string)<32: 
            binary_32_bit_format=(binary_32_bit_format[::-1]+''.join(['0' for i in range(0,32-len(binary_32_bit_format))]))[::-1]
        return binary_32_bit_format

    # method to check 64-bit 
    
    def __check_for_64_bits(self,binary_string): 
        binary_64_bit_format=binary_string
        if len(binary_64_bit_format)<64: 
            binary_64_bit_format=(binary_64_bit_format[::-1]+''.join(['0' for i in range(64-len(binary_64_bit_format))]))[::-1]
        return binary_64_bit_format

    # method to check 128-bit 
    
    def __check_for_128_bits(self,binary_string): 
        binary_128_bit_format=binary_string
        if len(binary_128_bit_format)<128: 
            binary_128_bit_format=(binary_128_bit_format[::-1]+''.join(['0' for i in range(128-len(binary_128_bit_format))]))[::-1]
        return binary_128_bit_format
    
    # method to convert decimal to binary

    def __convert_decimal_to_binary(self,number,number_of_bits=32): 
        if number_of_bits==32: 
            return self.__check_for_32_bits(bin(number)[2:])
        else: 
            return self.__check_for_64_bits(bin(number)[2:])

    # method to convert binary to decimal
    
    def __convert_binary_to_decimal(self,binary_string): 
        return int('0b'+binary_string,2)

    # method to convert binary to hex
    
    def __convert_binary_to_hex(self,binary_string): 
        hex_output=''
        for i in range(0,len(binary_string),4): 
            hex_output+=self.__look_up_BinToHex[binary_string[i:i+4]]
        return hex_output
    
    # method to convert hex to binary

    def __convert_hex_to_binary(self,hex_string): 
        binary_output=''
        for i in hex_string: 
            binary_output+=self.__look_up_HexToBin[i]
        return binary_output

    # method for performing the modular addition 2^n

    def __modulo_addition(self,operand_1,operand_2=0,modulo_power=32):   # perform the addition on integer format
        return (operand_1+operand_2)%pow(2,modulo_power)

    # method for performing rotate left shift - circular

    def __rotate_left_shift(self,element,number_of_times,default=32): 
        return (element<<number_of_times)|(element>>(default-number_of_times))

    # method for performing rotate right shift - circular

    def __rotate_right_shift(self,element,number_of_times,default=32): 
        return (element>>number_of_times)|(element<<(default-number_of_times))

    # method for performing right shift - not circular

    def __right_shift_operation(self,element,number_of_times): 
        return element>>number_of_times
    
    # method for converting the message into binary format

    def __message_to_binary_format(self): 
        binary_format=''
        for i in self.message: 
            binary_format+=self.__check_for_8_bit(bin(ord(i))[2:])
        return binary_format

    # method for padding the bits 

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

    # method for appending the remaining bits

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

    # method for spilting into 32 bit/ 64 bit blocks

    def __split_into_blocks(self,binary_string,slice_into=32): 
        result=[]
        for i in range(0,len(binary_string),slice_into): 
            result.append(binary_string[i:i+slice_into])
        return result

    # functions required to perform the operations

    def __functions(self,first_term,second_term,third_term,function_type=None,standard=None):
        if standard=='sha-1':
            if function_type=='ch': 
                return (first_term & second_term) ^ (~first_term & third_term)
            if function_type=='parity': 
                return first_term ^ second_term ^ third_term
            if function_type=='maj': 
                return (first_term & second_term) ^ (first_term & third_term) ^ (second_term & third_term)

    # method for SHA-1
    
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
                    function_output=self.__functions(buffer_b,buffer_c,buffer_d,function_type='ch',standard='sha-1')
                    constant=__constants[0]
                if 20<=k<40: 
                    function_output=self.__functions(buffer_b,buffer_c,buffer_d,function_type='parity',standard='sha-1')
                    constant=__constants[1]
                if 40<=k<60: 
                    function_output=self.__functions(buffer_b,buffer_c,buffer_d,function_type='maj',standard='sha-1')
                    constant=__constants[2]
                if 60<=k<80: 
                    function_output=self.__functions(buffer_b,buffer_c,buffer_d,function_type='parity',standard='sha-1')
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

    # method for SHA-256
            
    def __sha_256(self,message_blocks): 
        hash_output=''
        __constants=self.__constants_SHA_256
        for i in __constants:
            __constants[__constants.index(i)]=int('0b'+self.__convert_hex_to_binary(i),2)   
        buffer_a=int('0b'+self.__convert_hex_to_binary(self.__initial_hash_SHA_256[0]),2)
        buffer_b=int('0b'+self.__convert_hex_to_binary(self.__initial_hash_SHA_256[1]),2)
        buffer_c=int('0b'+self.__convert_hex_to_binary(self.__initial_hash_SHA_256[2]),2)
        buffer_d=int('0b'+self.__convert_hex_to_binary(self.__initial_hash_SHA_256[3]),2)
        buffer_e=int('0b'+self.__convert_hex_to_binary(self.__initial_hash_SHA_256[4]),2)
        buffer_f=int('0b'+self.__convert_hex_to_binary(self.__initial_hash_SHA_256[5]),2)
        buffer_g=int('0b'+self.__convert_hex_to_binary(self.__initial_hash_SHA_256[6]),2)
        buffer_h=int('0b'+self.__convert_hex_to_binary(self.__initial_hash_SHA_256[7]),2)
        hex_constants=[buffer_a,buffer_b,buffer_c,buffer_d,buffer_e,buffer_f,buffer_g,buffer_h]
        function_output=None
        flag=False
        for i in message_blocks: 
            message_32_bit_blocks=self.__split_into_blocks(i)
            if flag==True: 
                buffer_a,buffer_b,buffer_c,buffer_d,buffer_e,buffer_f,buffer_g,buffer_h=hex_constants
            for j in message_32_bit_blocks: 
                message_32_bit_blocks[message_32_bit_blocks.index(j)]=int('0b'+j,2)
            temp=[] 
            for l in range(64):  
                if 0<=l<16: 
                    temp.append(message_32_bit_blocks[l])
                if 16<=l<64:
                    s0=self.__rotate_right_shift(temp[l-15],7) ^ self.__rotate_right_shift(temp[l-15],18) ^ self.__right_shift_operation(temp[l-15],3)
                    s1=self.__rotate_right_shift(temp[l-2],17) ^ self.__rotate_right_shift(temp[l-2],19) ^ self.__right_shift_operation(temp[l-2],10)
                    temp1=self.__modulo_addition(temp[l-16],s0)
                    temp1=self.__modulo_addition(temp[l-7],temp1)
                    temp1=self.__modulo_addition(temp1,s1)
                    temp.append(temp1)
            message_32_bit_blocks=temp
            for k in range(64): 
                s1=self.__rotate_right_shift(buffer_e,6) ^ self.__rotate_right_shift(buffer_e,11) ^ self.__rotate_right_shift(buffer_e,25)
                s0=self.__rotate_right_shift(buffer_a,2) ^ self.__rotate_right_shift(buffer_a,13) ^ self.__rotate_right_shift(buffer_a,22)
                ch=(buffer_e & buffer_f) ^ (~buffer_e & buffer_g)
                maj=(buffer_a & buffer_b) ^ (buffer_c & buffer_a) ^ (buffer_b & buffer_c)
                temp1=self.__modulo_addition(buffer_h,s1)
                temp1=self.__modulo_addition(temp1,ch)
                temp1=self.__modulo_addition(temp1,__constants[k])
                temp1=self.__modulo_addition(temp1,message_32_bit_blocks[k])
                temp2=self.__modulo_addition(s0,maj)
                buffer_h=buffer_g 
                buffer_g=buffer_f
                buffer_f=buffer_e
                buffer_e=self.__modulo_addition(buffer_d,temp1)
                buffer_d=buffer_c
                buffer_c=buffer_b
                buffer_b=buffer_a
                buffer_a=self.__modulo_addition(temp1,temp2)
            buffer_list=[buffer_a,buffer_b,buffer_c,buffer_d,buffer_e,buffer_f,buffer_g,buffer_h]
            for m in range(len(hex_constants)): 
                hex_constants[m]=self.__convert_decimal_to_binary(self.__modulo_addition(hex_constants[m]+buffer_list[m]))
        for n in hex_constants: 
            hash_output+=self.__convert_binary_to_hex(n)
        return hash_output

    # integrating the methods for SHA-1

    def SHA_Standard_160_bits(self): 
        message_in_binary_format=self.__message_to_binary_format()
        message_in_binary_format=self.__append_padding_bits(message_in_binary_format)
        message_in_binary_format=self.__append_length(message_in_binary_format)
        message_possible_blocks=self.__possible_blocks(message_in_binary_format)
        return self.__sha(message_possible_blocks)     

    # integrating the methods for SHA-256

    def SHA_Standard_256_bits(self): 
        message_in_binary_format=self.__message_to_binary_format()
        message_in_binary_format=self.__append_padding_bits(message_in_binary_format)
        message_in_binary_format=self.__append_length(message_in_binary_format)
        message_possible_blocks=self.__possible_blocks(message_in_binary_format)
        return self.__sha_256(message_possible_blocks)
        

obj=SHA('Hello world!!!')
print('output for SHA-1 -> '+obj.SHA_Standard_160_bits())   
print('output for SHA-256 -> '+obj.SHA_Standard_256_bits())

# outputs:-

# output for SHA-1 -> 6555aa9d245f6dc2b57aa13366cc6c6fcccab6ad
# output for SHA-256 -> 4354dfda70c8f0d3991b9de3d56dcb6e9f2fc6c0316d235b63afeb388471ada4