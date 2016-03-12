import struct
import os
import re

class Item:
    def __init__(self, name, size, position):
        self.name = name 
        self.size = size
        self.position = position

class Pack:
    def __init__(self, numItems, pakPath):
        self.numItems = numItems
        self.pakPath = pakPath
        self.items = {}
        
    def addItem(self, name, size, position):
        name = sanitizeString(name)
        item = Item(name, size, position)
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

def loadPackHeader(path):
    offset = 0
    numItems = 0
    with open(path, "rb") as fp:
        magic = fp.read(4)
        dataOffset = fp.read(4)
        offset = struct.unpack("<l", dataOffset)[0]
        dataLength = fp.read(4)
        length = struct.unpack("<l", dataLength)[0]
        numItems = length / 64
    return (offset, numItems)
        
def loadPackDir(path, offset, numItems):
    pack = Pack(numItems, path)
    with open(path, "rb") as fp:
        fp.seek(offset, 0)
        for _ in range(0, numItems):
            name = fp.read(56)
            dataPosition = fp.read(4)
            position = struct.unpack("<l", dataPosition)[0]
            dataSize = fp.read(4)
            size = struct.unpack("<l", dataSize)[0]
            pack.addItem(name, size, position)
    return pack
    
def loadPack(path):
    offset, numItems = loadPackHeader(path)
    pack = loadPackDir(path, offset, numItems)
    return pack

def sanitizeString(s):
    return ''.join(c for c in s if c.isalnum() or c == '.' or c =='/')