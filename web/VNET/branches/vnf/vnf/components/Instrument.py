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


from Actor import Actor, action_link, action, actionRequireAuthentication, AuthenticationError


class Instrument(Actor):


    class Inventory(Actor.Inventory):

        import time
        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier of the instrument"


        import vnf.inventory
        dataobject = vnf.inventory.dataobject(
            'dataobject', default='instrument' )
        dataobject.meta['tip'] = 'the data object to be edited'

        pass # end of Inventory



    def default(self, director):
        return self.listall( director )


    def listall(self, director):
        try:
            page = director.retrieveSecurePage( 'instrument' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main

        # populate the main column
        document = main.document(title='List of instruments')
        document.description = ''
        document.byline = 'byline?'

        # retrieve id:record dictionary from db
        clerk = director.clerk
        instruments = clerk.indexInstruments()
        
        listinstruments( instruments.values(), document, director )
        
        return page


    def edit(self, director):
        page, document = self._head( director )
        
        scribe = director.scribe

        # the record
        obj = self._getDataObjectRecord( director )

        # properties of the data object
        properties = self.inventory.dataobject.propertyNames( director )
        
        # create form
        instrument = self.instrument_record
        scribe.objectEditForm(
            document, obj, properties,
            instrument, 'instrument',
            director)

        return page    


    def set(self, director):
        page, document = self._head( director )
        
        obj = self._getDataObjectRecord( director )

        dataobject = self.inventory.dataobject

        for prop in dataobject.propertyNames( director ):
            setattr(
                obj, prop,
                dataobject.inventory.getTraitValue( prop ) )
            continue

        director.clerk.updateRecord( obj )
        
        return page


    def run(self, director):
        page, document = self._head( director )
        return page


    def __init__(self, name=None):
        if name is None:
            name = "instrument"
        super(Instrument, self).__init__(name)
        return


    def _head(self, director):
        try:
            page = director.retrieveSecurePage( 'instrument' )
        except AuthenticationError, error:
            return error.page
        
        main = page._body._content._main

        # the record we are working on
        id = self.inventory.id
        self.instrument_record = instrument = self._getinstrument( id, director )

        # populate the main column
        document = main.document(title='Instrument: %s' % instrument.short_description )
        document.description = (
            'Instrument is a collection of neutron components. For example, '\
            'it can consist of a neutron source, a sample, and a detector system.\n'\
            )
        document.byline = '<a href="http://danse.us">DANSE</a>'

        from TreeViewCreator import create as create_treeview
        treeview = create_treeview(
            director.clerk.getHierarchy(instrument),
            'instrument',
            director)
        document.contents.append(  treeview )
        return page, document


    def _getDataObjectRecord(self, director):
        return self.inventory.dataobject.getRecord( director )
    

    def _getinstrument(self, id, director):
        clerk = director.clerk
        return clerk.getInstrument( id )


    def _configure(self):
        Actor._configure(self)
        self.id = self.inventory.id
        dataobject = self.dataobject = self.inventory.dataobject
        if dataobject.name == 'instrument':
            dataobject.inventory.id = self.id
            pass
        return


    pass # end of Instrument



from wording import plural, present_be

def listinstruments( instruments, document, director ):
    p = document.paragraph()

    n = len(instruments)

    p.text = [ 'There %s %s instrument%s: ' %
               (present_be(n), n, plural(n))
                ]

    from inventorylist import list
    list( instruments, document, 'instrument', director )
    return



# version
__id__ = "$Id$"

# End of file 
