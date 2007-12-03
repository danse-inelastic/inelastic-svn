#!/usr/bin/env python
# 
# Michael McKerns
# mmckerns@caltech.edu 
from distutils.core import setup

try:
    numericversion = ''
    import Numeric
except ImportError:
    raise "Numeric %r+ is required" % numericversion

setup(name='pygrace',
      version='0.2',
      description='Python bindings for grace',
      author = 'Mike McKerns',
      author_email = 'mmckerns@caltech.edu',
      url = 'http://www.its.caltech.edu/~mmckerns/software/',
      packages=['pygrace'],
      package_dir={'pygrace':''},
      )

# end of file
