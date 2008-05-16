
#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


#def main():
#
#
#    from vnf.applications.WebApplication import WebApplication
#
#
#    class MainApp(WebApplication):
#
#
#        def __init__(self):
#            WebApplication.__init__(self, name='main')#, asCGI=True)
#            return
#
#
#    app = MainApp()
#    return app.run()


# main
if __name__ == '__main__':
    from vnf.applications.WebApplication import WebApplication
    app=WebApplication(name='main')
    #import opal.inventory
    #app.actor='job'#'job'
    #app.actor=opal.inventory.actor(default="greet")
    #from os import environ
    #root='/home/jbk/dv/tools/pythia-0.8'
    #environ['PYTHONPATH']='/home/jbk:'environ['PYTHONPATH']
    #app.inventory.stream=file('test.html','w')
    app.run()
    import os
    os.system('firefox ~/test.html')

# version
__id__ = "$Id: main.py,v 1.1.1.1 2006-11-27 00:09:14 aivazis Exp $"

# End of file 
