#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                     California Institute of Technology
#                       (C) 2007  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Actor import Actor


class Samples(Actor):


    class Inventory(Actor.Inventory):

        import time
        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier for a given search"
        
        page = pyre.inventory.str('page', default='empty')

        pass # end of Inventory


    def default(self, director):
        page = director.retrievePage( 'samples' )
        if not page:
            return director.retrievePage("authentication-error")
        
        main = page._body._content._main
        
        # populate the main column
        document = main.document(title='Samples')
        document.description = (
            'Samples page displays a list of samples.'
            )
        document.byline = 'byline?'

        id = self.inventory.id
        if id is None: id = 'empty'

        samples = self._getsamples( id )

        if len(samples.elements()) == 0:
            noscatterer( document, director )
        else:
            listscatterers( samples.elements(), document, director )
            pass
    
        return page    
    
    
    
#    def perform(self, app, routine=None):
#        page = app.retrievePage(self.inventory.page)
#        return page


    def __init__(self, name=None):
        if name is None:
            name = "purser"
        super(Samples, self).__init__(name)
        return


    def _getsamples(self, id):
        path = self._getpath( id )
        from sampleassembly.saxml import parse_file
        samples = parse_file( path )
        return samples


    def _getpath(self, id):
        import os
        return os.path.join('db', 'samples', '%s.xml' % id )


    pass # end of Samples


def listscatterers( scatterers, document, director ):
    p = document.paragraph()

    n = len(scatterers)
    p.text = [ 'There are no samples yet.']
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
