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


from Form import Form as base, InputProcessingError


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


    def expand(self, form, errors = None, properties = None):
        '''expand an existing form with fields from this component'''

        if self.inventory.id == '':
            configuration = self.inventory
        else:
            configuration = self.getRecord()
        
        prefix = formactor_action_prefix
        
        id_field = form.hidden(
            name = '%s.id' % prefix, value = configuration.id)

        if errors:
            p = form.paragraph( cls = 'error' )
            p.text = [
                'The form you filled out contained some errros.',
                'Please look through the values you have entered',
                'and correct any mistakes.',
                ]

        if properties is None: properties = self.parameters
        for property in properties:
            meta = getattr( self.Inventory, property ).meta
            value = getattr( configuration, property )
            field = form.text(
                id = 'edit_%s' % property,
                name='%s.%s' % (prefix, property),
                label = meta.get('label') or property,
                value = value)
            tip = _combine( meta.get('tip') )
            if tip: field.help = tip
            if errors and property in errors:
                field.error = _combine( meta['tiponerror'] )
                pass # end if
            continue

        return


    def processUserInputs(self):
        'process user inputs and save them to db'

        if self.inventory.id == '':
            record = self.createRecord()
        else:
            record = self.getRecord( )
        
        for prop in self.parameters:
            setattr(
                record, prop,
                self.inventory.getTraitValue( prop ) )
            continue

        clerk = self.director.clerk
        clerk.updateRecord( record )

        return record


    def getRecord(self):
        'get DB record'
        id = self.inventory.id
        director = self.director
        clerk = director.clerk
        return clerk.getRecordByID( self.DBTable, id )


    def createRecord(self):
        director = self.director
        id = new_id( director )
        exec 'from vnf.dom.%s import %s as table' % (self.DBTable, self.DBTable)
        record = table()
        record.id = id
        director.clerk.newRecord( record )
        return record

    pass # end of DBObjectForm


def _combine(text):
    if isinstance(text, str): return text
    if isinstance(text, list) or isinstance(text, tuple):
        return ' '.join( text )
    raise NotImplementedError, text

from vnf.components.misc import new_id

formactor_action_prefix = 'actor.form-received' # assumed actor is a form actor


# version
__id__ = "$Id$"

# End of file 
