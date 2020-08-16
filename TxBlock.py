from cblock import CBlock
from transaction import Tx
from signatures import generate_keys
import pickle


class TxBlock(CBlock):
    def __init__(self, previous_block):
        super(TxBlock, self).__init__([], previous_block)

    def add_transaction(self, transaction):
        self.data.append(transaction)

    def is_valid(self):
        if not super(TxBlock, self).is_valid():
            return False
        for transaction in self.data:
            if not transaction.is_valid():
                return False
        return True

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

    savefile = open("block.dat", "wb")
    pickle.dump(B1, savefile)
    savefile.close()

    loadfile = open("block.dat", "rb")
    load_B1 = pickle.load(loadfile)
    print(B1.data)
    print(load_B1.data)

    for b in [root, B1, load_B1, load_B1.previous_block]:
        if b.is_valid():
            print("Success! Valid block")
        else:
            print("ERROR! Bad block")

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

