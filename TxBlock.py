import random
import time

from cblock import CBlock
from transaction import Tx
from signatures import generate_keys
import pickle


from Crypto.Hash import SHA256


REWARD = 25.
LEADING_ZEROS = 2
TARGET_START = bytes(''.join(['\x4f' for i in range(LEADING_ZEROS)]), 'utf8')


class TxBlock(CBlock):
    def __init__(self, previous_block):
        super(TxBlock, self).__init__([], previous_block)
        self.nonce = b''

    def add_transaction(self, transaction):
        self.data.append(transaction)

    def is_valid(self):
        if not super(TxBlock, self).is_valid():
            return False
        total_in, total_out = self.get_totals()
        if total_out - total_in - REWARD > 0.0000001:
            return False
        return True

    def get_totals(self):
        total_in = 0
        total_out = 0
        for transaction in self.data:
            if not transaction.is_valid():
                return False
            total_in += transaction.get_total_in()
            total_out += transaction.get_total_out()
        return total_in, total_out

    def compute_hash(self):
        if self.previous_block is None:
            return None
        hash = SHA256.new()
        hash.update(bytes(str(self.data), 'utf8'))
        hash.update(bytes(str(self.previous_hash), 'utf8'))
        hash.update(self.nonce)
        return hash.digest()

    def is_good_nonce(self):
        hash = SHA256.new()
        hash.update(bytes(str(self.data), 'utf8'))
        hash.update(bytes(str(self.previous_hash), 'utf8'))
        hash.update(self.nonce)
        digest = hash.digest()
        return digest[:LEADING_ZEROS] == TARGET_START

    def find_nonce(self):
        self.nonce = bytes(''.join(
            [chr(random.randint(0, 255)) for i in range(10 * LEADING_ZEROS)]),
                           'utf8')
        while not self.is_good_nonce():
            self.nonce = bytes(''.join(
                [chr(random.randint(0, 255)) for i in range(10*LEADING_ZEROS)]
            ), 'utf8')
        return None


if __name__ == "__main__":
    pr1, pu1 = generate_keys()
    pr2, pu2 = generate_keys()
    pr3, pu3 = generate_keys()

    Tx1 = Tx()
    Tx1.add_input(pu1, 1)
    Tx1.add_output(pu2, 1)
    Tx1.sign(pr1)

    if Tx1.is_valid():
        print("Success! Tx is valid")

    savefile = open("tx.dat", "wb")
    pickle.dump(Tx1, savefile)
    savefile.close()

    loadfile = open("tx.dat", "rb")
    newTx = pickle.load(loadfile)

    if newTx.is_valid():
        print("Sucess! Loaded tx is valid")
    loadfile.close()

    root = TxBlock(None)
    root.add_transaction(Tx1)

    Tx2 = Tx()
    Tx2.add_input(pu2, 1.1)
    Tx2.add_output(pu3, 1)
    Tx2.sign(pr2)
    root.add_transaction(Tx2)

    B1 = TxBlock(root)
    Tx3 = Tx()
    Tx3.add_input(pu3, 1.1)
    Tx3.add_output(pu1, 1)
    Tx3.sign(pr3)
    B1.add_transaction(Tx3)

    Tx4 = Tx()
    Tx4.add_input(pu1, 1)
    Tx4.add_output(pu2, 1)
    Tx4.add_reqd(pu3)
    Tx4.sign(pr1)
    Tx4.sign(pr3)
    B1.add_transaction(Tx4)
    start = time.time()
    print(B1.find_nonce())
    elapsed = time.time() - start
    print("elapsed time: " + str(elapsed) + " s.")
    if elapsed < 60:
        print("ERROR! Mining is too fast")
    if B1.is_good_nonce():
        print("Success! Nonce is good!")
    else:
        print("ERROR! Bad nonce")

    savefile = open("block.dat", "wb")
    pickle.dump(B1, savefile)
    savefile.close()

    loadfile = open("block.dat", "rb")
    load_B1 = pickle.load(loadfile)

    for b in [root, B1, load_B1, load_B1.previous_block]:
        if b.is_valid():
            print("Success! Valid block")
        else:
            print("ERROR! Bad block")

    if B1.is_good_nonce():
        print("Success! Nonce is good after save and load!")
    else:
        print("ERROR! Bad nonce after load")
    B2 = TxBlock(B1)
    Tx5 = Tx()
    Tx5.add_input(pu3, 1)
    Tx5.add_output(pu1, 100)
    Tx5.sign(pr3)
    B2.add_transaction(Tx5)

    load_B1.previous_block.add_transaction(Tx4)
    for b in [B2, load_B1]:
        if b.is_valid():
            print("ERROR! Bad block verified.")
        else:
            print("Success! Bad blocks detected")

    # Test mining rewards and tx fees
    pr4, pu4 = generate_keys()
    B3 = TxBlock(B2)
    B3.add_transaction(Tx2)
    B3.add_transaction(Tx3)
    B3.add_transaction(Tx4)
    Tx6 = Tx()
    Tx6.add_output(pu4, 25)
    B3.add_transaction(Tx6)
    if B3.is_valid():
        print("Success! Block reward succeeds")
    else:
        print("ERROR! Block reward fail")

    B4 = TxBlock(B3)
    B4.add_transaction(Tx2)
    B4.add_transaction(Tx3)
    B4.add_transaction(Tx4)
    Tx7 = Tx()
    Tx7.add_output(pu4, 25.2)
    B4.add_transaction(Tx7)
    if B4.is_valid():
        print("Success! Tx fees succeeds")
    else:
        print("ERROR! Tx fees fail")

    # Greedy miner
    B5 = TxBlock(B4)
    B5.add_transaction(Tx2)
    B5.add_transaction(Tx3)
    B5.add_transaction(Tx4)
    Tx8 = Tx()
    Tx8.add_output(pu4, 26.2)
    B5.add_transaction(Tx8)
    if not B5.is_valid():
        print("Success! Greedy miner detected")
    else:
        print("ERROR! Greedy miner not detected")