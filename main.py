import random
import asyncio
import sys
from torrent import Torrent
from tracker import Tracker

print("Name of torrent file: ", sys.argv[1])

torrent = Torrent(sys.argv[1])

print(torrent.output_file)
print(torrent.announce)
print(torrent.piece_length)
print(torrent.pieces[0])

peer_id = '-BT1010-' + ''.join([str(random.randint(0, 9)) for _ in range(12)])

tracker = Tracker(torrent)
response = asyncio.run(tracker.makeRequestToTracker(peer_id, 0, 0))

print(response.interval)
print(response.seeders)
print(response.leechers)
print(response.peers)


# file = open(filePath, "rb")
# obj = Decoder(file.read())
# metaInfoDict = obj.decode()
# print(metaInfoDict.keys())
# # print(metaInfoDict[b'announce'])
# # print(metaInfoDict[b'comment'])
# # print(metaInfoDict[b'created by'])
# # print(metaInfoDict[b'creation date'])
# infoDict = metaInfoDict[b'info']
# print(infoDict.keys())
# # print(infoDict[b'files'])
# # print(infoDict[b'length'])
# # print(type(infoDict[b'length']))
# # print(infoDict[b'name'])
# # print(infoDict[b'piece length'])
# # print(type(infoDict[b'piece length']))
# # print(type(infoDict[b'pieces']))
# # print(math.ceil(infoDict[b'length'] / infoDict[b'piece length']))
# encodeObj = Encoder(infoDict)
# infoHash = hashlib.sha1(encodeObj.encode()).digest()

# print("Hashed value length: {} and content: {}".format(len(infoHash), infoHash))
# announceString = (metaInfoDict[b'announce']).decode("utf-8")
# print(announceString)



# # Request to Tracker:
# paramsForTracker = urlencode({
#     'info_hash': infoHash,
#     'peer_id' : peer_id,
#     'uploaded': 0,
#     'downloaded': 0,
#     'left': infoDict[b'length'],
#     'port': PORT,
#     'compact': 1
# })

# print("Params sent to the tracker: ", paramsForTracker)

# reqForTrackers = requests.get(announceString, params=paramsForTracker)

# responseFromTracker = reqForTrackers.content
# trackerResponse = Decoder(responseFromTracker).decode()
# trackerReqInterval = trackerResponse[b'interval']

# peers = trackerResponse[b'peers']
# print(type(peers))

