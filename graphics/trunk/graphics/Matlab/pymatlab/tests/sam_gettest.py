import graphics.Matlab.pymatlab as pymatlab
import Numeric

def test():
    '''test(); simple test of put for list and array'''
    A = 1
    B = [1,2]
    C = Numeric.array(B)
#   S = 'foo'
#   T = Numeric.array(S)

#   vars = [A,B,C,S,T]
    vars = [A,B,C]
    m = pymatlab.matlab()

    print "Numeric imported..."
    print "testing put()...\n"
    x = raw_input("test ? > ")
    if x: exec "vars = ["+x+"]"

    for v in vars:

        vv = 'X'
        print "\nvalue = %r" % v
        print "RESULTS: whos[], get()"

        m.put(vv,v)
        print "shape='?', array='?', reduce=False: %r, %r" % \
              (m.whos[vv],m.get(vv))
        print "shape=None, array='?', reduce=False: %r, %r" % \
              (m.whos[vv],m.get(vv,shape=None))
        print "shape='?', array='?', reduce=True: %r, %r" % \
              (m.whos[vv],m.get(vv,reduce=True))
        print "shape='?', array=True, reduce=False: %r, %r" % \
              (m.whos[vv],m.get(vv,array=True))
        print "shape='?', array='?', reduce=False: %r, %r" % \
              (m.whos[vv],m.get(vv))
        print "shape='?', array=False, reduce=False: %r, %r" % \
              (m.whos[vv],m.get(vv,array=False))
        print "shape='?', array='?', reduce=False: %r, %r" % \
              (m.whos[vv],m.get(vv))

        m.delete(vv)

    return

if __name__ == '__main__':
    test()
