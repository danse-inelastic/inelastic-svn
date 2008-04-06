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



class ObjectEditFormCreater:


    def create(self, document, obj, properties,
               toplevel_container, actor, director):
        '''a form to edit the given object inside the
        given actor.

        document: the UI document where the form will be inserted
        obj: the object db record to be edited
        properties: the properties of the object
        toplevel_container: the top level container db object that
            the actor is working on
        actor: the actor
        director: the director
        '''
        return self.dispatch( obj )(
            document, obj, properties,
            toplevel_container, actor, director)


    def onInstrument(self, document, obj, properties,
                toplevel_container, actor, director):
        objtype = obj.__class__
        objtypename = objtype.__name__
        
        form = document.form(
            name=objtypename,
            legend=obj.short_description,
            action=director.cgihome)

        actor_field = form.hidden(name='actor', value=actor)
        routine_field = form.hidden(name='routine', value='set')
        id_field = form.hidden(
            name = '%s.id' % actor, value = toplevel_container.id)
        
        username_filed = form.hidden(
            name='sentry.username', value = director.sentry.username)
        ticket_filed = form.hidden(
            name='sentry.ticket', value = director.sentry.ticket)
        
        dataobject_filed = form.hidden(
            name = '%s.dataobject' % actor, value = objtypename.lower() )
        id_field1 = form.hidden(
            name = '%s.dataobject.id' % actor, value = obj.id)

        prefix = '%s.%s' % (actor, objtypename.lower() )

        for property in properties:
            
            value = getattr( obj, property )
            value = _tostr( value )
            
            field = form.text(
                id = property,
                name='%s.%s' % (prefix, property),
                label=property,
                value = value)
            
            descriptor = getattr(objtype, property)
            tip = descriptor.meta.get('tip')
            if tip: field.help = tip

            continue

        instrument = director.clerk.getHierarchy( obj )
        geometer = instrument.geometer
        for component in instrument.componentsequence:
            record = geometer[ component ]
            reference, position, orientation = \
                       record.reference_label, record.position, record.orientation

            name = 'instrument.geometer.%s' % (component, )
            value = '%s, %s, %s' % (position, orientation, reference or '')
            
            field = form.text(
                id = component,
                name = name,
                label = component,
                value =  value )

            continue
            
        submit = form.control(name="submit", type="submit", value="OK")
            
        p = form.paragraph()
        p.text = [
            ]
        
        return


    def dispatch(self, obj ):
        type = obj.__class__.__name__
        try:
            m = getattr(self, 'on%s' % type )
        except:
            m = self.default
            pass
        return m


    def default(self, document, obj, properties,
                toplevel_container, actor, director):
        objtype = obj.__class__
        objtypename = objtype.__name__
        
        form = document.form(
            name=objtypename,
            legend=obj.short_description,
            action=director.cgihome)

        actor_field = form.hidden(name='actor', value=actor)
        routine_field = form.hidden(name='routine', value='set')
        id_field = form.hidden(
            name = '%s.id' % actor, value = toplevel_container.id)
        
        username_filed = form.hidden(
            name='sentry.username', value = director.sentry.username)
        ticket_filed = form.hidden(
            name='sentry.ticket', value = director.sentry.ticket)
        
        dataobject_filed = form.hidden(
            name = '%s.dataobject' % actor, value = objtypename.lower() )
        id_field1 = form.hidden(
            name = '%s.dataobject.id' % actor, value = obj.id)

        prefix = '%s.%s' % (actor, objtypename.lower() )

        for property in properties:
            
            value = getattr( obj, property )
            value = _tostr( value )
            
            field = form.text(
                id = property,
                name='%s.%s' % (prefix, property),
                label=property,
                value = value)
            
            descriptor = getattr(objtype, property)
            tip = descriptor.meta.get('tip')
            if tip: field.help = tip

            continue
            
        submit = form.control(name="submit", type="submit", value="OK")
            
        p = form.paragraph()
        p.text = [
            ]
        
        return



def _tostr( value ):
    if isinstance(value, list) or isinstance(value, tuple):
        return ','.join( [ str(item) for item in value ] )
    return str(value)


# version
__id__ = "$Id$"

# End of file 
