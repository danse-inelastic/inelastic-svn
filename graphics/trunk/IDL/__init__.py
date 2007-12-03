__doc__='''Instructions for Pyre IDL component:
Import the IDL class            >>> from graphics.IDL import IDL
Instantiate the IDL class       >>> ri = IDL()
Get help                        >>> ri.doc()
'''
def IDL():
    from PyIDL import rsiIDL as IDLFactory
    return IDLFactory()
