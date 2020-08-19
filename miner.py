# Miner
import socket_utils
import transaction
import TxBlock
import signatures

wallets = ['localhost']
tx_list = []


class Miner:

    def __init__(self, public_key):
        self.__connection = socket_utils.SocketConnection()
        self.public_key = public_key
        
    def start_miner(self, ip_address, port):
        self.__connection.start_server(ip_address, port)
        for i in range(10):
            newTx = self.__connection.receive_object()
            if isinstance(newTx, transaction.Tx):
                tx_list.append(newTx)
                print("Recd tx")
            if len(tx_list) >= 2:
                break
        # add Txs to new block
        new_block = TxBlock.TxBlock(None)
        new_block.add_transaction(tx_list[0])
        new_block.add_transaction(tx_list[1])
        # Compute and add mining reward
        total_in = new_block.get_total_in()
        total_out = new_block.get_total_out()
        mine_reward = transaction.Transaction()
        mine_reward.add_output(self.public_key, 25.0 + total_in - total_out)
        new_block.add_transaction(mine_reward)
        # Find nonce
        for i in range(10):
            print("Finding Nonce...")
            new_block.find_nonce()
            if new_block.good_nonce():
                print("Good nonce found")
                break
        if not new_block.good_nonce():
            print("Error. Couldn't find nonce")
            return False
        # Send new block
        for ip_addr in wallet_list:
            print("Sending to " + ip_addr)
            socket_utils.sendObj(ip_addr, new_block, 5006)
        head_blocks.remove(new_block.previousBlock)
        head_blocks.append(new_block)
        return False
            
    

def minerServer(my_ip, wallet_list, my_public):
    server = socket_utils.newServerConnection(my_ip)
    # Get 2 Txs from wallets
    


my_pr, my_pu = Signatures.generate_keys()
minerServer('localhost', wallets, my_pu)
