from typing import Dict, OrderedDict


TOKEN_INT = b'i'
TOKEN_LIST = b'l'
TOKEN_DICT = b'd'
TOKEN_END = b'e'
TOKEN_STR_SEPARATOR = b':'
TOKEN_INT_BYTES = b'01234567899';

class Decoder:

    def __init__(self, data) -> None:
        if not isinstance(data, bytes):
            raise TypeError('Argument "data" must be of type bytes')
        self._data = data
        self._index = 0

    def decode(self):
        token = self._peek()
        # print("Running decode fun for {}", token)
        if token == TOKEN_INT:
            self._consume()
            return self._decode_int()
        elif token == TOKEN_LIST:
            self._consume()
            return self._decode_list()
        elif token == TOKEN_DICT:
            self._consume()
            return self._decode_dict()
        elif token == TOKEN_END:
            return None
        elif token in TOKEN_INT_BYTES:
            return self._decode_str()
        else:
            pass

    def _decode_int(self):
        # print("Decoding int")
        return int(self._read_until(TOKEN_END))

    def _decode_str(self):
        # print("Decoding str")
        bytesToRead = int(self._read_until(TOKEN_STR_SEPARATOR))
        val = self._data[self._index:self._index+bytesToRead]
        # print("Updating index from {} to {} after reading string".format(self._index, self._index + bytesToRead))
        self._index +=  bytesToRead
        # print("Updating index to ", self._index)
        return val

    def _decode_list(self):
        # print("Decoding list")
        elementsOflist = []
        while(self._peek() != None and self._peek() != TOKEN_END):
            elementsOflist.append(self.decode())
            # print("Printing list uptill now", elementsOflist)
        self._consume()
        return elementsOflist

    def _decode_dict(self):
        # print("Decoding dict")
        nextToken = self._peek()
        if nextToken == None:
            return {}
        if nextToken not in TOKEN_INT_BYTES:
            raise TypeError('Keys in dictionary should be of type "str"')
        dictOfElements = {}
        while (self._peek() != TOKEN_END and self._peek() != None):        
            # print("current self.peek inside dict is : ", self._peek())
            key = self.decode()
            value = self.decode()
            dictOfElements[key] = value
            # print("Dict uptill now: ",dictOfElements)
        self._consume()
        return dictOfElements

    def _peek(self):
        if((self._index + 1) >= len(self._data)):
            return None
        # print("Peeked: ", self._data[self._index:self._index+1])
        return self._data[self._index:self._index+1]

    def _read_until(self, TOKEN):
        occurrence = self._data.index(TOKEN, self._index)
        # print("Found {} token at position {}".format(TOKEN, occurrence))
        result = self._data[self._index:occurrence]
        self._index = occurrence + 1
        # print("Updating position to {}".format(self._index))
        return result

    def _consume(self):
        # print("Consuming at index: ", self._index)
        self._index += 1 

class Encoder:

    def __init__(self, data) -> None:
        self._data = data

    def encode(self):
        return self._encode_element(self._data)

    def _encode_element(self, data):
        if isinstance(data, dict):
            return self._encode_dict(data)
        elif isinstance(data, int):
            return self._encode_int(data)
        elif isinstance(data, str):
            return self._encode_str(data)
        elif isinstance(data, list):
            return self._encode_list(data)
        elif isinstance(data, bytes):
            return self._encode_bytes(data)
        else: 
            pass
        
    def _encode_int(self, data):
        return str.encode('i' + str(data) + 'e')

    def _encode_str(self, data):
        return str.encode(str(len(data)) + ':' + data)

    def _encode_list(self, data):
        encodedListElements = b''
        for item in data:
            encodedListElements += self._encode_element(item)
        return b'l' + encodedListElements + b'e'

    def _encode_dict(self, data):
        encodedDict = b''
        for key in data.keys():    
            encodedDict += self._encode_element(key) + self._encode_element(data[key])
        return b'd' + encodedDict + b'e'
    
    def _encode_bytes(self, data: str):
        encodedBytes = bytearray()
        encodedBytes += str.encode(str(len(data)))
        encodedBytes += b':'
        encodedBytes += data
        return encodedBytes
        
        
        