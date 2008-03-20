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
        
        page = pyre.inventory.str('page', default='empty')

        pass # end of Inventory



    def default(self, director):
        return self.listall( director )


    def listall(self, director):
        page = director.retrieveSecurePage( 'sampleassembly' )
        if not page:
            return director.retrievePage("authentication-error")
        
        main = page._body._content._main
        
        # populate the main column
        document = main.document(title='List of sample assemblies')
        document.description = ''
        document.byline = 'byline?'

        # retrieve id:record dictionary from db
        clerk = director.clerk
        sampleassemblies = clerk.indexSampleAssemblies()
        
        listsampleassemblies( sampleassemblies.values(), document, director )
        
        return page


    def edit(self, director):
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

        sampleassembly = self._getsampleassembly( id, director )
        scatterers = self._getscatterers( id, director )

        if len(scatterers) == 0:
            noscatterer( document, director )
        else:
            listscatterers( scatterers, document, director )
            pass
    
        return page    


    def __init__(self, name=None):
        if name is None:
            name = "sampleassembly"
        super(SampleAssemblyBuilder, self).__init__(name)
        return


    def _getsampleassembly(self, id, director):
        clerk = director.clerk
        return clerk.getSampleAssembly( id )


    def _getscatterers(self, id, director):
        clerk = director.clerk
        return clerk.getScatterers( id )


    pass # end of SampleAssemblyBuilder



def action_link( director, text, kwds):
    return '<a href="%s?%s">%s</a>' % (
        director.cgihome,
        '&'.join( ['%s=%s' % (k,v) for k,v in kwds.iteritems() ] ),
        text )
    

def listscatterers( scatterers, document, director ):
    p = document.paragraph()

    n = len(scatterers)
    p.text = [ 'There %s %s scatterer%s in this sample assembly: ' %
               (present_be(n), n, plural(n))
                ]
    formatstr = '%(index)s: %(name)s (%(link)s)'

    for i, scatterer in enumerate( scatterers ):
        p = document.paragraph()
        # link of callback
        link = action_link(
            director, 'configure',
            { 'actor': 'scatterer',
              'scatterer.id': scatterer.id,
              'sentry.username': director.sentry.username,
              'sentry.ticket': director.sentry.ticket,
              }
            )
        p.text += [
            formatstr % {'name': scatterer.short_description,
                         'link': link,
                         'index': i+1}
            ]
        continue
    return


def listsampleassemblies( sampleassemblies, document, director ):
    p = document.paragraph()

    n = len(sampleassemblies)
    p.text = [ 'There %s %s sampleassembl%s: ' %
               (present_be(n), n, plural(n, 'y'))
                ]
    formatstr = '%(index)s: %(name)s (%(link)s)'

    for i, sampleassembly in enumerate( sampleassemblies ):
        
        p = document.paragraph()
        
        # link of callback
        link = action_link(
            director, 'configure',
            { 'actor': 'sampleassembly',
              'routine': 'edit',
              'sampleassembly.id': sampleassembly.id,
              'sentry.username': director.sentry.username,
              'sentry.ticket': director.sentry.ticket,
              }
            )
        p.text += [
            formatstr % {'name': sampleassembly.short_description,
                         'link': link,
                         'index': i+1}
            ]
        continue
    return



def present_be( n ):
    if n > 1: return 'are'
    return 'is'


def plural1( n ):
    if n>1: return 's'
    return ''

def plural2( n ):
    if n>1: return 'ies'
    return 'y'

def plural( n, ending = '' ):
    f = { '': plural1,
          'y': plural2,
        }
    return f[ending](n)


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
