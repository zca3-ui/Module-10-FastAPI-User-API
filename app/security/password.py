from pwdlib import PasswordHash

# Configure Argon2 password hashing
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Hash a plain-text password using Argon2.

    Returns the secure password hash.
    """
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verify a plain-text password against its stored hash.

    Returns True if the password matches, otherwise False.
    """
    return password_hash.verify(
        plain_password,
        hashed_password
    )