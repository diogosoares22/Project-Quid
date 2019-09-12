import cirq


qubits = [cirq.GridQubit(i, 0) for i in range(3)]

# Create a circuit
circuit = cirq.Circuit()

#Entangle
circuit.append(cirq.H(qubits[1]))
circuit.append(cirq.CNOT(qubits[1],qubits[2]))

#Rotation with the real value
circuit.append(cirq.X(qubits[0]))

#
circuit.append(cirq.CNOT(qubits[0],qubits[1]))
circuit.append(cirq.H(qubits[0]))

#Measurement
#circuit.append(cirq.measure(*qubits[:-1], key='m'))


circuit.append(cirq.CZ(qubits[0],qubits[2]))
circuit.append(cirq.CNOT(qubits[1],qubits[2]))


circuit.append(cirq.measure(qubits[2], key='m'))



print("Circuit:")
print(circuit)

# Simulate the circuit several times.
simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=20)
print("Results:")
print(result)