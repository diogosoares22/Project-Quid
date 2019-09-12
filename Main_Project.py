import cirq
import random

def game(list_real):
    
    n=len(list_real)
    numr_bits=bits_transform(n)
    numr_qubits=2*n-1

    qubits = [cirq.GridQubit(i, 0) for i in range(numr_qubits)]
    circuit = cirq.Circuit()

    for k in range(n-1):
        i=2*k
        #Bell state
        circuit.append(cirq.H(qubits[i+1]))
        circuit.append(cirq.CNOT(qubits[i+1],qubits[i+2]))

        #Rotation with the real value
        player_nmr=list_real[k]

        circuit.append(cirq.Y(qubits[i])**player_nmr)

        circuit.append(cirq.CNOT(qubits[i],qubits[i+1]))
        circuit.append(cirq.H(qubits[i]))


        circuit.append(cirq.CZ(qubits[i],qubits[i+2]))
        circuit.append(cirq.CNOT(qubits[i+1],qubits[i+2]))

    circuit.append(cirq.Y(qubits[-1])**list_real[k+1])
    circuit.append(cirq.measure(qubits[-1],key='final'))

    # Simulate the circuit several times.
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1)

    return result.measurements['final'][0][0]

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

def generate_reals(length):
    reals = []
    total = 0
    for i in range(length - 1):
        appended = random.uniform(-3, 3)
        reals.append(appended)
        total += appended
    total %= 1
    reals.append(1 - total + random.randint(-3, 2))
    return reals
    
n=7

if __name__ == "__main__":
    print("Playing the game with {} players.".format(n))
    reals = generate_reals(n)
    i=0
    for i in range(len(reals)):
        reals[i]=round(reals[i])
    print(reals)
    print("The sum is {}.".format(sum(reals)))
    boolean=game(reals)
    if boolean:
        print("The result is odd")
    else:
        print("The result is even")
    