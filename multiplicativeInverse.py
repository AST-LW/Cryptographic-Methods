# multiplicative inverse calculation is very important in cryptographic methods
# the below, calculates the inverse in given mod value at faster rate using extended euclidean method

def multiplicativeInverse(number,modulo): 
    quotient,remainder=None,None
    dividend=modulo
    divisor=number
    t1,t2,t=0,1,None  # constants to defined initially
    while divisor!=0: 
        quotient=dividend//divisor
        remainder=dividend%divisor 
        t=t1-quotient*t2
        t1=t2
        t2=t
        dividend=divisor
        divisor=remainder
    return t1+modulo if t1<0 else t1

print('the inverse of {0} mod {1} is '.format(3,392)+str(multiplicativeInverse(27,392)))
 
# output:- 

# the inverse of 3 mod 392 is 363