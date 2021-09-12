import json
import requests
import random
import math
import hashlib
from bencoding import Decoder, Encoder
from urllib.parse import urlencode

PORT = 6888

filePath = '/Users/sagarailani/Projects/bittorrent-client/sample.torrent'
# obj = Decoder(b'l4:eggsi5ei-1e5:sagari1234556e3:ande')s
# obj = Decoder(b'd4:spaM2:as2:asi5e4:listli3e4:spamli199ed2:ab3:cde3:fgili3ei10eeeee')
# print(obj.decode())

file = open(filePath, "rb")
obj = Decoder(file.read())
metaInfoDict = obj.decode()
print(metaInfoDict.keys())
# print(metaInfoDict[b'announce'])
# print(metaInfoDict[b'comment'])
# print(metaInfoDict[b'created by'])
# print(metaInfoDict[b'creation date'])
infoDict = metaInfoDict[b'info']
print(infoDict.keys())
# print(infoDict[b'files'])
# print(infoDict[b'length'])
# print(type(infoDict[b'length']))
# print(infoDict[b'name'])
# print(infoDict[b'piece length'])
# print(type(infoDict[b'piece length']))
# print(type(infoDict[b'pieces']))
# print(math.ceil(infoDict[b'length'] / infoDict[b'piece length']))
encodeObj = Encoder(infoDict)
infoHash = hashlib.sha1(encodeObj.encode()).digest()

print("Hashed value length: {} and content: {}".format(len(infoHash), infoHash))
announceString = (metaInfoDict[b'announce']).decode("utf-8")
print(announceString)

peer_id = '-BT1010-' + ''.join([str(random.randint(0, 9)) for _ in range(12)])

# Request to Tracker:
paramsForTracker = urlencode({
    'info_hash': infoHash,
    'peer_id' : peer_id,
    'uploaded': 0,
    'downloaded': 0,
    'left': infoDict[b'length'],
    'port': PORT,
    'compact': 1
})

print("Params sent to the tracker: ", paramsForTracker)

reqForTrackers = requests.get(announceString, params=paramsForTracker)

responseFromTracker = reqForTrackers.content
trackerResponse = Decoder(responseFromTracker).decode()
trackerReqInterval = trackerResponse[b'interval']

peers = trackerResponse[b'peers']
print(type(peers))

