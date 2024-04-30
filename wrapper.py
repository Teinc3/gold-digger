#import time
import subprocess
import platform

class Wrapper:
    def __init__(self):
        pass
    
    def get_response(self, result, token):
        name = result["name"]
        if name == "progress_request":
            return 0 #requires state
        elif name == "transformation":
            return [Wrapper.get_security_code(result["seed1"], result["seed2"]), Wrapper.login(token)]
        elif name == "playtime":
            # We logged in!
            return True
        else:
            return False

    @staticmethod
    def get_security_code(seed1, seed2):
        path = "./security/bin/security" + ".exe" if platform.system() == "Windows" else ""
        #s = time.time()
        result = subprocess.run([path, str(int(seed1, 2)), str(int(seed2, 2))], capture_output=True, text=True)
        code = int(result.stdout)
        #print("Time taken: ", round((time.time() - s) * 1000, 2), " ms")
        binary_str = "0001110" + str(bin(code)[2:]).zfill(16) + "0"
        return bytes.fromhex(hex(int(binary_str, 2))[2:])

    @staticmethod
    def socket_init():
        return bytes.fromhex("1a20680006")
    
    @staticmethod
    def login(token):
        return bytes.fromhex(token)
    
    @staticmethod
    def spoof_progress():
        return bytes.fromhex("27fff0")
    
if __name__ == "__main__":

    wrapper = Wrapper()
    result = {
        "name": "transformation",
        "seed1": "010111000101010",
        "seed2": "11110001101001011111"
    }
    response = Wrapper.get_security_code(result["seed1"], result["seed2"])
    print(int.from_bytes(response))