 # importing libraries

import datetime
import hashlib
import json
from flask import Flask, jsonify


# -----------------------------------------------------------------------------------------------------------------------------------
# Part 1:  Building a BLOCKCHAIN
# -----------------------------------------------------------------------------------------------------------------------------------

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0', hash='0')

    def create_block(self, proof, previous_hash, hash):
        block = {
            'index': len(self.chain) + 1,
            'hash': hash,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof, hash_operation


    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    


# -----------------------------------------------------------------------------------------------------------------------------------
# Part 2:  Mining our Blockchain
# -----------------------------------------------------------------------------------------------------------------------------------

# Creating a Web App        
app = Flask(__name__)

# Creating A Blockchain
blockchain = Blockchain()

@app.route('/mine_block', methods = ['GET'])

def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof, hash_value = blockchain.proof_of_work(previous_proof)
    previous_hash = previous_block['hash']
    block = blockchain.create_block(proof, previous_hash, hash_value)
    response = {'message': 'Congratulations, You just mined a block!',
                'index': block['index'],
                'hash': block['hash'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}

    return jsonify(response), 200


# Getting The Full Blockchain
@app.route('/get_chain', methods = ['GET'])

def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    
    return jsonify(response), 200

# Running the App
app.run(host= '0.0.0.0', port= 5000)
