# Copyright 2005-2007 Brandon Keith  See LICENSE file for details. 
"""
version.py -- provide version information for Sample Builder,
including author list, program name, release info, etc.

$Id: version.py,v 1.22 2007/06/27 01:31:24 bhelfrich Exp $

NOTE: this is copied and imported by autoBuild.py in a directory
which contains no other files, so it needs to be completely self-contained.
(I.e. it should not import anything else in its source directory,
only builtin Python modules.)
"""

__copyright__ = "Copyright 2004-2007, Brandon Keith"

# Alphabetical by last name
__author__ = """Damian Allis
K. Eric Drexler
Josh Hall
Brian Helfrich
Eric Messick
Huaicai Mo
Ninad Sathaye
Mark Sims
Bruce Smith
Will Ware"""

class Version:
    """Example usage:
    from version import Version
    v = Version()
    print v, v.product, v.authors
    """
    # Every instance of Version will share the same state
    __shared_state = {
        "major": 0,
        "minor": 9,
        "tiny": 1,     # tiny and teensy are optional
        # "teensy": 0,   # you can have both, or just tiny, or neither
        "releaseType": "Alpha 9",
        "releaseDate": "July 1, 2007",
        "product": "Sample Builder",
        "copyright": __copyright__,
        "authors": __author__
        }
    def __init__(self):
        # Use Alex Martelli's singleton recipe
        # http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66531
        self.__dict__ = self.__shared_state
    def __setattr__(self, attr, value):  # attributes write-protected
        raise AttributeError, attr
    def __repr__(self):
        major = self.__shared_state["major"]
        minor = self.__shared_state["minor"]
        str = "%d.%d" % (major, minor)
        if self.__shared_state.has_key("tiny"):
            teensy = self.__shared_state["tiny"]
            str += ".%d" % teensy
            if self.__shared_state.has_key("teensy"):
                teensy = self.__shared_state["teensy"]
                str += ".%d" % teensy
        return str

###############################

if __name__ == "__main__":
    v = Version()
    print v
    for x in dir(v):
        print x + ":", getattr(v, x)
        print
    # test write protection
    try:
        v.foo = "bar"
        print "WRITE PROTECTION IS BROKEN"
    except AttributeError:
        pass
