import os
import binascii
from Crypto.Cipher import AES
from .ed25519 import H, publickey, scalarmult, decodepoint, decodeint, encodepoint

class MoneroECIES:
    """
    A class representing the Elliptic Curve Integrated Encryption Scheme (ECIES) 
    for the Monero Edwards25519 curve.
    """

    @staticmethod
    def generate_keypair():
        """
        Generate a Monero keypair consisting of a private and a public key.
        """
        private_key = os.urandom(32)
        public_key = publickey(private_key)
        return private_key, public_key

    @staticmethod
    def encrypt(sender_private_key, receiver_public_key, message):
        """
        Encrypt a message using the sender's private key and the receiver's public key.
        """
        if isinstance(message, str):
            message = message.encode()

        shared_secret = scalarmult(decodepoint(receiver_public_key), decodeint(sender_private_key))
        key = H(encodepoint(shared_secret))[:32]

        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(message)

        return ciphertext, tag, cipher.nonce

    @staticmethod
    def decrypt(receiver_private_key, sender_public_key, ciphertext, tag, nonce):
        """
        Decrypt a message using the receiver's private key and the sender's public key.
        """
        try:
            shared_secret = scalarmult(decodepoint(sender_public_key), decodeint(receiver_private_key))
            key = H(encodepoint(shared_secret))[:32]

            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            return cipher.decrypt_and_verify(ciphertext, tag)
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")

    @staticmethod
    def hex_to_bytes(hex_string):
        """
        Convert a hex string to bytes.
        """
        return binascii.unhexlify(hex_string)


