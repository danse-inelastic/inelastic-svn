#!/usr/bin/env python
#

import os
from google.appengine.ext.webapp import template

import wsgiref.handlers

from google.appengine.ext import webapp

class MainHandler(webapp.RequestHandler):

    def get(self):
    #self.response.out.write('Hello world!')
#    greetings_query = Greeting.all().order('-date')
#    greetings = greetings_query.fetch(10)
#
#    if users.get_current_user():
#        url = users.create_logout_url(self.request.uri)
#        url_linktext = 'Logout'
#    else:
#        url = users.create_login_url(self.request.uri)
#        url_linktext = 'Login'
#
#    template_values = {
#        'greetings': greetings,
#        'url': url,
#        'url_linktext': url_linktext,
#        }
#
#    path = os.path.join(os.path.dirname(__file__), 'index.html')
#    self.response.out.write(template.render(path, template_values))
        path = os.path.join(os.path.dirname(__file__), 'vimm.html')
        self.response.out.write(template.render(path,{}))


def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()
