import socket
import traceback
import re
import collections
import Settings

PORT = 60040            # Standard port for HS50

STX = b'\x02'
ETX = b'\x03'

# TODO: I think this needs to be a thread
class HS50 ():

    online = False
    socket = None
    inputList=[b"72", b"50", b"51", b"52", b"53", b"54", b"73", b"74", b"77"]

    def __init__(self, parent):
        # Init the connection
        host = Settings.Config.get("HS50","ip")
        if len(host):
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((host, PORT))
                self.socket.setblocking(False)
                self.online=True
            except:
                traceback.print_exc()
                self.socket = None
                self.online=False
                
        # Start a timer to get latest setting from HS50
        # self.timer = wx.Timer(self)
        # self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        # self.timer.Start(0.2e+3) # 0.2 second interval

    def OnDestroy (self, evt):
        # Cleanup Timer
        self.timer.Stop()
        
        # Let the event pass
        evt.Skip()
        
    def OnTimer (self, evt):
        self.message = b''
        try:
            if self.socket:
                self.message = self.socket.recv(200)
        except:
            pass
            
        # See if there are any incoming messages
        if len(self.message):
            #print (self.message)
            # Find the message of interest.  Discard anything before it.  Preserve everything after it
            r = re.search(STX + b"ABSC:([0-9]{2}):([0-9]{2}):([0-9]{1})" + ETX + b"(.*)", self.message)
            if r:
                bus, material, tally, self.message = r.groups()
                
                # Which radio button do we need to update?
                bus_radio = None
                if bus == b"02":
                    pass
                    # TODO
                    
        # Send the next request
        # b"02" = PGM
        c = STX + b"QBSC:" + b"02" + ETX
        try:
            if self.socket:
                self.socket.sendall(c)
        except:
            pass
        