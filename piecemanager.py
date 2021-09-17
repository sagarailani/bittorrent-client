from hashlib import sha1
import math

REQUEST_SIZE = 2**14
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

class PieceManager:

    def __init__(self, torrent):
        self.torrent = torrent    
        self.have_pieces = []
        self.ongoing_pieces = []
        self.pending_blocks = []
        self.missing_pieces = self._initiate_pieces()
        self.total_pieces = len(self.torrent.pieces)

    def _initiate_pieces(self):
        total_pieces = self.torrent.pieces
        std_piece_blocks = math.ceil(self.torrent.piece_length / REQUEST_SIZE)
        pieces = []

        for index, hashvalue in enumerate(total_pieces):

            if index < (len(total_pieces) - 1):
                blocks = [Block(index, offset * REQUEST_SIZE, REQUEST_SIZE) for offset in range(std_piece_blocks)]
            else:
                last_piece_size = self.torrent.total_size % self.torrent.piece_length
                last_piece_blocks = math.ceil(last_piece_size / REQUEST_SIZE)
                blocks = [Block(index, offset * REQUEST_SIZE, REQUEST_SIZE) for offset in range(last_piece_blocks)]
                if last_piece_size % REQUEST_SIZE > 0:
                    block = blocks[-1]
                    block.length = last_piece_size % REQUEST_SIZE
                    blocks[-1] = block
            pieces.append(Piece(index, blocks, hashvalue))
        return pieces

    @property
    def complete(self):
        return len(self.have_pieces) == self.total_pieces