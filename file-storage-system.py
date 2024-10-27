import hashlib
import time
import os

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index  # Block index
        self.previous_hash = previous_hash  # Hash of the previous block
        self.timestamp = timestamp  # Time of block creation
        self.data = data  # Data stored in the block
        self.hash = hash  # Current block's hash


def calculate_hash(index, previous_hash, timestamp, data):
    # Create a hash for the block using its contents
    value = str(index) + str(previous_hash) + str(timestamp) + str(data)
    return hashlib.sha256(value.encode()).hexdigest()  # SHA-256 hashing


class Blockchain:
    def __init__(self):
        self.chain = []  # Initialize an empty list for the blockchain
        self.create_block(0, "0")  # Create the genesis block


    def create_block(self, index, previous_hash, data=""):
        # Create a new block and append it to the chain
        timestamp = time.time()
        hash = calculate_hash(index, previous_hash, timestamp, data)
        block = Block(index, previous_hash, timestamp, data, hash)  # Create a new block
        self.chain.append(block)  # Add the block to the chain

        return block


    def add_file(self, file_path):
        # Add a file to the blockchain
        if os.path.exists(file_path): 
            with open(file_path, 'rb') as file:  # Open the file in binary mode
                content = file.read()
                file_hash = hashlib.sha256(content).hexdigest()  # Calculate file hash
                block_data = {'file_name': os.path.basename(file_path), 'file_hash': file_hash}

                # Create a block with file metadata
                self.create_block(len(self.chain), self.chain[-1].hash, block_data)  # Add to blockchain

                return block_data
            
        else:
            raise FileNotFoundError("File not found")  # Raise an error if the file is missing


    def get_files(self):
        # Retrieve metadata for all files stored in the blockchain
        return [block.data for block in self.chain]  # Return list of file data


# Example usage
blockchain = Blockchain()

# Upload a file (make sure to have a file named "test.txt" in the same directory)
file_data = blockchain.add_file("test.txt")
print("File added:", file_data)

# Retrieve all files
files = blockchain.get_files()
print("Files in the blockchain:")
for f in files:
    print(f)
