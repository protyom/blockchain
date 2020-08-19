# Miner
import socket_utils
import transaction
import TxBlock
import signatures

wallet_list = ['localhost']
tx_list = []
head_blocks=[None]


def findLongestBlockchain():
    longest = -1
    long_head = None
    for b in head_blocks:
        current = b
        this_len = 0
        while current != None:
            this_len = this_len + 1
            current = current.previousBlock
        if this_len > longest:
            long_head = b
            longest = this_len
    return long_head


class Miner:

    def __init__(self, public_key):
        self.__connection = socket_utils.SocketConnection()
        self.public_key = public_key
        
    def start_miner(self, wallets, ip_address, port):
        self.__connection.start_server(ip_address, port)
        for i in range(10):
            newTx = self.__connection.receive_object()
            if isinstance(newTx, transaction.Tx):
                tx_list.append(newTx)
                print("Recd tx")
            if len(tx_list) >= 2:
                break
        # add Txs to new block
        new_block = TxBlock.TxBlock(findLongestBlockchain())
        new_block.add_transaction(tx_list[0])
        new_block.add_transaction(tx_list[1])
        # Compute and add mining reward
        total_in, total_out = new_block.get_totals()
        mine_reward = transaction.Tx()
        mine_reward.add_output(self.public_key, 25.0 + total_in - total_out)
        new_block.add_transaction(mine_reward)
        # Find nonce
        for i in range(10):
            print("Finding Nonce...")
            new_block.find_nonce()
            if new_block.is_good_nonce():
                print("Good nonce found")
                break
        if not new_block.is_good_nonce():
            print("Error. Couldn't find nonce")
            return False
        # Send new block
        for ip_addr in wallet_list:
            print("Sending to " + ip_addr)
            self.__connection.send_object(ip_addr, new_block, 5006)
        head_blocks.remove(new_block.previous_block)
        head_blocks.append(new_block)
        return False


my_pr, my_pu = signatures.generate_keys()
miner = Miner(my_pu)
miner.start_miner(wallet_list, 'localhost', 5005)
