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


from Actor import Actor, action_link, action, actionRequireAuthentication
from vnf.weaver import action_href
from PyHtmlTable import PyHtmlTable

class Sample(Actor):

    class Inventory(Actor.Inventory):

        import time
        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier for a given search"
        
        page = pyre.inventory.str('page', default='empty')

    def default(self, director):
        return self.listall( director )

    def listall(self, director):
        page = director.retrievePage( 'sample' )
        
        main = page._body._content._main
        
        # populate the main column
        document = main.document(title='List of samples')
        document.description = ''
        document.byline = 'byline?'

        # retrieve id:record dictionary from db
        clerk = director.clerk
        scatterers = clerk.indexScatterers(where='template=True').values()
        scatterers = [ clerk.getHierarchy(scatterer) for scatterer in scatterers]
        samples = scatterers
            
        p = document.paragraph()
        columns = ['short_description','matter.realmatter.chemical_formula', 'matter.realmatter.cartesian_lattice', 
                   'matter.realmatter.atom_symbols','matter.realmatter.fractional_coordinates', 
                   'shape.realshape.short_description', 'shape.realshape.height','shape.realshape.width',
                   'shape.realshape.thickness',]
#        columnTitles = ['Select for neutron experiment', 
        columnTitles = ['Sample description','Chemical formula', 'Cartesian lattice', 
                        'Atom symbols', 'Fractional coordinates', 'Shape description', 'Shape height', 'Shape width', 
                        'Shape thickness']

        t=PyHtmlTable(len(samples), len(columnTitles), {'width':'400','border':2,'bgcolor':'white'})
        for colNum, col in enumerate(columnTitles):
            t.setc(0,colNum,col)
#        for row in range(numSamples):
#            colNum=0
#            for name in samples[row].getColumnNames():
        for row, sample in enumerate( samples ):
            #first put in the radio button
#            selection = "<input type='radio' name='actor.form-received.kernel_id' value="+sample.id+" id='radio'/>"
#            t.setc(row+1, 0, selection)
            for colNum, col in enumerate( columns ):
                if col == 'short_description':
                    value = sample.getColumnValue(col)
#                    link = action_link(
#                        actionRequireAuthentication(
#                        'neutronexperimentwizard',
#                        director.sentry,
#                        label = value,
#                        routine = 'create_new_sample'
#                        ),  director.cgihome
#                        )
#                    value = link
                    t.setc(row+1,colNum+1,value)
                    continue
                else:
                    attrs=col.split('.')
                    try:
                        value = getattr(getattr(getattr(sample, attrs[0]),attrs[1]),attrs[2])
                    except:
                        value=''
                    t.setc(row+1,colNum,value)
        p.text = [t.return_html()]
        
        p = document.paragraph()
        p.text = [action_link(
        actionRequireAuthentication(
        'sampleInput', director.sentry,
        label = 'Add a new sample',
        routine = 'default'
        ),  director.cgihome),'<br>']

        return page  


    def __init__(self, name=None):
        if name is None:
            name = "sample"
        super(Sample, self).__init__(name)
        return

# version
__id__ = "$Id$"

# End of file 
