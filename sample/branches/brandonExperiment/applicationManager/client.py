from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientCreator

class Greeter(Protocol):
    
    def connectionMade(self):
        self.transport.write("Hello server, I am the client!\r\n")
        self.transport.loseConnection()
    
    def sendMessage(self, msg):
        self.transport.write("MESSAGE %s\n" % msg)
        
    def dataReceived(self, data):
        stdout.write(data)

def gotProtocol(p):
    p.sendMessage("Hello")
    reactor.callLater(1, p.sendMessage, "This is sent in a second")
    reactor.callLater(2, p.transport.loseConnection)

c = ClientCreator(reactor, Greeter)
c.connectTCP("localhost", 88007).addCallback(gotProtocol)