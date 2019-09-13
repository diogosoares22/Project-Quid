import cirq
import math

def QFT(qubits):
    circuit=cirq.Circuit()
    for j in range(len(qubits)):
        for k in range(j):
            circuit.append(cirq.CZ(qubits[j], qubits[k])**(math.pi/float(2**(j-k))))
        circuit.append(cirq.H(qubits[j]))
    return circuit

def sum(qft_qubits,normal_qubits):
    #normal_qubits are from n to 1
    #qft_qubits are from 1 to n
    circuit=cirq.Circuit()
    n=len(qft_qubits)
    #circuit.append(cirq.X(b[0]))
    #circuit.append(cirq.X(b[2]))

    for i in range(1,n+1):
        for k in range(i):
            circuit.append(cirq.CZ(normal_qubits[k], qft_qubits[i-1])**(math.pi/(2**(i-k))))
    return circuit

def iQFT(qubits):
    circuit=cirq.Circuit()
    circuit.append(cirq.inverse(QFT(qubits)))
    return circuit
n=3
qubits = [cirq.GridQubit(i, 0) for i in range(n)]
b = [cirq.GridQubit(i+n, 0) for i in range(n)]

circuit=cirq.Circuit()
circuit.append(QFT(qubits))
circuit.append(sum(qubits,b))
circuit.append(iQFT(qubits))
circuit.append(cirq.measure(*qubits,key='m'))
print(circuit)
simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=20)
print(result.measurements['m'])
