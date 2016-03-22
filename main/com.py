import common

def findFile(name):
    print name
    for pack in common.PACKS:
        print pack.pakPath
        if name in pack:
            return pack[name]
        return None