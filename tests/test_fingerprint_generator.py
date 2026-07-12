print("FILE LOADED")

from modules.fingerprinting.fingerprint_generator import (
    FingerprintGenerator
)

def main():
    print("TEST STARTED")
    generator = FingerprintGenerator()

    result = generator.generate(r"C:\Users\Bieber\Desktop\radio-monitor\data\chunks\chunk_000001.wav")

    print()
    print("Duration")
    print(result["duration"])

    print()

    print("fingerprint length: ")
    print(len(result["fingerprint"]))



if __name__ == "__main__":
    main()

