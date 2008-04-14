#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                     California Institute of Technology
#                       (C) 2007  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Actor import Actor, action_link, action, actionRequireAuthentication


class ScatteringKernel(Actor):

    class Inventory(Actor.Inventory):

        import time
        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier for a given search"
        
        page = pyre.inventory.str('page', default='empty')

    def default(self, director):
        return self.listall( director )

    def listall(self, director):
        page = director.retrievePage('scatteringKernel')
        
        main = page._body._content._main
        
        # populate the main column
        document = main.document(title='List of scattering kernels')
        document.description = ''
        document.byline = 'byline?'

        # retrieve id:record dictionary from db
        clerk = director.clerk
        scatteringKernels = clerk.getScatteringKernels()
        scatteringKernelValues=[]
        for scatteringKernel in scatteringKernels:
            scatteringKernelValues.append(scatteringKernel.getValues())
            
        p = document.paragraph()
        numScatteringKernels = len(scatteringKernels)
        numColumns=scatteringKernels[0].getNumColumns()

        from PyHtmlTable import PyHtmlTable
        t=PyHtmlTable(numScatteringKernels,numColumns)#, {'width':'400','border':2,'bgcolor':'white'})
        for row in range(numScatteringKernels):
            colNum=0
            for name in scatteringKernels[row].getColumnNames():
                t.setc(row,colNum,scatteringKernels[row].getColumnValue(name))
                colNum+=1
        p.text = [t.return_html()]
        
        p = document.paragraph()
        p.text = [action_link(
        actionRequireAuthentication(
        'scatteringKernelInput', director.sentry,
        label = 'Add a new scattering kernel'),  director.cgihome
        ),
        '<br>']
        
        return page          



    def __init__(self, name=None):
        if name is None:
            name = "scatteringKernel"
        super(ScatteringKernel, self).__init__(name)
        return








# version
__id__ = "$Id$"

# End of file 
