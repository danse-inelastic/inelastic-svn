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
        sampleValues=[]
        for sample in samples:
            sampleValues.append(sample.getValues())
            
        p = document.paragraph()
        numSamples = len(samples)
        numColumns=samples[0].getNumColumns()

        from PyHtmlTable import PyHtmlTable
        t=PyHtmlTable(numSamples,numColumns)#, {'width':'400','border':2,'bgcolor':'white'})
        for row in range(numSamples):
            colNum=0
            for name in samples[row].getColumnNames():
                t.setc(row,colNum,samples[row].getColumnValue(name))
                colNum+=1
        p.text = [t.return_html()]
        
        p = document.paragraph()
        p.text = [
        '''<strong>Note</strong>: would like to modify material and/or construct overall sample shape here.  
It may be advisable to reuse DANSE Python code by Python/Jython 
Web Start (http://personalpages.tds.net/~kent37/Python/JythonWebStart.html)'''
        ]
        
        return page  


    def __init__(self, name=None):
        if name is None:
            name = "sample"
        super(Sample, self).__init__(name)
        return

# version
__id__ = "$Id$"

# End of file 
