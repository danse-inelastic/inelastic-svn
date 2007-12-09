# Copyright 2006-2007 Brandon Keith  See LICENSE file for details. 
"""
PixelTester.py

$Id: PixelTester.py,v 1.3 2007/05/17 18:17:05 emessick Exp $
"""

# PixelTester is untested -- not even fully parsed by python yet

##e needs save button, per-session filenames, access to on disk log of prior files,
# or way of reading new image from same file, and including reread-policy
# (and id if done "by command to instance")
# along with filename in the texture-dict key
# (but optim for when multiple reads got same image data, whether by same instance or different ones??
#  not simple -- eg if single textures have varying data or (worse for displists) names, other issues, and somewhat orthogonal)


#e more imports

from Column import SimpleColumn #e reloadable

class PixelTester(InstanceOrExpr, DelegatingMixin): # ought to be InstanceMacro but trying this alternate style just to see it
    # args
    testexpr = Arg(Widget2D) # instantiated right here, hope that's ok
    testname = Arg(str) # required for now, used to form filename
    # value
    filename = format_Expr("/tmp/%s.jpg", testname)
    delegate = SimpleColumn(
        
        TextRect("saved image from PRIOR session, in blue box"), # kluge: execute this first, so we read file before writing it
        Boxed(bordercolor = blue)(
            Image(filename)
        ),
        Spacer(0.3),
        
        TextRect("live widget, in purple box"),
        Boxed(bordercolor = purple)(
            PixelGrabber(testexpr, filename)
        ),

        ##e and put current session image here, for comparison, or put top on in a tab control for flicker test
    )
    pass # end of class PixelTester

# end
