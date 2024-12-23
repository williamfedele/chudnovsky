import decimal
import math
import sys
from time import time, sleep

# Number of decimals to reach.
# Progress is shown in console if MAX_DECIMALS fits in one terminal row.
MAX_DECIMALS = 200

# Decimal precision
decimal.getcontext().prec = 1000

# Constants
C1 = decimal.Decimal(545140134)
C2 = decimal.Decimal(13591409)
C3 = decimal.Decimal(640320)


# Function to compute the k-th term of the Chudnovsky series
def chudnovsky_term(k):
    # Calculate the factorials
    fac6k = decimal.Decimal(math.factorial(6 * k))
    fac3k = decimal.Decimal(math.factorial(3 * k))
    fac1k = decimal.Decimal(math.factorial(1 * k))

    # Numerator and denominator for the k-th term
    numerator = fac6k * (C1 * k + C2)
    denominator = fac3k * fac1k**3 * C3 ** (3 * k + decimal.Decimal(3) / 2)

    # Return the k-th term with the alternating sign (-1)^k
    return decimal.Decimal((-1) ** k) * (numerator / denominator)


# Function to compute pi using the Chudnovsky series
def chudnovsky(num_terms):
    series_sum = decimal.Decimal(0)
    for k in range(num_terms):
        series_sum += chudnovsky_term(k)
    # Multiply by 12 to get 1/pi
    return decimal.Decimal(1) / (decimal.Decimal(12) * series_sum)


# Function to compute pi using the Chudnovsky series optimized with binary splitting.
def chudnovsky_optimized(num_terms):
    # TODO
    pass


def find_diff_index(n1, n2):
    for i, (d1, d2) in enumerate(zip(str(n1), str(n2))):
        if d1 != d2:
            return i

    return 0


if __name__ == "__main__":
    prev = decimal.Decimal(0)
    start_time = time()

    for num_terms in range(1, 50):
        result = chudnovsky(num_terms)
        diff_idx = find_diff_index(prev, result)

        if diff_idx > MAX_DECIMALS:
            end_time = time()
            print(f"\033[92m{str(prev)[:MAX_DECIMALS]}")
            print(
                f"\033[96mTook {end_time - start_time:.2f}s and {num_terms} terms to reach {diff_idx} decimals of Pi."
            )
            break

        sys.stdout.write(f"\033[92m{str(prev)[0:diff_idx]}")
        sys.stdout.write(f"\033[91m{str(result)[diff_idx:MAX_DECIMALS]}\r")
        sys.stdout.flush()

        prev = result
