import base64
import hashlib
import secrets


def hash_password(password: str) -> str:
    """
    Хэширование пароля
    """
    salt = secrets.token_bytes(16)

    iterations = 300
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations)

    return str(hashed)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Проверка хэща с паролем
    True - совпадение
    False - некорректность
    """
    algorithm, iterations, salt_b64, hash_b64 = hashed_password.split('$')

    salt = base64.b64decode(salt_b64)
    expected_hash = base64.b64decode(hash_b64)

    provided_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        int(iterations)
    )

    return secrets.compare_digest(provided_hash, expected_hash)
