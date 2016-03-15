import struct
import os

class Item:
    def __init__(self, name, size, position):
        self.name = name 
        self.size = size
        self.position = position

    def setPack(self, pack):
        self.pack = pack

    def getFileData(self):
        data = None
        with open(self.pack.pakPath, "rb") as fp:
            fp.seek(self.position, 0)
            data = fp.read(self.size)
        return data


class Pack:
    def __init__(self, pakPath):
        self.pakPath = pakPath
        self.items = {}
        self.loadPack()

    def loadPack(self):
        self.loadPackHeader()
        self.loadPackDir()

    def loadPackHeader(self):
        self.startOffset = 0
        self.numItems = 0
        with open(self.pakPath, "rb") as fp:
            magic = fp.read(4)
            dataOffset = fp.read(4)
            self.startOffset = struct.unpack("<l", dataOffset)[0]
            dataLength = fp.read(4)
            length = struct.unpack("<l", dataLength)[0]
            self.numItems = length / 64

    def loadPackDir(self):
        with open(self.pakPath, "rb") as fp:
            fp.seek(self.startOffset, 0)
            for _ in range(0, self.numItems):
                name = fp.read(56)
                dataPosition = fp.read(4)
                position = struct.unpack("<l", dataPosition)[0]
                dataSize = fp.read(4)
                size = struct.unpack("<l", dataSize)[0]
                self.addItem(name, size, position)

        
    def addItem(self, name, size, position):
        name = self.sanitizeString(name)
        item = Item(name, size, position)
        item.setPack(self)
        self.items[name] = item

        
    def saveFile(self, name, destPath):
        data = self.getFileData(name)
        filePath = os.path.join(destPath, name)
        dirPath = os.path.dirname(filePath)
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        with open(filePath, "wb") as fp:
            fp.write(data)
            
    def getFileData(self, name):
        item = self.items[name]
        data = None
        with open(self.pakPath, "rb") as fp:
            fp.seek(item.position, 0)
            data = fp.read(item.size)
        return data

    #implement  file = pack[filename]
    def __getitem__(self, key):
        if not key in self.items:
            raise KeyError
        return self.items[key]

    #implement filename in pack
    def __contains__(self, item):
        return item in self.items

    def sanitizeString(self, s):
        return ''.join(c for c in s if c.isalnum() or c == '.' or c =='/')

    @staticmethod
    def loadPacks(dirPath):
        packs = []
        i = 0
        while i >= 0:
            name = "PAK%s.PAK" % i
            if not os.path.isfile(os.path.join(dirPath, name)):
                break
            p = Pack(os.path.join(dirPath, name))
            packs.append(p)
            i += 1
        return packs
