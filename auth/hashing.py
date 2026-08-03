# importing the password library module
from pwdlib import PasswordHash

# creating password hashing object
password_hash_instance = PasswordHash.recommended()

# function for hashing the password
def hash_password(password: str) -> str:
    hashed_password = password_hash_instance.hash(password)
    return hashed_password

# function for verifying the entered password
def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash_instance.verify(password, hashed_password)

