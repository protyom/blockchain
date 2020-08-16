from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

from Crypto.Hash import SHA256


class CBlock:
    data = None
    previous_hash = None
    previous_block = None

    def __init__(self, data, previous_block):
        self.data = data
        if previous_block is not None:
            self.previous_hash = previous_block.compute_hash()
            self.previous_block = previous_block

    def compute_hash(self):
        hash = SHA256.new()
        hash.update(bytes(str(self.data), 'utf8'))
        hash.update(bytes(str(self.previous_hash), 'utf8'))
        return hash.digest()

    def is_valid(self):
        if self.previous_block is None:
            return True
        return self.previous_hash == self.previous_block.compute_hash()

