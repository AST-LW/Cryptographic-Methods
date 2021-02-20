# euclid algorithm is used to calculate the gcd of two numbers at faster rate
# we can tell whether two numbers are relative/co-primes or not using euclid algorithm
# for relative primes, gcd of the two numbers is 1

def euclidAlogorithm(a,b): 
    if b==0: 
        return a
    remainder=a%b
    return euclidAlogorithm(b,remainder)

print('the GCD is '+str(euclidAlogorithm(1234567891011121314151617181920212223242526272829,1221)))

# output:-

# for a=1234567891011121314151617181920212223242526272829, b=1221
# the GCD is 3