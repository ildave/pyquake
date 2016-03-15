def findFile(name, packs):
    print name
    for pack in packs:
        print pack.pakPath
        if name in pack:
            return pack[name]
        return None