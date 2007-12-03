#!/usr/bin/env python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#Created by:  Jiwu Liu (jliu@pa.msu.edu)
#description:  Required initialization when trying to use Gtk+ together with thread
#                      Currently needed by Matplotlib 
#<LicenseText>
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import gtk
gtk.threads_init()

#version
__id__ = '$Id: gtkinit.py,v 1.2 2005/05/23 15:51:00 jwliu Exp $'
