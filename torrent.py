"""
This wrapper will get input as torrent bytes data and decode it using the parser. 
And will have properties for all the data which is required from the torrent file

-> piece length
-> pieces
-> infoHash
-> announce string
-> file size
-> file name

"""
from hashlib import sha1
from collections import namedtuple
from bencoding import Decoder, Encoder

TorrentFile = namedtuple('TorrentFile', ['filename', 'length'])

class Torrent:

    def __init__(self, fileName) -> None:
        self.fileName = fileName
        self.files = []

        with open(self.fileName, 'rb') as f :
            metaInfo = f.read()  
            self.metaInfo = Decoder(metaInfo).decode()
            info = Encoder(self.metaInfo[b'info']).encode()
            self.infoHash = sha1(info).digest()
            self._extractFileNames()

    def _extractFileNames(self):
        self.files.append(TorrentFile(self.metaInfo[b'info'][b'name'].decode('utf-8'),
        self.metaInfo[b'info'][b'length']))

    @property
    def announce(self):
        return self.metaInfo[b'announce'].decode('utf-8')

    @property
    def piece_length(self):
        return self.metaInfo[b'info'][b'piece length']
    
    @property
    def total_size(self):
        return self.files[0].length

    @property    
    def output_file(self):
        return self.files[0].filename

    @property
    def pieces(self):
        piecesData = self.metaInfo[b'info'][b'pieces']
        pieces = []
        offset = 0
        length = len(piecesData)
        while(offset < length) :
            pieces.append(piecesData[offset:offset+20])
            offset += 20
        return pieces        


        