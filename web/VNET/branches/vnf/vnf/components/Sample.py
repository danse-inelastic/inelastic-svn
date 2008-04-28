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
        samples = clerk.getSamples()
            
        p = document.paragraph()
        numSamples = len(samples)
        columns = ['Sample', 'Material','Shape']        
#        columns = ['Sample Name', 'Texture','Creator','Date Created','Id']
#        matterColumns=['Matter Description','Cartesian Lattice','Atom Positions']
#        shapeColumns=['Shape Description','Cartesian Lattice','Atom Positions']
        numColumns=len(columns)#scatteringKernels[0].getNumColumns()

        from PyHtmlTable import PyHtmlTable
        t=PyHtmlTable(numSamples,numColumns, {'width':'400','border':2,'bgcolor':'white'})
        for colNum, col in enumerate(columns):
            t.setc(0,colNum,col)
#        for row in range(numSamples):
#            colNum=0
#            for name in samples[row].getColumnNames():
        for row, job in enumerate( samples ):
            for colNum, colName in enumerate( columns ):
                
                value = job.getColumnValue(colName)
                if colName == 'Sample':
                    link = action_link(
                        actionRequireAuthentication(
                        'sample',
                        director.sentry,
                        label = value,
                        routine = 'sampleInput',
                        id = job.id,
                        ),  director.cgihome
                        )
                    value = link
                
                
                t.setc(row,colNum,samples[row].getColumnValue(name))
                colNum+=1
        p.text = [t.return_html()]
        
        p = document.paragraph()
        p.text = [action_link(
        actionRequireAuthentication(
        'materialInput', director.sentry,
        label = 'Add a new type of material'),  director.cgihome
        ),
        '<br>',
        action_link(
        actionRequireAuthentication(
        'shapeInput', director.sentry,
        label = 'Add a new sample shape'),  director.cgihome
        )]

        return page  


    def __init__(self, name=None):
        if name is None:
            name = "sample"
        super(Sample, self).__init__(name)
        return

# version
__id__ = "$Id$"

# End of file 
