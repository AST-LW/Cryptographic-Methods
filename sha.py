# still onGoing...

class SHA():

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
    
    def __check_for_32_bits(self,binary_string): 
        binary_32_bit_format=binary_string
        if len(binary_string)<32: 
            binary_32_bit_format=(binary_32_bit_format[::-1]+''.join(['0' for i in range(0,32-len(binarybinary_32_bit_format))]))[::-1]
        return binary_32_bit_format
    
    def __check_for_64_bits(self,binary_string): 
        binary_64_bit_format=binary_string
        if len(binary_64_bit_format)<64: 
            binary_64_bit_format=(binary_64_bit_format[::-1]+''.join(['0' for i in range(64-len(binary_64_bit_format))]))[::-1]
        return binary_64_bit_format
    
    def __convert_decimal_to_binary(self,number,number_of_bits=32): 
        if number_of_bits==32: 
            return self.__check_for_32_bits(bin(number)[2:])
        else: 
            return self.__check_for_64_bits(bin(number)[2:])
    
    def __convert_binary_to_decimal(self,binary_string): 
        return int('0b'+binary_string,2)
    
    def __convert_binary_to_hex(self,binary_string): 
        hex_output=''
        for i in range(0,len(binary_string,4)): 
            hex_output+=self.__look_up_BinToHex[binary_string[i:i+4]]
        return hex_output
    
    def __convert_hex_to_binary(self,hex_string): 
        binary_output=''
        for i in range(0,len(hex_string)): 
            binary_output+=self.__look_up_HexToBin[hex_string[i:i+4]]
        return binary_output

    def __modulo_addition(self,operand_1,operand_2,modulo_power=32):   # perform the addition on integer format
        return (operand_1+operand_2)%pow(2,modulo_power)

    


    def hash(self,type_of_hash=None): 
