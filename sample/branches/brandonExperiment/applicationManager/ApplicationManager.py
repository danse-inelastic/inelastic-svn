from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver

class ApplicationManager(LineReceiver):

    def connectionMade(self):
        print 'connection made'
        #self.factory.numProtocols = self.factory.numProtocols+1 

    def connectionLost(self, reason):
        print 'Lost connection'
        #self.factory.numProtocols = self.factory.numProtocols-1
        
    apps = {'How are you?': 'Fine', None : "I don't know what you mean"}

    def lineReceived(self, line):
        print line
        
        
        
#        self.apps
#        if self.apps.has_key(line):
#            self.sendLine(self.apps[line])
#        else:
#            self.sendLine(self.answers[None])
            
            

#    def dataReceived(self, data):
#        if 
#        self.transport.write(data)



# Next lines are magic:
factory = Factory()
factory.protocol = ApplicationManager

# 8007 is the port you want to run under. Choose something >1024
reactor.listenTCP(88007, factory)
reactor.run()












