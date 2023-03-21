import secrets

# Tinyec is not a library suitable for production. It is useful
# for security professionals to understand the inner workings of
# EC, and be able to play with pre-defined curves.
from tinyec import registry


curve = registry.get_curve("brainpoolP256r1")


def compress_point(point):
    return hex(point.x) + hex(point.y % 2)[2:]


def ecc_calc_encryption_keys(public_key):
    ciphertext_private_key = secrets.randbelow(curve.field.n)
    ciphertext_public_key = ciphertext_private_key * curve.g
    shared_ecc_key = public_key * ciphertext_private_key
    return shared_ecc_key, ciphertext_public_key


def ecc_calc_decryption_key(private_key, ciphertext_public_key):
    shared_ecc_key = ciphertext_public_key * private_key
    return shared_ecc_key


priv_key = secrets.randbelow(curve.field.n)
pub_key = priv_key * curve.g
print("Private key:", hex(priv_key))
print("Public key:", compress_point(pub_key))

(encrypt_key, cipher_public_key) = ecc_calc_encryption_keys(pub_key)
print("Ciphertext public key:", compress_point(cipher_public_key))
print("Encryption key:", compress_point(encrypt_key))

decrypt_key = ecc_calc_decryption_key(priv_key, cipher_public_key)
print("Decryption key:", compress_point(decrypt_key))
