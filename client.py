import asyncio
from tracker import Tracker
from asyncio import Queue
import time
import random

class Client:

    def __init__(self, torrent):
        self.torrent = torrent
        # Initialize tracker 
        self.tracker = Tracker(torrent)
        
        # Initialize peers
        # This is an asyncio queue because I think as multiple workers are running and accessing this queue at the same time
        # They might run into a deadlock situation, so this abstraction provides some protection against it.
        # But, these are not threads so, I don't understand how a deadlock might occur, or why we need this abstraction. 
        self.available_peers = Queue()

        # Initalize PeerConnections which can be used to connect to peers returned by Tracker
        # Also called workers. 
        # Here they will be just co-routines, so we can spawn a good amount of them without any performance related issues
        # They are not processes or threads. They are just small co-routines who will run inside the event loop and give return
        # back once their non-blocking work is done, and once they are blocked by a result from the peer, they return control back
        # to main event loop. 
        self.peerConnections = []

        # Flag to flip if client needs to be terminated
        self.abort = False
        

    # This start code is responsible for initializing the tracker and making a request to it once the interval time period expires
    # It again refreshes the available_peer queue by dumping already present peers inside the queue and adding new ones.

    async def start(self):

        previous = None
        interval = 0

        while True:

            if self.abort:
                print("Aborting download")
                break
        
            current = time.time()
            
            if (not previous) or ((previous + interval) < current) :
                print("Making request to tracker at time: {}".format(current))
                trackerResponse = await self.tracker.makeRequestToTracker(self.peer_id(), 0, 0) 

                if trackerResponse:
                    print("Interval for tracker requests: {}".format(trackerResponse.interval))
                    previous = current
                    self._delete_peers_from_queue()
                    interval = trackerResponse.interval
                    for peer in trackerResponse.peers:
                        self.available_peers.put_nowait(peer)    
                    print("Available peers: ")
                    print(self.available_peers)
            else :
                await asyncio.sleep(5)
        
        self.close()

    def _delete_peers_from_queue(self):
        while not self.available_peers.empty():
            self.available_peers.get_nowait()
        
    def close(self):
        self.abort = True
        self.tracker.close()
    
    def peer_id(self):
        return '-BT1010-' + ''.join([str(random.randint(0, 9)) for _ in range(12)])
