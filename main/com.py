 def findFile(name, packs):
 	for pack in packs:
 		if name in pack:
 			return pack[name]
 	return None