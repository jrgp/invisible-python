def encode(source: bytes) -> bytes:
    bits = b"".join(f"{byte:08b}".encode("ascii") for byte in source)
    return bits.replace(b"0", b" ").replace(b"1", b"\t")


def decode(encoded: bytes) -> bytes:
    if len(encoded) % 8 or any(byte not in (32, 9) for byte in encoded):
        raise ValueError("Encoded input must contain only spaces and tabs in groups of eight")
    bits = encoded.replace(b" ", b"0").replace(b"\t", b"1")
    return bytes(int(bits[index:index + 8], 2) for index in range(0, len(bits), 8))
