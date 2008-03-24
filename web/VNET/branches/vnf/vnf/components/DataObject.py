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


from pyre.components.Component import Component


class DataObject(Component):


    class Inventory(Component.Inventory):

        import pyre.inventory

        id = pyre.inventory.str( 'id', default = '' )

        creater = pyre.inventory.str(name='creater', default = '')

        date = pyre.inventory.str( name='date', default = '' )

        short_description = pyre.inventory.str(name='short_description')
        pass # end of Inventory


    def __init__(self, name):
        Component.__init__(self, name, facility='dataobject')
        self.dbTable = self.__class__.__name__
        return


    def getRecord(self, director):
        '''retrieve db record'''
        # the id in its db table
        objID = self.inventory.id
        # table name
        table = self.dbTable
        # retrieve record from db
        return director.clerk.getRecordByID( table, objID )


    def propertyNames(self, director):
        '''get property names'''
        # override this method if the following automatic
        # retrieval does not work

        # record
        record = self.getRecord( director )
        
        # properties of the data object (columns in the table)
        properties = record.getColumnNames()
        
        # remove id from list. we don't want users to edit that.
        del properties[ properties.index('id') ]
        
        # remove any thing ends with 'id'
        properties = filter( lambda a: not a.endswith( 'id' ), properties )
        return properties
        


# version
__id__ = "$Id$"

# End of file 
