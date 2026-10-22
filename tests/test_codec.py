import pytest

from invisible_python import decode, encode


@pytest.mark.parametrize("source", [b"", b'print("hello")\n', bytes(range(256))])
def test_round_trip(source):
    encoded = encode(source)
    assert decode(encoded) == source
    assert set(encoded) <= {32, 9}
    assert len(encoded) == 8 * len(source)


def test_bit_order():
    assert encode(b"\x00\x01\x80\xff") == (
        b"        " + b"       \t" + b"\t       " + b"\t\t\t\t\t\t\t\t"
    )


@pytest.mark.parametrize("encoded", [b"       \n", b"       0", b"\xef\xbb\xbf     ", b"       \r"])
def test_invalid_characters(encoded):
    with pytest.raises(ValueError):
        decode(encoded)


@pytest.mark.parametrize("encoded", [b" ", b"\t" * 7, b" " * 9])
def test_invalid_lengths(encoded):
    with pytest.raises(ValueError):
        decode(encoded)
