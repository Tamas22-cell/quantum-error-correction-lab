
import csv
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, pauli_error

SHOTS = 5000
PROBABILITIES = [i / 100 for i in range(0, 31, 2)]


def make_noise_model(p):
    model = NoiseModel()
    model.add_all_qubit_quantum_error(
        pauli_error([("X", p), ("I", 1 - p)]),
        ["id"]
    )
    return model


def make_circuit(encoded):
    n = 3 if encoded else 1
    qc = QuantumCircuit(n, n)

    # Prepare logical |1>
    qc.x(0)

    if encoded:
        qc.cx(0, 1)
        qc.cx(0, 2)

    # Independent bit-flip noise on data qubits
    for q in range(n):
        qc.id(q)

    qc.measure(range(n), range(n))
    return qc


def failure_rate(counts, encoded):
    failures = 0

    for state, count in counts.items():
        if encoded:
            failed = state.count("1") < 2
        else:
            failed = state == "0"

        if failed:
            failures += count

    return failures / SHOTS


def simulate(p, encoded, seed):
    simulator = AerSimulator(
        noise_model=make_noise_model(p)
    )

    circuit = make_circuit(encoded)

    result = simulator.run(
        circuit,
        shots=SHOTS,
        seed_simulator=seed
    ).result()

    return failure_rate(result.get_counts(), encoded)


def main():
    physical = []
    corrected = []
    theory = []

    print("\nQUANTUM ERROR CORRECTION BENCHMARK")
    print("-" * 60)
    print("Noise | Physical error | Encoded error | Theory")

    for i, p in enumerate(PROBABILITIES):
        raw = simulate(p, False, 1000 + i)
        encoded = simulate(p, True, 2000 + i)
        expected = 3 * p**2 - 2 * p**3

        physical.append(raw)
        corrected.append(encoded)
        theory.append(expected)

        print(
            f"{p:5.0%} | "
            f"{raw:13.2%} | "
            f"{encoded:13.2%} | "
            f"{expected:7.2%}"
        )

    with open(
        "benchmark_results.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow([
            "noise_probability",
            "physical_error",
            "encoded_error",
            "theoretical_error"
        ])

        for i, p in enumerate(PROBABILITIES):
            writer.writerow([
                p,
                physical[i],
                corrected[i],
                theory[i]
            ])

    plt.figure(figsize=(10, 6))

    plt.plot(
        PROBABILITIES,
        physical,
        "r--o",
        label="Physical qubit"
    )

    plt.plot(
        PROBABILITIES,
        corrected,
        "b-o",
        label="3-qubit repetition code"
    )

    plt.plot(
        PROBABILITIES,
        theory,
        "g:",
        label="Theoretical logical error"
    )

    plt.xlabel("Physical bit-flip probability")
    plt.ylabel("Failure probability")
    plt.title("Quantum Error Correction Benchmark")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        "quantum_benchmark.png",
        dpi=200
    )

    print("\nSaved: quantum_benchmark.png")
    print("Saved: benchmark_results.csv")

    plt.show()


if __name__ == "__main__":
    main()
