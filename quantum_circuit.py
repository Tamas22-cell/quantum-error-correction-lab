from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator


def build_circuit(error_qubit=None):
    data = QuantumRegister(3, "data")
    ancilla = QuantumRegister(2, "ancilla")
    syndrome = ClassicalRegister(2, "syndrome")
    result = ClassicalRegister(3, "result")

    qc = QuantumCircuit(data, ancilla, syndrome, result)

    # Logical |1> preparation
    qc.x(data[0])

    # Encoding
    qc.cx(data[0], data[1])
    qc.cx(data[0], data[2])

    # Introduce a single bit-flip error
    if error_qubit is not None:
        qc.x(data[error_qubit])

    # Syndrome extraction
    qc.cx(data[0], ancilla[0])
    qc.cx(data[1], ancilla[0])

    qc.cx(data[1], ancilla[1])
    qc.cx(data[2], ancilla[1])

    qc.measure(ancilla, syndrome)

    # Error correction
    with qc.if_test((syndrome, 1)):
        qc.x(data[0])

    with qc.if_test((syndrome, 3)):
        qc.x(data[1])

    with qc.if_test((syndrome, 2)):
        qc.x(data[2])

    qc.measure(data, result)

    return qc


simulator = AerSimulator()

for error in [None, 0, 1, 2]:
    circuit = build_circuit(error)
    job = simulator.run(circuit, shots=100)
    counts = job.result().get_counts()

    print(f"Error on qubit {error}: {counts}")

print("\nQuantum error correction simulation completed.")