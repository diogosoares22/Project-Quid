import cirq
import random
import math
import sys
import getopt
import numpy as np

def generate_reals():
    reals = []
    total = 0
    for i in range(n - 1):
        appended = random.uniform(-2**(k + 1) + 1, 2**(k + 1) - 1)
        reals.append(appended)
        total += appended
    total %= 1
    reals.append(1 - total + random.randint(-2**(k + 1) + 1, 2**(k + 1) - 2))
    return reals
    
def entanglement(mediumqubits, destqubits):
    circuit = cirq.Circuit()

    for j in range(k):
        circuit.append(cirq.H(mediumqubits[j]))
        circuit.append(cirq.CNOT(mediumqubits[j], destqubits[j]))

    return circuit

def addnum(targetqubits, real):
    circuit = cirq.Circuit()

    for i in range(k):
        circuit.append(cirq.Y(targetqubits[i])**(real / 2**(i)))

    return circuit

def printcursumqubits(systemstate):
    zeroind = 0

    for l in range(k):
        oneind = 2 ** (3 * k - 1 - l)
        zeronorm = 0
        onenorm = 0
        for a in range(2**l):
            for b in range(2**(k - 1 - l)):
                shift = 2 ** (3 * k - l) * a + 2 ** (2 * k) * b
                zerocoef = systemstate[zeroind + shift]
                onecoef = systemstate[oneind + shift]
                zeronorm += zerocoef.real ** 2 + zerocoef.imag ** 2
                onenorm += onecoef.real ** 2 + onecoef.imag ** 2
        norm = zeronorm + onenorm
        normrt = math.sqrt(norm)

        print("2^{} sum 0: {}".format(l, zeronorm / norm))
        print("2^{} sum 1: {}".format(l, onenorm / norm))

if __name__ == "__main__":
    global n, k, showstate, showcommunication
    if len(sys.argv) > 1:
        try:
            ops, otherargs = getopt.getopt(sys.argv[1:], 'sc')
        except Exception as e:
            print("Invalid option.")
            print(e.msg)
            exit(0)
        showstate = False
        showcommunication = False
        for op in ops:
            if op[0] == '-s':
                showstate = True
            if op[0] == '-c':
                showcommunication = True
        if len(otherargs) != 2:
            print("Need two non-option arguments. Got {} (that is {} argument{}).".format(otherargs, len(otherargs), "" if len(otherargs) == 1 else "s"))
            exit(0)
        try:
            n = int(otherargs[0])
        except Exception as e:
            print("{} is not a valid integer.".format(otherargs[0]))
            exit(0)
        try:
            k = int(otherargs[1])
        except Exception as e:
            print("{} is not a valid integer.".format(otherargs[0]))
            exit(0)
        if (n < 2):
            print("n = {} < 2 is invalid.".format(n))
            exit(0)
        if (k < 1):
            print("k = {} < 1 is invalid.".format(k))
            exit(0)
    else:
        n = 2
        k = 3
        showstate = False
        showcommunication = False
    modulo = 2**k
    if k == 1:
        print("The game for {} players.".format(n))
    else:
        print("The game for {} players telling mod {}.".format(n, modulo))
    reals = generate_reals()
    print("The players will get {}.".format(reals))
    sumreals = int(sum(reals))
    if k == 1:
        print("The sum is {}.".format(sumreals))
    else:
        print("The sum is {} ({} mod {}).".format(sumreals, sumreals % modulo, modulo))
    print("Starting the game...\n")

    firstk = [cirq.GridQubit(j, 0) for j in range(k)]
    secondk = [cirq.GridQubit(j, 0) for j in range(k, 2*k)]
    thirdk = [cirq.GridQubit(j, 0) for j in range(2*k, 3*k)]
    firstthreek = [cirq.GridQubit(j, 0) for j in range(3 * k)]
    systemstate = np.zeros((2**(3*k),), dtype=np.complex64)
    systemstate[0] = 1
    if showstate:
        print("state to zero")
        printcursumqubits(systemstate)
        print()
    for i in range(n - 1):
        res = cirq.Simulator().simulate(entanglement(secondk, thirdk), qubit_order=firstthreek, initial_state=systemstate)
        systemstate = res.final_state
        print("Prepared entangled qubits for P{} -> P{}.\n".format(i, i + 1))
        res = cirq.Simulator().simulate(addnum(firstk, reals[i]), qubit_order=firstthreek, initial_state=systemstate)
        systemstate = res.final_state 
        print("Added {} by player {}.".format(reals[i], i))
        if showstate:
            printcursumqubits(systemstate)
        print()
        telcirc = cirq.Circuit()
        for j in range(k):
            telcirc.append(cirq.CNOT(cirq.GridQubit(k + j, 0), cirq.GridQubit(j, 0)))
            telcirc.append(cirq.H(cirq.GridQubit(k + j, 0)))
            telcirc.append(cirq.measure(cirq.GridQubit(j, 0), key = '{}-0'.format(j)))
            telcirc.append(cirq.measure(cirq.GridQubit(k + j, 0), key = '{}-1'.format(j)))
        res = cirq.Simulator().simulate(telcirc, qubit_order = firstthreek, initial_state=systemstate)
        systemstate = res.final_state
    
        doz = []
        dox = []
        for j in range(k):
            doz.append(res.measurements['{}-1'.format(j)][0])
            dox.append(res.measurements['{}-0'.format(j)][0])
    
        if showcommunication:
            print("P{} -> P{}".format(i, i + 1))
            for j in range(k):
                print("({}, {})".format(int(dox[j]), int(doz[j])), end = '')
            print('\n')

        rcivcirc = cirq.Circuit()
        for j in range(k):
            if doz[j]:
                rcivcirc.append(cirq.Z(cirq.GridQubit(2 * k + j, 0)))
            if dox[j]:
                rcivcirc.append(cirq.X(cirq.GridQubit(2 * k + j, 0)))
        res = cirq.Simulator().simulate(rcivcirc, qubit_order = firstthreek, initial_state=systemstate)
        systemstate = res.final_state

        measuredmask = 0
        for j in range(k):
            if dox[j]:
                measuredmask += 2**(2 * k - 1 - j)
            if doz[j]:
                measuredmask += 2**(k - 1 - j)

        nsysstate = np.zeros((2**(3*k),), dtype=np.complex64)
        for l in range(2**k):
            nsysstate[2**(2*k)*l] = systemstate[2**k*measuredmask + l]

        systemstate = nsysstate

        print("Qubit{} teleported to player {}.\n".format("" if k == 1 else "s", i + 1))

    res = cirq.Simulator().simulate(addnum(firstk, reals[n - 1]), qubit_order=firstthreek, initial_state=systemstate)
    systemstate = res.final_state

    print("Added {} by player {}.".format(reals[n - 1], n - 1))
    if showstate:
        printcursumqubits(systemstate)
    print()

    mescircuit = cirq.Circuit()
    for i in range(k):
        controlqubit = cirq.GridQubit(i, 0)
        for j in range(i + 1, k):
            targetqubit = cirq.GridQubit(j, 0)
            mescircuit.append((cirq.Y(targetqubit)**(-2**(i - j))).controlled_by(controlqubit))
    mescircuit.append(cirq.measure(*[cirq.GridQubit(i, 0) for i in range(k)], key = 'f'))
    res = cirq.Simulator().simulate(mescircuit, qubit_order=firstthreek, initial_state=systemstate)
    if k == 1:
        odd = res.measurements['f'][0]
        if odd:
            print("Measured 1. The sum is ODD.")
        else:
            print("Measured 0. The sum is EVEN.")
    else:
        result = 0
        binar = ""
        for i in range(k):
            binar += "1" if res.measurements['f'][k - 1 - i] else "0"
            if res.measurements['f'][i]:
                result += 2**i
        print("Measured {}. The sum is {} mod {}.".format(binar, result, modulo))
