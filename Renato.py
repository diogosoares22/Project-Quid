import cirq

def game(list_real):
    n=len(list_real)
    numr_bits=bits_transform(n)
    numr_qubits=2*n-1
    
    return value

def bits_transform(n):
    real=1/n
    i=2
    while (2**-i>=real):
        i=i+1
    return i+1

def round_base(real_n,numr_bits):
    real_n=real_n%2
    aux=real_n%(2**-(numr_bits-1))
    return real_n-aux

def bits_to_basis(bitstring):
    if bitstring=='00':
        return 'I'
    elif bitstring=='01':
        return 'X'
    elif bitstring=='10':
        return 'Z'
    elif bitstring=='11':
        return 'XZ'