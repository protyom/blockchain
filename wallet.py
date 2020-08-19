# Wallet
from socket_utils import SocketConnection
import transaction
import signatures

connection = SocketConnection()

head_blocks = [None] # stores blocks in RAM

pr1, pu1 = signatures.generate_keys()
pr2, pu2 = signatures.generate_keys()
pr3, pu3 = signatures.generate_keys()

Tx1 = transaction.Tx()
Tx2 = transaction.Tx()

Tx1.add_input(pu1, 4.0)
Tx1.add_input(pu2, 1.0)
Tx1.add_output(pu3, 4.8)
Tx2.add_input(pu3, 4.0)
Tx2.add_output(pu2, 4.0)
Tx2.add_reqd(pu1)

Tx1.sign(pr1)
Tx1.sign(pr2)
Tx2.sign(pr3)
Tx2.sign(pr1)

try:
    connection.send_object('localhost', Tx1)
    print("Sent Tx1")
    connection.send_object('localhost', Tx2)
    print("Sent Tx2")
except:
    print("Error! Connection unsuccessful")

connection.start_server('localhost', 5006)
for i in range(30):
    new_block = connection.receive_object()
    if new_block:
        break
connection.close()

if new_block.is_valid():
    print("Success! Block is valid")
if new_block.good_nonce():
    print("Success! Nonce is valid")

for b in head_blocks:
    if new_block.previousHash == b.compute_hash():
        new_block.previous_block = b
        head_blocks.remove(b)
        head_blocks.append(new_block)




