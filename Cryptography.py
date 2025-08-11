import rsa

class Cryptography:
    def __init__(self, key_size):
        self.key_size = key_size
        self.public_key, self.private_key = rsa.newkeys(self.key_size)
        self.modulus = self.public_key.n  # Save modulus for later use

    def encrypt(self, message):
        if isinstance(message, str):
            message = message.encode()  # Convert to bytes if it's a string
        cipher = rsa.encrypt(message, self.public_key)
        return cipher, self.modulus

    def decrypt(self, message):
        return rsa.decrypt(message, self.private_key)

    def customDecrypt(self, message, key, n):
        # Create a temporary private key with the provided parameters
        temp_private_key = rsa.PrivateKey(n, 65537, key, 0, 0)
        return rsa.decrypt(message, temp_private_key)

    def get_public_key(self):
        return self.public_key

    def get_private_key(self):
        return self.private_key

    def get_key_size(self):
        return self.key_size
