import unittest
from ecies_xmr.ecies import MoneroECIES

class TestMoneroECIES(unittest.TestCase):

    def test_encrypt_decrypt(self):
        # Key Generation
        sender_private, sender_public = MoneroECIES.generate_keypair()
        receiver_private, receiver_public = MoneroECIES.generate_keypair()

        # Encryption
        original_message = "Hello, this is a test message!"
        ciphertext, tag, nonce = MoneroECIES.encrypt(sender_private, receiver_public, original_message)

        # Decryption
        decrypted_message = MoneroECIES.decrypt(receiver_private, sender_public, ciphertext, tag, nonce).decode()

        # Assertions
        self.assertEqual(decrypted_message, original_message, "Decryption failed or message corrupted!")

if __name__ == '__main__':
    unittest.main()
