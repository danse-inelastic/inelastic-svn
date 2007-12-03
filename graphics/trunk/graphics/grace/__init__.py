__doc__ = '''Instructions for Pyre grace component:
Import the PyGrace class        >>> from graphics.grace import grace
Instantiate the PyGrace class   >>> gr = grace()
Get help                        >>> gr.doc()
'''

def grace():
    from PyGrace import PyGrace as PyGraceFactory
    return PyGraceFactory()

