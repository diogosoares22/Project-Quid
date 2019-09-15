def decimalToBinary(n, a, b) : 
  
    binary = ""  
    Integral = int(n)  
    fractional = n - Integral 
    
    i = 0
    while (Integral and i < a) : 
          
        rem = Integral % 2
        binary += str(rem);  
        Integral //= 2
        i+=1
      
    binary = binary[ : : -1]  
     
    binary += '.'

    while (b) : 
          
        fractional *= 2
        fract_bit = int(fractional)  
  
        if (fract_bit == 1) : 
              
            fractional -= fract_bit  
            binary += '1'
              
        else : 
            binary += '0'
  
        b -= 1
  
    return binary

def parse_dec(n, a, b) : 
  
    binary = ""  
    integral = int(n)  
    fract = n - integral 
    
    i = 0
    while (integral and i < a) : 
          
        rem = integral % 2
        binary += str(rem);  
        integral //= 2
        i+=1
      
    binary = binary[ : : -1]  
     
    binary += '.'

    while (b) : 
          
        fract *= 2
        fract_bit = int(fract)  
  
        if (fract_bit == 1) : 
              
            fract -= fract_bit  
            binary += '1'
              
        else : 
            binary += '0'
  
        b -= 1
  
    return binary  

def parse_bin(s):
    b = s.split('.')
    return int(b[0], 2) + 1

print(parse_dec(10.123, 3, 2))

print(parse_dec(0.876, 3, 2))

print(parse_bin("10.11"))
