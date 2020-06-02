from hashlib import sha256
import json
import time
import rsa
from flask import Flask, request
import requests
import base64

from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as Sig_pk
from Crypto.Hash import SHA, SHA256, MD5
 
def rsa_sign(data, key_path):
    """
    :param pri_key: 私钥
    :param data: 待签名数据
    :param sign_type: 的签名方式
    :return:
    """
    key = open(key_path, 'r').read()
    rsakey = RSA.importKey(key)
    # 根据sha算法处理签名内容  (此处的hash算法不一定是sha,看开发)
    data = SHA.new(data.encode())
    # 私钥进行签名
    sig_pk = Sig_pk.new(rsakey)
    sign = sig_pk.sign(data)
    # 将签名后的内容，转换为base64编码
    result = base64.b64encode(sign)
    # 签名结果转换成字符串
    signature = result.decode()
    #print('signature: ',data)
    return signature
 
 
def rsa_verify(data, signature, public_key_path):
    """
    :param pub_key: 公钥
    :param data: 待签名数据
    :param sign: 需要验签的签名
    :param sign_type: 的签名方式
    :return:
    """
    # base64解码
    signature = base64.b64decode(signature)
    # 获取公钥
    key = open(public_key_path).read()
    rsakey = RSA.importKey(key)
    # 将签名之前的内容进行hash处理
    sha_name = SHA.new(data.encode())
    # 验证签名
    signer = Sig_pk.new(rsakey)
    result = signer.verify(sha_name, signature)
    # 验证通过返回True   不通过返回False
    #print(result)
    return result
    


def compute_merkle_root_hash(transactions):
        if transactions == []:
            return 'None'
        trans_contents = [trans['content'] for trans in transactions]
        while len(trans_contents) != 1:
            if len(trans_contents) % 2 == 1:
                last = len(trans_contents) - 3
            else:
                last = len(trans_contents) - 2
            i = 0
            new_contents = []
            while i <= last:
                left = trans_contents[i]
                right = trans_contents[i+1]
                double_hash_left = sha256(sha256(left.encode()).hexdigest().encode()).hexdigest()
                double_hash_right = sha256(sha256(right.encode()).hexdigest().encode()).hexdigest()
                c = double_hash_left + double_hash_right 
                c_hash = sha256(sha256(c.encode()).hexdigest().encode()).hexdigest()
                new_contents.append(c_hash)
                i += 2
            if len(trans_contents) % 2 == 1:
                new_contents.append(trans_contents[last+2])
            trans_contents = new_contents
        return trans_contents[0]

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.merkle_hash = compute_merkle_root_hash(self.transactions)
        self.nonce = nonce

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        '''
        s = ""
        s += str(self.index)
        for i in range(len(self.transactions)):
            s += self.transactions[i]
        s += str(self.timestamp)
        s += self.previous_hash
        s += str(self.nonce)

        s_json = json.dumps(s)
        x = sha256()
        x.update(s_json.encode())
        h = x.hexdigest()
        return h
        '''

        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()
    

    


class Blockchain:
    # difficulty of our PoW algorithm
    difficulty = 2

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []

    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        index = 0
        transactions = []
        timestamp = 0.0
        previous_hash = "0"*64
        block = Block(index=index, transactions=transactions, timestamp=timestamp,previous_hash=previous_hash)
        block.hash = block.compute_hash()
        self.chain.append(block)


    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            print('Previous hash is not matched.')
            return False

        if not Blockchain.is_valid_proof(block, proof):
            print('Proof is not valid.')
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    @staticmethod
    def proof_of_work(block):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our difficulty criteria.
        """
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not Blockchain.ifsatisfy_diff(computed_hash):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_new_transaction(self, transaction):
        #print(transaction)
        content = transaction['content']
        #content = content.encode("utf8")
        
        random_gen = Random.new().read
        #生成秘钥对实例对象：1024是秘钥的长度
        rsa = RSA.generate(1024, random_gen)

        # 获取公钥，保存到文件
        private_pem = rsa.exportKey()
        private_key_path = transaction['author']+'_private.pem'
        with open(private_key_path, 'wb') as f:
            f.write(private_pem)

        # 获取私钥保存到文件
        public_pem = rsa.publickey().exportKey()
        public_key_path = transaction['author']+'_public.pem'
        with open(public_key_path, 'wb') as f:
            f.write(public_pem)
        
        signature = rsa_sign(content, private_key_path)
        print('signature: ',signature)
        transaction['signature'] = signature

        #verify = rsa_verify(content, signature, public_key_path)
        #print(verify)
        
        self.unconfirmed_transactions.append(transaction)
    
    @staticmethod
    def ifsatisfy_diff(s):
        for i in range(Blockchain.difficulty):
            if s[i] == 1:
                return False
        return True

    @classmethod
    def is_valid_proof(cls, block, block_hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (cls.ifsatisfy_diff(block_hash) and block_hash == block.compute_hash())

    @classmethod
    def check_chain_validity(cls, chain):
        result = True
        previous_hash = "0"

        for block in chain:
            block_hash = block.hash
            # remove the hash field to recompute the hash again
            # using `compute_hash` method.
            delattr(block, "hash")

            if not cls.is_valid_proof(block, block_hash) or previous_hash != block.previous_hash:
                result = False
                break

            block.hash, previous_hash = block_hash, block_hash

        return result

    def mine(self):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """
        if self.unconfirmed_transactions == []:
            return False

        transactions = self.unconfirmed_transactions
        for transaction in transactions:
            author = transaction['author']
            public_key_path = author + '_public.pem'
            content = transaction['content']
            signature = transaction['signature']
            verify = rsa_verify(content, signature, public_key_path)
            if verify == False:
                print('Transaction not verified.')
                return 
        previous_block = self.last_block
        last_index = previous_block.index

        index = last_index + 1
        timestamp = time.time()
        previous_hash = previous_block.hash

        newblock = Block(index=index, transactions=transactions, timestamp=timestamp, previous_hash=previous_hash)
        proof = Blockchain.proof_of_work(newblock)

        self.add_block(newblock, proof)
        self.unconfirmed_transactions = []
        return newblock.index



app = Flask(__name__)

# the node's copy of blockchain
blockchain = Blockchain()
blockchain.create_genesis_block()

# the address to other participating members of the network
peers = set()


# endpoint to submit a new transaction. This will be used by
# our application to add new data (posts) to the blockchain
@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    required_fields = ["author", "content"]

    for field in required_fields:
        if not tx_data.get(field):
            return "Invalid transaction data", 404

    tx_data["timestamp"] = time.time()

    blockchain.add_new_transaction(tx_data)

    return "Success", 201


# endpoint to return the node's copy of the chain.
# Our application will be using this endpoint to query
# all the posts to display.
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data,
                       "peers": list(peers)})


# endpoint to request the node to mine the unconfirmed
# transactions (if any). We'll be using it to initiate
# a command to mine from our application itself.
@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
    result = blockchain.mine()
    if not result:
        return "No transactions to mine"
    else:
        # Making sure we have the longest chain before announcing to the network
        chain_length = len(blockchain.chain)
        consensus()
        if chain_length == len(blockchain.chain):
            # announce the recently mined block to the network
            announce_new_block(blockchain.last_block)
        return "Block #{} is mined.".format(blockchain.last_block.index)


# endpoint to add new peers to the network.
@app.route('/register_node', methods=['POST'])
def register_new_peers():
    node_address = request.get_json()["node_address"]
    print('register_node:',node_address)
    if not node_address:
        return "Invalid data", 400

    # Add the node to the peer list
    peers.add(node_address)

    # Return the consensus blockchain to the newly registered node
    # so that he can sync
    return get_chain()


@app.route('/register_with', methods=['POST'])
def register_with_existing_node():
    """
    Internally calls the `register_node` endpoint to
    register current node with the node specified in the
    request, and sync the blockchain as well as peer data.
    """
    #print('********************')
    print(request.get_json())
    node_address = request.get_json()["node_address"]
    if not node_address:
        return "Invalid data", 400

    data = {"node_address": request.host_url}
    headers = {'Content-Type': "application/json"}

    # Make a request to register with remote node and obtain information
    response = requests.post(node_address + "/register_node",
                             data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        global blockchain
        global peers
        # update chain and the peers
        chain_dump = response.json()['chain']
        blockchain = create_chain_from_dump(chain_dump)
        peers.update(response.json()['peers'])
        return "Registration successful", 200
    else:
        # if something goes wrong, pass it on to the API response
        #print(response.content)
        #print(response.status_code)
        return response.content, response.status_code



def create_chain_from_dump(chain_dump):
    generated_blockchain = Blockchain()
    generated_blockchain.create_genesis_block()
    for idx, block_data in enumerate(chain_dump):
        if idx == 0:
            continue  # skip genesis block
        block = Block(block_data["index"],
                      block_data["transactions"],
                      block_data["timestamp"],
                      block_data["previous_hash"],
                      block_data["nonce"])
        proof = block_data['hash']
        added = generated_blockchain.add_block(block, proof)
        if not added:
            raise Exception("The chain dump is tampered!!")
    return generated_blockchain


# endpoint to add a block mined by someone else to
# the node's chain. The block is first verified by the node
# and then added to the chain.
@app.route('/add_block', methods=['POST'])
def verify_and_add_block():
    block_data = request.get_json()
    block = Block(block_data["index"],
                  block_data["transactions"],
                  block_data["timestamp"],
                  block_data["previous_hash"],
                  block_data["nonce"])

    proof = block_data['hash']
    added = blockchain.add_block(block, proof)

    if not added:
        return "The block was discarded by the node", 400

    return "Block added to the chain", 201


# endpoint to query unconfirmed transactions
@app.route('/pending_tx')
def get_pending_tx():
    return json.dumps(blockchain.unconfirmed_transactions)


def consensus():
    """
    Our naive consnsus algorithm. If a longer valid chain is
    found, our chain is replaced with it.
    """
    global blockchain

    longest_chain = None
    current_len = len(blockchain.chain)

    for node in peers:
        response = requests.get('{}chain'.format(node))
        length = response.json()['length']
        chain = response.json()['chain']
        if length > current_len and blockchain.check_chain_validity(chain):
            current_len = length
            longest_chain = chain

    if longest_chain:
        blockchain = longest_chain
        return True

    return False


def announce_new_block(block):
    """
    A function to announce to the network once a block has been mined.
    Other blocks can simply verify the proof of work and add it to their
    respective chains.
    """
    for peer in peers:
        url = "{}add_block".format(peer)
        headers = {'Content-Type': "application/json"}
        requests.post(url,
                      data=json.dumps(block.__dict__, sort_keys=True),
                      headers=headers)
