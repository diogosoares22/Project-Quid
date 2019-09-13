import cirq
import math

def QFT(qubits):
    circuit=cirq.Circuit()
    for j in range(len(qubits)):
        for k in range(j):
            circuit.append(cirq.CZ(qubits[j], qubits[k])**(1/float(2**(j-k))))
        circuit.append(cirq.H(qubits[j]))
    l = len(qubits)
    for j in range(len(qubits)//2):
        circuit.append(cirq.SWAP(qubits[j], qubits[l - 1 - j]))
    return circuit

def sumup(qft_qubits,normal_qubits):
    #normal_qubits are from n to 1
    #qft_qubits are from 1 to n
    circuit=cirq.Circuit()
    n=len(qft_qubits)
    circuit.append(cirq.X(b[0]))
    circuit.append(cirq.X(b[2]))

    for i in range(1,n+1):
        for k in range(i):
            circuit.append(cirq.CZ(normal_qubits[k], qft_qubits[i-1])**(1/(2**float(i-k-1))))
    return circuit

def iQFT(qubits):
    circuit=cirq.Circuit()
    circuit.append(cirq.inverse(QFT(qubits)))
    return circuit
n=3
qubits = [cirq.GridQubit(i, 0) for i in range(n)]
b = [cirq.GridQubit(i+n, 0) for i in range(n)]

circuit=cirq.Circuit()
circuit.append(cirq.X(qubits[0]))
circuit.append(cirq.X(qubits[2]))
circuit.append(QFT(qubits))
circuit.append(sumup(qubits,b))
circuit.append(iQFT(qubits))
#circuit.append(cirq.measure(*qubits,key='m'))
print(circuit)
simulator = cirq.Simulator()
fullprob = True
if fullprob:
    state = simulator.simulate(circuit).final_state
    #print(state)
    for i in range(n):
        zeroprob = 0
        oneprob = 0
        for a in range(2**(i)):
            for b in range(2**(2 * n - 1 - i)):
                zerocoef = state[a * 2**(2 * n - i) + b]
                onecoef = state[a * 2**(2 * n - i) + 2**(2 * n - 1 - i) + b]
                zeroprob += zerocoef.real**2 + zerocoef.imag**2
                oneprob += onecoef.real**2 + onecoef.imag**2
        print("{}: {} (0), {} (1)".format(i, zeroprob, oneprob))
else:
    result = simulator.run(circuit, repetitions=20)
    print(result.measurements['m'])
