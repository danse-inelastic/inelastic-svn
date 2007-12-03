
# Copyright (c) 2001-2004 Twisted Matrix Laboratories.
# See LICENSE for details.


from twisted.internet import reactor, protocol


class Echo(protocol.Protocol):
    """This is just about the simplest possible protocol"""
    
    def dataReceived(self, data):
        # check to see what application is needed, then launch a new client
        words = data.split()
        if words[0]=='deploy-graphics':
            self.transport.write('graphics deploying')
            import os
            os.spawnl('cd /home/jbk/DANSE/graphics; python graphics/MainPlotWindow.py; cd -')
        else:  
            # this is if you want to write data to the client    
            self.transport.write(data)


def main():
    """This runs the protocol on port 8000"""
    factory = protocol.ServerFactory()
    factory.protocol = Echo
    reactor.listenTCP(8000,factory)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
