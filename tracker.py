from urllib.parse import urlencode
from bencoding import Decoder
from collections import namedtuple
import socket
from struct import unpack
import aiohttp

Peer = namedtuple('Peer', ['address', 'port'])

class TrackerResponse:

    def __init__(self, response):
        self.response = response

    @property
    def interval(self):
        return self.response[b'interval']

    @property
    def seeders(self):
        return self.response[b'complete']

    @property
    def leechers(self):
        return self.response[b'incomplete']

    @property
    def peers(self):
        data = self.response[b'peers']
        return [Peer(socket.inet_ntoa(data[i:i+4]), _decode_port(data[i+4:i+6])) for i in range(0, len(data), 6)]

class Tracker:

    def __init__(self, torrent) : 
        self.torrent = torrent
        self.client = aiohttp.ClientSession()
        
    async def makeRequestToTracker(self,
                            peer_id,
                            downloaded,
                            uploaded) :
        
        params = {
            'info_hash': self.torrent.infoHash,
            'peer_id': peer_id,
            'uploaded': uploaded,
            'port': 6888,
            'downloaded': downloaded,
            'left': self.torrent.total_size - downloaded,
            'compact': 1
        }
        url = self.torrent.announce + '?' + urlencode(params)    
        print("Connecting to tracker at {}".format(url))
        
        async with self.client.get(url) as response:
            if not response.status == 200: 
                raise ConnectionError("Error connecting to tracker. Status code: {}".format(response.status))
            data = await response.read()
            return TrackerResponse(Decoder(data).decode())
        
    def close(self) :
        self.client.close()


def _decode_port(port):
    return unpack(">H", port)[0]