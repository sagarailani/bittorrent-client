import struct
import bitstring

class PeerMessage:

    Choke = 0
    Unchoke = 1
    Interested = 2
    NotInterested = 3
    Have = 4
    Bitfield = 5
    Request = 6
    Piece = 7
    Cancel = 8
    Handshake = None
    KeepAlive = None

    def encode(self) -> bytes:
        pass

    @classmethod
    def decode(cls, data: bytes):
        pass

class Handshake(PeerMessage):

    """
    Handshake message contains 
    <lenPstr><pstr><8paddedbytes><infoHash><peerId>
    <1><len(protocol)><8><20><20>
    total comes upto 49 + len(protocol) which is 19 in this case

    """
    protocol = b'Bittorrent protocol'
    length = 49 + 19

    def __init__(self, info_hash: bytes, peer_id: bytes):
        if isinstance(info_hash, str):
            info_hash = info_hash.encode('utf-8')
        if isinstance(peer_id, str):
            peer_id = peer_id.encode('utf-8')
        self.info_hash = info_hash
        self.peer_id = peer_id
    
    def encode(self):
        """

        """
        return struct.pack(
            '>B19s8x20s20s',
            19,
            Handshake.protocol,
            self.info_hash,
            self.peer_id
        )

    @classmethod
    def decode(cls, data: bytes):
        if len(data) < Handshake.length:
            return None
        parts = struct.unpack('>B19s8x20s20s', data)
        print("Printing parts after decoding hash message")
        print(parts)
        return cls(parts[2], parts[3])

class KeepAlive(PeerMessage):

    def __str__(self) -> str:
        return 'KeepAlive'
    
class Choke(PeerMessage):

    def __str__(self) -> str:
        return 'Choke'

class Unchoke(PeerMessage):

    def __str__(self) -> str:
        return 'Unchoke'

class Interested(PeerMessage):

    def encode(self) -> bytes:
        return struct.pack(
            '>Ib',
            1,
            PeerMessage.Interested)

    def __str__(self) -> str:
        return 'Interested'
    

class NotInterested(PeerMessage):

    def encode(self) -> bytes:
        return struct.pack(
            '>Ib',
            1,
            PeerMessage.NotInterested)

    def __str__(self) -> str:
        return 'NotInterested'
    
class Have(PeerMessage):

    def __init__(self, index: int):
        self.index = index

    def encode(self) -> bytes:
        return struct.pack(
            '>IbI',
            5,
            PeerMessage.Have,
            self.index)
    
    @classmethod
    def decode(cls, data: bytes):
        if len(data) < 5:
            return None
        parts = struct.unpack('>IbI', data)
        return cls(parts[2])

class Bitfield(PeerMessage):

    """
    This bitfield seems like current status of the download
    so, if a torrent has 5 pieces and all of them are missing then bitfield would be 
    00000 -> 5 zeros, 1 for each piece
    000 -> 3 additional zeros to complete the byte
    highest bit is 0th piece and next highest is 1st piece and so on.
    """

    def __init__(self, data):
        self.bitfield = bitstring.BitArray(bytes=data)
        print("printing bitfield")
        print(self.bitfield)
    
    def encode(self) -> bytes:
        size = len(self.bitfield)
        packWithThis = '>Ib' + str(size) + 's'
        print(packWithThis)
        return struct.pack(
            packWithThis,
            1 + size,
            PeerMessage.Bitfield,
            self.bitfield
        )

    @classmethod
    def decode(cls, data: bytes):
        length = struct.unpack('>Ib', data[:4])[0]
        parts = struct.unpack('>Ib' + (length - 1) + 's', data)
        return cls(parts[2])


# class Request(PeerMessage):

# class Piece(PeerMessage):

# class Cancel(PeerMessage):


