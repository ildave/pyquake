import vid

realtime = 0
old_realtime = 0
host_frametime = 0

def host_filtertime(t):
    global realtime
    global old_realtime
    global host_frametime
    realtime += t 
    if (realtime - old_realtime < (1.0 / 72)):
        return False
    host_frametime = realtime - old_realtime
    old_realtime = realtime
    
    return True

def host_frame(t):
    if not host_filtertime(t):
        return
    
    vid.manage_events()
    vid.vid_update()
    