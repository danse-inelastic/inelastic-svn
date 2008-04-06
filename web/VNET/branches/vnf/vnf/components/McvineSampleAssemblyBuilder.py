# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class Builder:

    sampleassemblyxmlfilename = 'sampleassembly.xml'

    def render(self, sampleassembly):
        from SampleAssemblyXMLBuilder import Builder
        contents = Builder().render(sampleassembly)
        return [ (self.sampleassemblyxmlfilename, contents) ]


    pass # Builder


# version
__id__ = "$Id$"

# End of file 
