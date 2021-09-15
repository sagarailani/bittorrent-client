from hashlib import sha1

class Block:

    Missing = 0
    Pending = 1
    Retrieved = 2

    def __init__(self, piece : int, offset : int, length : int) :
        self.piece = piece
        self.offset = offset
        self.length = length
        self.status = self.Missing
        self.data = None

class Piece:

    def __init__(self, index : int, blocks, hash_value) :
        self.index = index
        self.blocks = blocks
        self.hash_value = hash_value

    def reset(self):
        for block in self.blocks:
            block.status = Block.Missing
    
    def nextRequest(self) -> Block:
        # Here I want to find out next missing block inside the piece and return it        
        missing = [b for b in self.blocks if b.status is Block.Missing]
        if missing:
            missing[0].status = Block.Pending
            return missing[0]
        return None
    
    def blockRecieved(self, offset: int, data: bytes):
        # Here I want to check length of recieved block against the block data I have
        # Also do I want to check the hash of the block ? I think I got to check if all the blocks are present
        # If they are, I can verify the hash and if it mismatches I can reset the piece and set it's state to missing.
        recievedBlock = [b for b in self.blocks if offset == b.offset]
        block = recievedBlock[0] if recievedBlock else None
        if block or len(data) == block.length:            
            block.data = data
            block.status = Block.Retrieved
        
        if self.isPieceComplete():
            if not self.isHashMatching():
                self.reset()

    def isPieceComplete(self) -> bool:
        for block in self.blocks:
            if block.status == Block.Missing or block.status == Block.Pending:
                return False
        return True

    def isHashMatching(self) -> bool:
        return self.hash_value == sha1(self.data).digest

    @property
    def data(self):
        retrieved = sorted(self.blocks, key=lambda b: b.offset)
        return b''.join(block.data for block in retrieved)


