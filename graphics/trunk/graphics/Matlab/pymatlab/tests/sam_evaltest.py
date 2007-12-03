import graphics.Matlab.pymatlab as pymatlab
import Numeric

def test():
    '''test(); test of eval and comm for Matlab commands'''
    m = pymatlab.matlab()
    print "testing eval... (exit == quit)"
    while 1:
        command = raw_input("eval > ")
        if command == 'exit' and not m.evalbuff: break
        m.eval(command)    
        print "local show() = %r" % m.show(local=True)
        print "evalbuff = %r" % m.evalbuff
        print ""
    print ""
    affirm = raw_input("Test prompt? ")
    if affirm in ['t','true','True','T','Y','Yes','yes','y','ok','OK','1']:
        print 'Local variables: %s' % m.show(local=True)
        print "testing prompt... (exit == quit)"
        m.prompt()
        print 'Local variables: %s' % m.show(local=True)
    return

if __name__ == '__main__':
    test()
