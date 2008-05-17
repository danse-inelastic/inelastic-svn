# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Brandon Keith
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def renderCif( sample ):
    from CifRenderer import CifRenderer
    return CifRenderer().render( sample )


def weaveCif( sample, stream = None):
    cif = renderCif( sample )
    if stream is None:
        import sys
        stream = sys.stdout
    stream.write( '%s' % cif )
    return


# version
__id__ = "$Id$"

# End of file
