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


    def objectEditForm(self, document, obj, properties, actor, director):
        '''a form to edit the given object inside the
        given actor.

        document: the UI document where the form will be inserted
        obj: the object db record to be edited
        properties: the properties of the object
        actor: the actor
        director: the director
        '''
        form = document.form(
            name=obj.__class__.__name__,
            legend=obj.short_description,
            action=app.cgihome)

        actor_field = form.hidden(name='actor', value=actor)
        username_filed = form.hidden(
            name='sentry.username', value = director.sentry.username)
        ticket_filed = form.hidden(
            name='sentry.ticket', value = director.sentry.ticket)

        for property in properties:
            value = getattr( obj, property )
            field = form.field(
                id = property,
                name='%s.%s.%s' % (actor, obj, property),
                label=property,
                value = value)
            
            descriptor = getattr(obj.__class__, property)
            tip = descriptor.meta.get('tip')
            if tip: field.help = tip

            continue
            
        submit = form.control(name="submit", type="submit", value="OK")
            
        p = form.paragraph()
        p.text = [
            "some texts here",
            ]
        
        return


# version
__id__ = "$Id: Scribe.py,v 1.27 2008-02-21 10:02:22 aivazis Exp $"

# End of file 
