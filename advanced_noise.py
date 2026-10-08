from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError

SHOTS = 1000


def build_circuit():
    data = QuantumRegister(3, "data")
    anc = QuantumRegister(2, "anc")
    syndrome = ClassicalRegister(2, "syndrome")
    result = ClassicalRegister(3, "result")

    qc = QuantumCircuit(data, anc, syndrome, result)

    # Prepare logical |1>
    qc.x(data[0])
    qc.cx(data[0], data[1])
    qc.cx(data[0], data[2])

    # Introduce an error on qubit 1
    qc.x(data[1])

    # Syndrome extraction
    qc.cx(data[0], anc[0])
    qc.cx(data[1], anc[0])
    qc.cx(data[1], anc[1])
    qc.cx(data[2], anc[1])

    qc.measure(anc, syndrome)

    # Conditional correction
    with qc.if_test((syndrome, 1)):
        qc.x(data[0])

    with qc.if_test((syndrome, 3)):
        qc.x(data[1])

    with qc.if_test((syndrome, 2)):
        qc.x(data[2])

    qc.measure(data, result)
    return qc


def build_noise_model(p):
    noise = NoiseModel()

    noise.add_all_qubit_quantum_error(
        depolarizing_error(p, 1), ["x"]
    )

    noise.add_all_qubit_quantum_error(
        depolarizing_error(p, 2), ["cx"]
    )

    noise.add_all_qubit_readout_error(
        ReadoutError([[1 - p, p], [p, 1 - p]])
    )

    return noise


def main():
    circuit = build_circuit()

    print("ADVANCED QUANTUM NOISE SIMULATION")
    print("-" * 45)

    for p in [0.0, 0.01, 0.03, 0.05, 0.10]:
        simulator = AerSimulator(
            noise_model=build_noise_model(p)
        )

        result = simulator.run(
            circuit,
            shots=SHOTS
        ).result()

        counts = result.get_counts()

        successes = sum(
            count
            for state, count in counts.items()
            if state.split()[0] == "111"
        )

        print(
            f"Noise: {p:.2f} | "
            f"Success: {successes / SHOTS:.2%}"
        )

    print("\nAdvanced noise simulation completed.")


if __name__ == "__main__":
    main()