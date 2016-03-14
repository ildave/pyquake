import time
import host
import vid
import pak

PAK_PATH = "/home/dave/PAK0.PAK"

def shutdown():
    global isRunning
    isRunning = False

def main():
    print "main"
    screen = vid.vid_init()
    oldtime = time.time()
    pack = pak.Pack(PAK_PATH)
    
    
#     for k in pack.items:
#         pack.saveFile(k, "/home/dave/quakefiles")

    palette = vid.loadPalette(pack)
    #vid.drawPalette(screen, palette)
    vid.drawImage(screen, palette, "gfx/loading.lmp", pack, 220, 100)
    while vid.run():
        newtime = time.time()
        host.host_frame(newtime - oldtime)
        oldtime = newtime
    
    
    
if __name__ == '__main__':
    print "start"
    main()