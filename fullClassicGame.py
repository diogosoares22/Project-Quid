import cirq
import random
import math

systemstate = 0

measuredstates = []

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
    
def prepare_entangled(numplay):
    global systemstate
    circuit = cirq.Circuit()

    for i in range(numplay - 1):
        circuit.append(cirq.H(cirq.GridQubit(2 * i + 1, 0)))
        circuit.append(cirq.CNOT(cirq.GridQubit(2 * i + 1, 0), cirq.GridQubit(2 * i + 2, 0)))

    res = cirq.Simulator().simulate(circuit, qubit_order = qubs)
    systemstate = res.final_state

def addnum(player, real):
    global systemstate
    circuit = cirq.Circuit()
    circuit.append(cirq.Y(cirq.GridQubit(2 * player, 0))**real)
    res = cirq.Simulator().simulate(circuit, qubit_order = qubs, initial_state=systemstate)
    systemstate = res.final_state

def sendfrom(player):
    global systemstate
    global measuredstates
    circuit = cirq.Circuit()
    circuit.append(cirq.CNOT(cirq.GridQubit(2 * player + 1, 0), cirq.GridQubit(2 * player, 0)))
    circuit.append(cirq.H(cirq.GridQubit(2 * player + 1, 0)))
    circuit.append(cirq.measure(cirq.GridQubit(2 * player, 0), key = '{}-0'.format(player)))
    circuit.append(cirq.measure(cirq.GridQubit(2 * player + 1, 0), key = '{}-1'.format(player)))
    res = cirq.Simulator().simulate(circuit, qubit_order = qubs, initial_state=systemstate)
    systemstate=res.final_state
    
    doz = res.measurements['{}-1'.format(player)][0]
    dox = res.measurements['{}-0'.format(player)][0]
    measuredstates.append(dox)
    measuredstates.append(doz)

    circuit2 = cirq.Circuit()
    if doz:
        circuit2.append(cirq.Z(cirq.GridQubit(2 * player + 2, 0)))
    if dox:
        circuit2.append(cirq.X(cirq.GridQubit(2 * player + 2, 0)))
    nres = cirq.Simulator().simulate(circuit2, qubit_order = qubs, initial_state=systemstate)
    systemstate=nres.final_state

def printcursumqubit(i):
    factor = math.sqrt(2**(n - 1 - i))
    zeroind = 0
    for j in range(2 * i):
        if measuredstates[j]:
            zeroind += 2 ** (2 * n - 2 - j)
    oneind = zeroind + 2 ** (2 * n - 2 - 2 * i)

    zerocoef = systemstate[zeroind]
    onecoef = systemstate[oneind]

    print("sum 0: {} (prob. {})".format(zerocoef * factor, factor * factor * (zerocoef.real ** 2 + zerocoef.imag ** 2)))
    print("sum 1: {} (prob. {})".format(onecoef * factor, factor * factor * (onecoef.real ** 2 + onecoef.imag ** 2)))

n = 11
showstate = False
qubs = [cirq.GridQubit(i, 0) for i in range(2 * n - 1)]

if __name__ == "__main__":
    print("The game for {} players.".format(n))
    reals = generate_reals(n)
    print("The players will get {}.".format(reals))
    print("The sum is {}.".format(sum(reals)))
    print("Starting the game...\n")

    prepare_entangled(n)
    print("Prepared entangled state.")
    if showstate:
        printcursumqubit(0)
    print()
    
    for i in range(n - 1):
        addnum(i, reals[i])
        print("Added {} by player {}.".format(reals[i], i))
        if showstate:
            printcursumqubit(i)
        print()
        sendfrom(i)
        print("Qubit teleported to player {}.\n".format(i + 1))

    addnum(n - 1, reals[n - 1])
    print("Added {} by player {}.".format(reals[n - 1], n - 1))
    if showstate:
        printcursumqubit(n - 1)
    print()

    mescircuit = cirq.Circuit()
    mescircuit.append(cirq.measure(cirq.GridQubit(2 * n - 2, 0), key = 'f'))
    res = cirq.Simulator().simulate(mescircuit, qubit_order=qubs, initial_state=systemstate)
    odd = res.measurements['f'][0]
    if odd:
        print("Measured 1. The sum is ODD.")
    else:
        print("Measured 0. The sum is EVEN.")
