#!/usr/bin/env python
"""\
Vimm: Visual Interface for Materials Manipulation

Copyright 2010 Caltech.  Copyright 2005 Sandia Corporation.  Under the terms of Contract
DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government
retains certain rights in this sofware.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  
USA
"""

import sys,wx

#print sys.path
#sys.path.append(os.path.abspath('..'))#this is a hack because Eclipse has bug

from vimm.FrameSep import FrameSep

def Main():
    app = wx.PySimpleApp()
    frame = FrameSep(None,-1,'vimm')
    frame.Show()
    if len(sys.argv) > 1:
        fname = sys.argv[1]
        frame.load_file_nodialog(fname)
    else: 
        pass
        #frame.load_file_nodialog("/home/jbk/DANSE/vimm/testfiles/o2.molf")
        #frame.create_xyz_file()
        #frame.dotest()
        
    app.MainLoop()

if __name__ == '__main__':
    do_profile = 0
    if do_profile:
        import profile,pstats
        profile.run('Main()',
                    'vimm_prof')
        vimm_prof = pstats.Stats('vimm_prof')
        vimm_prof.strip_dirs().sort_stats('time').print_stats(20)
    else:
        Main()
    #end
