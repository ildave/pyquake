import pygame
import struct

RED = (255, 0, 0)
WHITE = (255, 255, 255)
size = (640, 480)

isRunning = True

def run():
    return isRunning

def vid_init():
    print "vid_init"
    pygame.init()
    screen = pygame.display.set_mode(size)
    screen.fill(WHITE)
    return screen

def vid_update():
    pygame.display.update() 

def manage_events():
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            print "QUIT"
            global isRunning
            isRunning = False
            
def drawPalette(screen, palette):
    pixels = pygame.PixelArray(screen)
    w = 30
    h = 30
    x = 0
    y = 0
    for c in palette:
        print "x: %s" % x 
        print "y: %s" % y
        print "draw %s, %s, %s" % c
        for i in range(x, w + x):
            for j in range(y, h + y):
                print "%s_%s" % (i, j)
                pixels[i][j] = c 
        x = x + w 
        if x + w > 639:
            x = 0
            y = y + h 
    del pixels 
    
def loadImageData(name, pack):
    data = pack.getFileData(name)
    width = struct.unpack("<l", data[0]+data[1]+data[2]+data[3])[0]
    height = struct.unpack("<l", data[4]+data[5]+data[6]+data[7])[0]
    return data[8:], width, height
    
def drawImage(screen, palette, name, pack, xpos, ypos):
    data, width, height = loadImageData(name, pack)
    pixels = pygame.PixelArray(screen)
    x = xpos
    y = ypos
    for b in data:
        paletteIndex = struct.unpack("<B", b)[0]
        color = palette[paletteIndex]
        pixels[x][y] = color
        x = x + 1
        if x > (width + xpos) - 1:
            x = xpos
            y = y + 1
    del pixels
    
            
def loadPalette(pack):
    palette = []
    data = pack.getFileData("gfx/palette.lmp")
    for i in range(0, len(data), 3):
        r = struct.unpack("<B", data[i])[0]
        g = struct.unpack("<B", data[i + 1])[0]
        b = struct.unpack("<B", data[i + 2])[0]
        palette.insert(i / 3, (r, g, b))
    return palette
