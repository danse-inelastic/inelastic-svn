#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2007  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Actor import Actor


class SampleAssemblyBuilder(Actor):


    class Inventory(Actor.Inventory):

        import time
        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier for a given search"

        pass # end of Inventory


    def default(self, director):
        page = director.retrieveSecurePage( 'sampleassembly' )
        if not page:
            return director.retrievePage("authentication-error")
        
        main = page._body._content._main
        
        # populate the main column
        document = main.document(title='Sample Assembly Builder')
        document.description = (
            'Sample assembly is a collection of neutron scatterers. For example, '\
            'it can consist of a main sample, a sample container, and a furnace.\n'\
            )
        document.byline = 'byline?'

        id = self.inventory.id
        if id is None: id = 'empty'

        sampleassembly = self._getsampleassembly( id )

        if len(sampleassembly.elements()) == 0:
            noscatterer( document, director )
        else:
            listscatterers( sampleassembly.elements(), document, director )
            pass
    
        return page    


    def __init__(self, name=None):
        if name is None:
            name = "purser"
        super(SampleAssemblyBuilder, self).__init__(name)
        return


    def _getsampleassembly(self, id):
        path = self._getpath( id )
        from sampleassembly.saxml import parse_file
        sampleassembly = parse_file( path )
        return sampleassembly


    def _getpath(self, id):
        import os
        return os.path.join( 'sampleassemblies', '%s.xml' % id )


    pass # end of SampleAssemblyBuilder


def listscatterers( scatterers, document, director ):
    p = document.paragraph()

    n = len(scatterers)
    p.text = [ 'There %s %s scatterer%s in this sample assembly: ' %
               (present_be(n), n, plural(n))
                ]
    formatstr = '%(index)s: %(name)s (<a href="%(cgihome)s?actor=scatterer&scatterer.name=%(name)s">configure</a>)'

    for i, scatterer in enumerate( scatterers ):
        p = document.paragraph()
        p.text += [
            formatstr % {'name': scatterer.name,
                         'cgihome': director.cgihome,
                         'index': i+1}
            ]
        continue
    return


def present_be( n ):
    if n > 1: return 'are'
    return 'is'

def plural( n ):
    if n>1: return 's'
    return ''


def noscatterer( document, director ):
    p = document.paragraph()
    p.text = [
        "There is no scatterer in this sample assembly. ",
        'Please <a href="%s?actor=addscatterer">add</a> a scatter.' % (
        director.cgihome,)
        ]
    return


# version
__id__ = "$Id$"

# End of file 
