"""Three-qubit bit-flip code: exact classical probability benchmark.

The logical state is |0_L> = |000> or |1_L> = |111>.
Independent bit flips are corrected by majority voting.
"""
import argparse


def logical_error_uncoded(p: float) -> float:
    if not 0 <= p <= 1:
        raise ValueError('p must be between 0 and 1')
    return p


def logical_error_encoded(p: float) -> float:
    if not 0 <= p <= 1:
        raise ValueError('p must be between 0 and 1')
    return 3 * p * p * (1 - p) + p ** 3


def main() -> None:
    parser = argparse.ArgumentParser(description='3-qubit bit-flip error correction benchmark')
    parser.add_argument('--p', type=float, default=0.1, help='Independent physical bit-flip probability')
    args = parser.parse_args()
    raw = logical_error_uncoded(args.p)
    coded = logical_error_encoded(args.p)
    print(f'Physical bit-flip probability: {args.p:.2%}')
    print(f'Unencoded logical error:       {raw:.2%}')
    print(f'Encoded logical error:         {coded:.2%}')
    print(f'Absolute improvement:         {raw-coded:.2%}')
    print('Model: independent X errors; ideal encoding, syndrome and correction.')


if __name__ == '__main__':
    main()
