from signatures import generate_keys, sign, verify


class Tx:

    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.sigs = []
        self.reqd = []

    def __gather(self):
        return [self.inputs, self.outputs, self.reqd]

    def add_input(self, from_addr, amount):
        self.inputs.append((from_addr, amount))

    def add_output(self, to_addr, amount):
        self.outputs.append((to_addr, amount))

    def add_reqd(self, addr):
        self.reqd.append(addr)

    def sign(self, private_key):
        message = self.__gather()
        signature = sign(message, private_key)
        self.sigs.append(signature)

    def check_address(self, public_key, message):
        has_valid = False
        for signature in self.sigs:
            if verify(message, signature, public_key):
                has_valid = True
                break
        return has_valid

    def is_valid(self): # TODO: save signatures together with addresses. Maybe dict public_key -> amount, sign?
        message = self.__gather()
        total_in = 0
        total_out = 0
        if len(self.inputs) + len(self.reqd) > len(self.sigs):
            return False
        for public_key, amount in self.inputs:
            if amount < 0:
                return False
            total_in += amount
            if not self.check_address(public_key, message):
                return False

        for public_key in self.reqd:
            if not self.check_address(public_key, message):
                return False

        for public_key, amount in self.outputs:
            if amount < 0:
                return False
            total_out += amount

        if total_in < total_out:
            return False

        return True

    def __repr__(self):
        header = 'Transaction class:\nInputs:\n'
        inputs = '\n'.join([str(input_addr) for input_addr in self.inputs])
        outputs = '\n'.join([str(output_addr) for output_addr in self.outputs])
        reqds = '\n'.join([str(req) for req in self.reqd])
        sigs = '\n'.join([str(sig) for sig in self.sigs])
        return '\n'.join((header, inputs, 'Outputs:\n', outputs, 'Signatures:\n', sigs, 'Requireds:\n', reqds, 'End.'))



if __name__=='__main__':

    pr1, pu1 = generate_keys()
    pr2, pu2 = generate_keys()
    pr3, pu3 = generate_keys()
    pr4, pu4 = generate_keys()

    Tx1 = Tx()
    Tx1.add_input(pu1, 1)
    Tx1.add_output(pu2, 1)
    Tx1.sign(pr1)
    if Tx1.is_valid():
        print("Success! Tx is valid")
    else:
        print("ERROR! Tx is invalid")

    Tx2 = Tx()
    Tx2.add_input(pu1, 2)
    Tx2.add_output(pu2, 1)
    Tx2.add_output(pu3, 1)
    Tx2.sign(pr1)

    Tx3 = Tx()
    Tx3.add_input(pu3, 1.2)
    Tx3.add_output(pu1, 1.1)
    Tx3.add_reqd(pu4)
    Tx3.sign(pr3)
    Tx3.sign(pr4)

    for t in [Tx1, Tx2, Tx3]:
        if t.is_valid():
            print("Success! Tx is valid")
        else:
            print("ERROR! Tx is invalid")

    # Wrong signatures
    Tx4 = Tx()
    Tx4.add_input(pu1, 1)
    Tx4.add_output(pu2, 1)
    Tx4.sign(pr2)

    # Escrow Tx not signed by the arbiter
    Tx5 = Tx()
    Tx5.add_input(pu3, 1.2)
    Tx5.add_output(pu1, 1.1)
    Tx5.add_reqd(pu4)
    Tx5.sign(pr3)

    # Two input addrs, signed by one
    Tx6 = Tx()
    Tx6.add_input(pu3, 1)
    Tx6.add_input(pu4, 0.1)
    Tx6.add_output(pu1, 1.1)
    Tx6.sign(pr3)

    # Outputs exceed inputs
    Tx7 = Tx()
    Tx7.add_input(pu4, 1.2)
    Tx7.add_output(pu1, 1)
    Tx7.add_output(pu2, 2)
    Tx7.sign(pr4)

    # Negative values
    Tx8 = Tx()
    Tx8.add_input(pu2, -1)
    Tx8.add_output(pu1, -1)
    Tx8.sign(pr2)

    # Modified Tx
    Tx9 = Tx()
    Tx9.add_input(pu1, 1)
    Tx9.add_output(pu2, 1)
    Tx9.sign(pr1)
    # outputs = [(pu2,1)]
    # change to [(pu3,1)]
    Tx9.outputs[0] = (pu3, 1)

    for t in [Tx4, Tx5, Tx6, Tx7, Tx8, Tx9]:
        if t.is_valid():
            print("ERROR! Bad Tx is valid")
        else:
            print("Success! Bad Tx is invalid")
