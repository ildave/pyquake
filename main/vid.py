import pygame
import struct
import common
RED = (255, 0, 0)
WHITE = (255, 255, 255)
size = (common.WIDTH, common.HEIGTH)

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
        if x + w > (common.WIDTH - 1):
            x = 0
            y = y + h 
    del pixels 
    
def loadImageData(item):
    data = item.getFileData()
    width = struct.unpack("<l", data[0]+data[1]+data[2]+data[3])[0]
    height = struct.unpack("<l", data[4]+data[5]+data[6]+data[7])[0]
    print "w, h: %s %s" % (width, height)
    return data[8:], width, height
    
def drawImage(item, xpos, ypos):
    data, width, height = loadImageData(item)
    pixels = pygame.PixelArray(common.SCREEN)
    x = xpos
    y = ypos
    for b in data:
        paletteIndex = struct.unpack("<B", b)[0]
        if paletteIndex != 255:  ###transparent pixel
            color = common.PALETTE[paletteIndex]
            pixels[x][y] = color
        x = x + 1
        if x > (width + xpos) - 1:
            x = xpos
            y = y + 1
    del pixels
    
            
def loadPalette(paletteFile):
    palette = []
    data = paletteFile.getFileData()
    for i in range(0, len(data), 3):
        r = struct.unpack("<B", data[i])[0]
        g = struct.unpack("<B", data[i + 1])[0]
        b = struct.unpack("<B", data[i + 2])[0]
        palette.insert(i / 3, (r, g, b))
    return palette
