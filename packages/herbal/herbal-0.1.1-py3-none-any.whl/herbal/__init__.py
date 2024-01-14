"""Python package for the Tiny Encryption Algorithm (TEA)."""

import os
import struct
from base64 import b85decode, b85encode
from ctypes import c_uint32 as uint32_t
from hashlib import scrypt
from typing import Iterable, Union, overload

__all__ = ["encrypt", "decrypt"]
__version__ = "0.1.1"

String = Union[str, bytes]
Block64 = tuple[uint32_t, uint32_t]
Block128 = tuple[uint32_t, uint32_t, uint32_t, uint32_t]

# 2^32 / 𝜙 (golden ratio)
KEY_SCHEDULE = int(2**32 / ((1 + 5**0.5) / 2))


def derive_key(password: bytes, *, salt: bytes) -> Block128:
    """
    Securely derive a 128-bit encryption key from a given password.

    Uses the scrypt key derivation function.

    :param bytes password: Password bytes object.
    :param bytes salt: Random data to prevent rainbow table cracking.
    :return Block128: Key represented as four unsigned 32-bit integers.
    """
    size = 16  # 128 bits.
    key = scrypt(password, salt=salt, n=2**14, r=8, p=1, dklen=size)
    a, b, c, d = (uint32_t(i) for i in struct.unpack(">4I", key))
    return a, b, c, d


def to_blocks(data: bytes, add_padding: bool = False) -> Iterable[Block64]:
    """
    Convert bytes into a sequence of uint32 blocks.

    :param bytes data: Bytes data to be converted.
    :param add_padding bool: Add padding to data, defaults to False.
    :yield Iterable[Block64]: Sequence of two unsigned 32-bit integers.
    """
    size = 8  # 64 bits.
    if add_padding:
        # Add random padding to prevent errors with smaller block sizes.
        pad = size - len(data) % size
        data += os.urandom(pad - 1) + pad.to_bytes(1, "big")
    uint32_array = (
        struct.unpack(">2I", data[i : i + size])
        for i in range(0, len(data), size)
    )
    blocks = ((uint32_t(y), uint32_t(z)) for (y, z) in (uint32_array))
    yield from blocks


def from_blocks(
    blocks: Iterable[Block64], remove_padding: bool = False
) -> bytes:
    """
    Convert a sequence of uint32 blocks into bytes.

    :param Iterable[Block64] blocks: Sequence of two unsigned 32-bit
        integers.
    :param remove_padding bool: Remove padding from data, defaults
        to False.
    :return bytes: Bytestring representation.
    """
    data = b"".join(struct.pack(">2I", y.value, z.value) for y, z in blocks)
    if remove_padding:
        # Remove padding from data.
        return data[: -data[-1]]
    return data


def encode_block(v: Block64, k: Block128, /) -> Block64:
    """
    TEA block encoding algorithm.

    https://www.tayloredge.com/reference/Mathematics/TEA-XTEA.pdf.

    :param Block64 v: Unencoded 64-bit block as two unsigned 32-bit
        integers.
    :param Key128 k: 128-bit key as four unsigned 32-bit integers.
    :return Block64: Encoded 64-bit block.
    """
    y, z = v
    sum_ = uint32_t(0)
    for _ in range(32):
        sum_.value += KEY_SCHEDULE
        y.value += (
            ((z.value << 4) + k[0].value)
            ^ (z.value + sum_.value)
            ^ ((z.value >> 5) + k[1].value)
        )
        z.value += (
            ((y.value << 4) + k[2].value)
            ^ (y.value + sum_.value)
            ^ ((y.value >> 5) + k[3].value)
        )
    return y, z


def decode_block(v: Block64, k: Block128, /) -> Block64:
    """
    TEA block decoding algorithm.

    https://www.tayloredge.com/reference/Mathematics/TEA-XTEA.pdf.

    :param Block64 v: Encoded 64-bit block as two unsigned 32-bit
        integers.
    :param Key128 k: 128-bit key as four unsigned 32-bit integers.
    :return Block64: Decoded 64-bit block.
    """
    y, z = v
    sum_ = uint32_t(KEY_SCHEDULE << 5)
    for _ in range(32):
        z.value -= (
            ((y.value << 4) + k[2].value)
            ^ (y.value + sum_.value)
            ^ ((y.value >> 5) + k[3].value)
        )
        y.value -= (
            ((z.value << 4) + k[0].value)
            ^ (z.value + sum_.value)
            ^ ((z.value >> 5) + k[1].value)
        )
        sum_.value -= KEY_SCHEDULE

    return y, z


@overload
def encrypt(plaintext: str, password: String) -> str:
    ...


@overload
def encrypt(plaintext: bytes, password: String) -> bytes:
    ...


def encrypt(plaintext: String, password: String) -> String:
    """
    Encrypt the provided plaintext using the TEA block cipher.

    >>> herbal.encrypt("hello, world! :3", password="secret")

    :param String plaintext: String to be encrypted.
    :param String password: Password to derive the encryption key from.
    :return String: Encrypted ciphertext.
    """
    data_type = type(plaintext)
    if isinstance(plaintext, str):
        plaintext = plaintext.encode()
    if isinstance(password, str):
        password = password.encode()

    salt = os.urandom(16)
    key = derive_key(password, salt=salt)
    blocks = to_blocks(plaintext, add_padding=True)
    encoded_blocks = (encode_block(i, key) for i in blocks)
    ciphertext = from_blocks(encoded_blocks)
    output = b85encode(salt) + b":" + b85encode(ciphertext)

    if data_type is str:
        return output.decode()
    return output


@overload
def decrypt(ciphertext: str, password: String) -> str:
    ...


@overload
def decrypt(ciphertext: bytes, password: String) -> bytes:
    ...


def decrypt(ciphertext: String, password: String) -> String:
    """
    Decrypt the provided ciphertext using the TEA block cipher.

    >>> herbal.decrypt(
    ...     "____)$x>_HL%IQu6Gn|A:E4h?9Cdc>N"
    ...     "DjFwP`;Ya1Qd6{O1;8JV%Nq}4(qY++",
    ...     password="secret"
    ... )

    :param String plaintext: String to be decrypted.
    :param String password: Password to derive the encryption key from.
    :return String: Decrypted plaintext.
    """
    data_type = type(ciphertext)
    if isinstance(ciphertext, str):
        ciphertext = ciphertext.encode()
    if isinstance(password, str):
        password = password.encode()

    salt, ciphertext = (b85decode(i) for i in ciphertext.split(b":"))

    if len(ciphertext) % 8:
        raise NotImplementedError("String bytes must be a multiple of 8.")

    key = derive_key(password, salt=salt)
    encoded_blocks = to_blocks(ciphertext)
    decoded_blocks = (decode_block(i, key) for i in encoded_blocks)
    plaintext = from_blocks(decoded_blocks, remove_padding=True)
    if data_type is str:
        return plaintext.decode()
    return plaintext
