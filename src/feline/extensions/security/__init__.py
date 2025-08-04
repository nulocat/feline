import base64
import hashlib
import hmac
import os


class AlgorithmNotSupported(Exception):
    def __init__(self, algorithm) -> None:
        super().__init__(
            f"This algorithm '{algorithm}' can't be checked by Feline Security."
        )


SUPPORTED_ALGORITHMS = {"sha256", "sha512", "sha3_256"}


def secure_hash(
    secret: str,
    iterations: int = 260_000,
    salt_size: int = 16,
    pbkdf2_hash_algorithm: str = "sha256",
) -> str:
    """
    Hashes a secret using PBKDF2 with the specified algorithm and salt.
    Returns a string in the format: pbkdf2_<algorithm>$<iterations>$<salt_b64>$<hash_b64>
    """
    if pbkdf2_hash_algorithm not in SUPPORTED_ALGORITHMS:
        raise AlgorithmNotSupported(pbkdf2_hash_algorithm)

    salt = os.urandom(salt_size)
    hash_bytes = hashlib.pbkdf2_hmac(
        pbkdf2_hash_algorithm, secret.encode(), salt, iterations
    )
    return f"pbkdf2_{pbkdf2_hash_algorithm}${iterations}${base64.b64encode(salt).decode()}${base64.b64encode(hash_bytes).decode()}"


def hash_check(secret: str, secret_hashed: str) -> bool:
    """
    Verifies a secret against its hashed value.
    """
    algorithm, iterations_str, salt_b64, hash_b64 = secret_hashed.split("$")
    algorithm_parts = algorithm.split("_")

    if algorithm_parts[0] != "pbkdf2" or algorithm_parts[1] not in SUPPORTED_ALGORITHMS:
        raise AlgorithmNotSupported(algorithm)

    iterations = int(iterations_str)
    salt = base64.b64decode(salt_b64)
    expected_hash = base64.b64decode(hash_b64)
    result_hash = hashlib.pbkdf2_hmac(
        algorithm_parts[1], secret.encode(), salt, iterations
    )
    return hmac.compare_digest(result_hash, expected_hash)
