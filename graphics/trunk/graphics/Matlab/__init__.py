__doc__ = '''Instructions for Pyre Matlab component:
Import the IDL class            >>> from graphics.Matlab import Matlab
Instantiate the IDL class       >>> ml = Matlab()
Get help                        >>> ml.help()
'''
def Matlab():
    from Matlab import Matlab as MatlabFactory
    return MatlabFactory()
