from crypto_signature import CryptoSignatureGenerator
import time


def main():
    print("=== Генератор криптографических подписей ===\n")
    generator = CryptoSignatureGenerator()
    print(f"Timestamp: {generator.timestamp}")
    print(f"Начальный counter: {generator.counter}\n")
    print("Генерация подписей:")
    for i in range(10):
        signature = generator.generate_signature()
        print(f"Подпись {i+1}: {signature} (counter: {generator.counter})")
    print("\n" + "="*50)
    print("\nГенерация с заданным timestamp:")
    custom_timestamp = 1234567890
    generator2 = CryptoSignatureGenerator(custom_timestamp)
    print(f"Timestamp: {generator2.timestamp}")
    signatures = [generator2.generate_signature() for _ in range(5)]
    for i, sig in enumerate(signatures, 1):
        print(f"Подпись {i}: {sig}")
    print("\n" + "="*50)
    print("\nСброс генератора:")
    generator.reset()
    print(f"Новый timestamp: {generator.timestamp}")
    print(f"Подпись после сброса: {generator.generate_signature()}")


if __name__ == "__main__":
    main()
