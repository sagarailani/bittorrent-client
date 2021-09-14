import asyncio
import sys
from torrent import Torrent
from client import Client

print("Name of torrent file: ", sys.argv[1])

torrent = Torrent(sys.argv[1])
client = Client(torrent)

loop = asyncio.get_event_loop()
task = loop.create_task(client.start())

loop.run_until_complete(task)

