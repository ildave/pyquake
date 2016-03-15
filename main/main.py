import time
import host
import vid
import pak
import com

PAK_PATH = "/home/dave/PAK0.PAK"

def shutdown():
    global isRunning
    isRunning = False

def main():
    print "main"
    screen = vid.vid_init()
    oldtime = time.time()
    packs = pak.Pack.loadPacks("/home/dave")

    pack = pak.Pack(PAK_PATH)
    
    
#     for k in pack.items:
#         pack.saveFile(k, "/home/dave/quakefiles")
    
    paletteFile = com.findFile("gfx/palette.lmp", packs)
    palette = vid.loadPalette(paletteFile)
    #vid.drawPalette(screen, palette)
    item = com.findFile("gfx/loading.lmp", packs)
    vid.drawImage(screen, palette, item, 220, 100)
    while vid.run():
        newtime = time.time()
        host.host_frame(newtime - oldtime)
        oldtime = newtime
    
    
    
if __name__ == '__main__':
    print "start"
    main()