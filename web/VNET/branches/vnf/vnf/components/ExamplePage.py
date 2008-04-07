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


from Actor import Actor, action_link, actionRequireAuthentication, AuthenticationError


class ExamplePage(Actor):



    def default(self, director):
        try:
            page = director.retrievePage( 'examplePage' )
        except AuthenticationError, error:
            return error.page

        main = page._body._content._main

        # populate the main column
        document = main.document(title='Test')
        p = document.paragraph()
        p.text = [
            'Example Page',
            ]

        return page


    def __init__(self, name=None):
        if name is None:
            name = "greet"
        super(ExamplePage, self).__init__(name)
        return


    pass # end of Greeter


# version
__id__ = "$Id$"

# End of file 
