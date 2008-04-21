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


# Specialized form to directly deal with a db object.


from Form import Form as base


class DBObjectForm( base ):

    class Inventory( base.Inventory ):
        import pyre.inventory
        id = pyre.inventory.str( 'id', default = '' )
        short_description = pyre.inventory.str(
            'short_description', default = '' )
        short_description.meta['tip'] = 'A short description'
        pass # end of Inventory


    parameters = [] # parameters to edit in the form

    DBTable = '' # db table class name
    
    
    def legend(self):
        'return a legend string'
        record = self.getRecord()
        return 'Edit %s %r' % (
            self.__class__.__name__.lower(),
            record.short_description)


    def expand(self, form):
        '''expand an existing form with fields from this component'''
        
        record = self.getRecord()
        
        prefix = formactor_action_prefix
        
        id_field = form.hidden(
            name = '%s.id' % prefix, value = record.id)
        
        for property in self.parameters:
            
            value = getattr( record, property )
            value = tostr( value )
            
            field = form.text(
                id = property,
                name='%s.%s' % (prefix, property),
                label=property,
                value = value)
            
            descriptor = getattr(self.Inventory, property)
            tip = descriptor.meta.get('tip')
            if tip:
                field.help = tip
                #field.error = tip

            continue

        return


    def processUserInputs(self):
        'process user inputs and save them to db'

        record = self.getRecord( )
        
        for prop in self.parameters:
            setattr(
                record, prop,
                self.inventory.getTraitValue( prop ) )
            continue

        clerk = self.director.clerk
        clerk.updateRecord( record )

        return


    def getRecord(self):
        'get DB record'
        id = self.inventory.id
        director = self.director
        clerk = director.clerk
        return clerk.getRecordByID( self.DBTable, id )


    pass # end of DBObjectForm



def tostr( value ):
    '''convert a value to a string

    str(obj) sometimes does not work, so we have to have this method.
    '''
    if isinstance(value, list) or isinstance(value, tuple):
        return ','.join( [ str(item) for item in value ] )
    return str(value)



formactor_action_prefix = 'actor.form-received' # assumed actor is a form actor


# version
__id__ = "$Id$"

# End of file 
