#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                               Orthologue, Ltd.
#                      (C) 2004-2006  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.components.Component import Component


class Scribe(Component):

    
    def objectEditForm(self, document, obj, properties,
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


# version
__id__ = "$Id: Scribe.py,v 1.27 2008-02-21 10:02:22 aivazis Exp $"

# End of file 
