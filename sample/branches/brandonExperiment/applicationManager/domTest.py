        
#from xml.dom.ext.reader import Sax2
#from xml.dom import EMPTY_NAMESPACE

import xml.dom.minidom
from xml.dom.minidom import Node
         
doc = xml.dom.minidom.parse(file('appRequest2.xml'))
#reader = Sax2.Reader()
#doc = reader.fromStream(open('addressbook.xml'))

ndata=[]
         
for node in doc.getElementsByTagName("app"):
    for node2 in node.childNodes:
        print 'name:',node2.nodeName
        print 'value:',node2.nodeValue
        try:
            print 'data:',node2.data
        except:
            print 'no data'
    print node.parentNode.nodeName
    print node.parentNode.nodeValue
    name = node.getElemetsByTagName('name') 
    print name.nodeValue 
    data = node.getElementsByTagName("data")
    for node2 in data:
        ndata.append(node2.data)
      
print ndata


