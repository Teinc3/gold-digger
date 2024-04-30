class Unwrapper:
    def __init__(self, binary):
        self.binary = binary

    def unwrap(self):
        # Convert binary to string
        binary_str = ''.join(format(byte, '08b') for byte in self.binary)

        # Check if binary_str is 0001011010100000
        if binary_str == '0001011010100000':
            return { "name": "progress_request" }

        # Discard the first bit
        binary_str = binary_str[1:]

        # Read the next 6 bits
        six_bits_str = binary_str[:6]

        # Perform switch case
        if six_bits_str == '001001':
            return {
                "name": "transformation",
                "seed1": binary_str[6:22],
                "seed2": binary_str[22:42]
            }
        elif six_bits_str == '001011':
            return { "name": "playtime" }
        else:
            return (six_bits_str, { "name": "unknown" })

# Example usage
if __name__ == '__main__':
    binary = bytes.fromhex('132096a93c80') # 0001 0010 --> 0 001001 --> 001001
    unwrapper = Unwrapper(binary)
    result = unwrapper.unwrap()
    print(result)