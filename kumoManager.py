from AJArest import kumo

class kumoManager (kumo.Client):
    namesDst = ["%i" % x for x in range (17)]
    namesSrc = ["%i" % x for x in range (17)]
    online = False

    def __init__ (self, url, cacheRawParameters=True):
        try:
            kumo.Client.__init__(self,
                                url=url,
                                cacheRawParameters=cacheRawParameters)
            self.online = True
        except:
            self.online = False

    def getNames (self):
        if self.online:
            for i in range(1,17):
                # Get Destination Names
                name = "%3i: " % (i)
                name += self.getParameter('eParamID_XPT_Destination%i_Line_1' % (i))[1]
                name += ' '
                name += self.getParameter('eParamID_XPT_Destination%i_Line_2' % (i))[1]
                self.namesDst[i] = name

                # Get Source Name
                name = "%3s: " % (i)
                name += self.getParameter('eParamID_XPT_Source%s_Line_1' % (i))[1]
                name += ' '
                name += self.getParameter('eParamID_XPT_Source%s_Line_2' % (i))[1]
                self.namesSrc[i] = name

    def setChannel (self, destination, source):
        if self.online:
            return self.setParameter('eParamID_XPT_Destination%i_Status' %  int(destination) , str(source))

    def getChannel (self, destination):
        if self.online:
            return int(self.getParameter('eParamID_XPT_Destination%i_Status' % (i))[1])
