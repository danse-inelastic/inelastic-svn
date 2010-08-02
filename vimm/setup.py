"""
Vimm is an open source package for visualizing materials and molecules.
"""

classifiers = """\
Development Status :: 3 - Alpha
Intended Audience :: Developers
Intended Audience :: Science/Research
License :: OSI Approved :: BSD License
Programming Language :: Python
Topic :: Scientific/Engineering
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: Microsoft :: Windows
Operating System :: Unix
Operating System :: MacOS
"""

from distutils.core import setup

doclines = __doc__.split("\n")

setup(name="vimm",
      version="0.7",
      description=doclines[0],
      long_description=__doc__,
      author = "J. Brandon Keith",
      author_email = "jbrkeith@gmail.com",
      url = "http://danse.us",
      license = "GPL",
      platforms = ['any'],
      classifiers = filter(None,classifiers.split("\n")),
      packages = ["vimm","vimm.IO","vimm.engines"],
      #scripts = ["scripts/runVimm.py"],
      )
      
