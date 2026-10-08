import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, pauli_error


SHOTS = 2000


def build_noise_model(p):
    noise_model = NoiseModel()

    error = pauli_error([
        ("X", p),
        ("I", 1 - p)
    ])

    noise_model.add_all_qubit_quantum_error(
        error,
        ["id"]
    )

    return noise_model


def create_circuit():
    qc = QuantumCircuit(3, 3)

    # Logical |1> state
    qc.x(0)
    qc.cx(0, 1)
    qc.cx(0, 2)

    # Apply independent noise to each data qubit
    for qubit in range(3):
        qc.id(qubit)

    # Majority-vote decoding for computational-basis states
    qc.measure([0, 1, 2], [0, 1, 2])

    return qc


def run_simulation(p):
    simulator = AerSimulator(
        noise_model=build_noise_model(p)
    )

    circuit = create_circuit()

    result = simulator.run(
        circuit,
        shots=SHOTS
    ).result()

    counts = result.get_counts()

    # A majority of zero bits means logical failure
    failures = 0

    for state, count in counts.items():
        if state.count("1") < 2:
            failures += count

    return failures / SHOTS


def main():
    probabilities = np.linspace(0, 0.5, 11)

    physical_errors = []
    simulated_errors = []
    theoretical_errors = []

    print("\nQUANTUM ERROR CORRECTION - NOISE SIMULATION")
    print("-" * 55)

    for p in probabilities:
        simulated = run_simulation(p)

        # Three-qubit repetition-code logical error probability
        theoretical = 3 * p**2 - 2 * p**3

        physical_errors.append(p)
        simulated_errors.append(simulated)
        theoretical_errors.append(theoretical)

        print(
            f"Noise: {p:.2f} | "
            f"Physical: {p:.4f} | "
            f"Logical: {simulated:.4f} | "
            f"Theory: {theoretical:.4f}"
        )

    plt.figure(figsize=(10, 6))

    plt.plot(
        probabilities,
        physical_errors,
        "r--",
        label="Physical Qubit Error"
    )

    plt.plot(
        probabilities,
        simulated_errors,
        "bo-",
        label="Simulated Logical Error"
    )

    plt.plot(
        probabilities,
        theoretical_errors,
        "g-",
        label="Theoretical Logical Error"
    )

    plt.xlabel("Physical Bit-Flip Probability")
    plt.ylabel("Logical Error Probability")
    plt.title("Quantum Error Correction - 3 Qubit Repetition Code")

    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig("quantum_error_correction_results.png", dpi=200)
    plt.show()

    print("\nGraph saved: quantum_error_correction_results.png")


if __name__ == "__main__":
    main()