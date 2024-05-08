import subprocess;
import random;
import time;

combination_count = 100

def generator() -> int:
    # Generates a tuple of seed1 and seed2
    # seed1: [0, 2**16), seed2: [0, 2**20)

    seed1 = random.randint(0, 2**16 - 1)
    seed2 = random.randint(0, 2**20 - 1)
    return (seed1, seed2)

def main() -> None:
    # Randomizes the seed
    random.seed(time.time())

    # Generates seed pairs
    seed_pairs = [generator() for _ in range(combination_count)]
    print(f"Running {combination_count} seed combinations")

    for filename in ["security", "old_security"]:

        # Clocks the time taken for security.exe to calculate all 50 seeds
        checksum = 0
        start = time.time()
        for seed_pair in seed_pairs:
            result = subprocess.run([f"./bin/{filename}.exe", str(seed_pair[0]), str(seed_pair[1])], capture_output=True, text=True)
            output = int(result.stdout.strip())
            checksum += output
        end = time.time()

        print(f"{filename} time taken: {end - start} seconds with checksum {checksum}")

if __name__ == "__main__":
    main()