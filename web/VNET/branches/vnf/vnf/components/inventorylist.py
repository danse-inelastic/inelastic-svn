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


from Actor import action_link, actionRequireAuthentication


def list( container, document, actor, director ):
    p = document.paragraph()

    formatstr = '%(index)s: %(name)s (%(link)s)'

    for i, element in enumerate( container ):
        
        p = document.paragraph()
        
        # link of callback
        link = action_link(
            actionRequireAuthentication(
            actor, director.sentry,
            routine = 'edit',
            label = 'configure',
            id = element.id,
            ),  director.cgihome
            )
        p.text += [
            formatstr % {'name': element.short_description,
                         'link': link,
                         'index': i+1}
            ]
        continue
    return


# version
__id__ = "$Id$"

# End of file 
