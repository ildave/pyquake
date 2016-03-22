import time
import host
import vid
import pak
import com
import common


def main():
    print "main"
    common.SCREEN = vid.vid_init()
    oldtime = time.time()
    common.PACKS = pak.Pack.loadPacks(common.PAK_PATH)    
    
#     for k in pack.items:
#         pack.saveFile(k, "/home/dave/quakefiles")
    
    paletteFile = com.findFile("gfx/palette.lmp")
    common.PALETTE = vid.loadPalette(paletteFile)
    #vid.drawPalette(screen, palette)
    item = com.findFile("gfx/menuplyr.lmp")
    vid.drawImage(item, 220, 100)
    while vid.run():
        newtime = time.time()
        host.host_frame(newtime - oldtime)
        oldtime = newtime
    
    
    
if __name__ == '__main__':
    print "start"
    main()