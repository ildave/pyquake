import struct
import com

class WadItem:
    def __init__(self, name, size, filetype, start):
            self.name = name
            self.size = size
            self.filetype = filetype
            self.start = start
    
    def setWad(self, wad):
        self.wad = wad
        
    def getFileData(self):
        return self.wad.getFileData(self.name)
    
    

class Wad:
    def __init__(self, wadFile):
        self.wadData = wadFile.getFileData()
        self.magic = self.wadData[0:4]
        self.numEntries = struct.unpack("<l", self.wadData[4]+self.wadData[5]+self.wadData[6]+self.wadData[7])[0]
        self.dirOffset = struct.unpack("<l", self.wadData[8]+self.wadData[9]+self.wadData[10]+self.wadData[11])[0]
        
        self.items = {}
        
        for i in range(0, self.numEntries):
            start = self.dirOffset + (i * 32)
            offset = struct.unpack("<l", self.wadData[start:start+4])[0]
            dsize = struct.unpack("<l", self.wadData[start+4:start+8])[0]
            size = struct.unpack("<l", self.wadData[start+8:start+12])[0]
            filetype = struct.unpack("<c", self.wadData[start+12])[0]
            compr = struct.unpack("<c", self.wadData[start+13])[0]
            dummy = struct.unpack("<h", self.wadData[start+14:start+16])[0]
            name = self.wadData[start+16:start+32]
            name = self.sanitizeString(name)

            item = WadItem(name, size, filetype, offset)
            item.setWad(self)
            self.items[name] = item
            
    def getFileData(self, name):
        item = self.items[name]
        return self.wadData[item.start:item.start+item.size]
    
    def getItem(self, name):
        return self.items[name]
    
    def sanitizeString(self, s):
        return ''.join(c for c in s if c.isalnum() or c == '.' or c =='/' or c == '_')
    
    @staticmethod
    def loadWad():
        wadFile =  com.findFile("gfx.wad")
        wad = Wad(wadFile)
        return wad