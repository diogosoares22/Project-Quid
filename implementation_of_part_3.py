#imports
import random
import math

#global variables
global MAX
global SUM

MAX=1000

class player:

    #construtor
    def __init__(self,real):
        self.real=real


def generate_list(n):
    random_list=[]
    sum=0
    for i in range(n-1):
        new_v=random.uniform(-MAX,MAX)
        random_list.append(new_v)
        sum+=new_v
    new_v=random.randint(-MAX,MAX)+1-sum%1
    random_list.append(new_v)
    sum+=new_v
    return random_list

def generate_players(n,r_list):
    player_list=[]
    for i in range(n):
        player_list.append(player(r_list[i]))
    return player_list

def integer_bits(mod,n):
    from math import log2,ceil
    return ceil(log2(mod*n))

def fractional_bits(n):
    from math import log2,floor
    return floor(log2(n))+1

def dec_to_bin(number,mod,n):
    integer_part=bin(int(number%mod))[2:]
    integer_part=(integer_bits(mod,n)-len(integer_part))*'0'+integer_part
    fractional_part=conv_frac(number%1,fractional_bits(n))
    return integer_part+fractional_part

def conv_frac(dec_frac,bits):
    bin_frac=''
    dec_frac=(dec_frac//(2**(-bits)))*2**(-bits)
    for i in range(1,bits+1):
        bit=int(dec_frac//2**(-i))
        bin_frac+=str(bit)
        dec_frac=dec_frac-bit*(1/2**i)
    return bin_frac

def binary_sum(bin1,bin2):
    carry=0
    sum=''
    for i in range(len(bin1)-1,-1,-1):
        sum=str((int(bin1[i])+int(bin2[i])+carry)%2)+sum
        carry=(int(bin1[i])+int(bin2[i])+carry)//2
    return sum

def bin_to_dec(b,mod,n):
    exponent=integer_bits(mod,n)-1
    sum=0
    for i in range(len(b)):
        sum+=int(b[i])*(2**exponent)
        exponent-=1
    return sum



if __name__== "__main__":
    #main function
    n=1000
    mod=273
    number_list=generate_list(n)
    right_result=int(sum(number_list)%mod)
    player_list=generate_players(len(number_list),number_list)
    SUM=dec_to_bin(player_list[0].real,mod,n)
    for i in range(1,n):
        SUM=binary_sum(SUM,dec_to_bin(player_list[i].real,mod,n))
    real_sum=bin_to_dec(SUM,mod,n)
    if int(math.ceil(real_sum))%mod==right_result:
        print('SUCCESS')
                 