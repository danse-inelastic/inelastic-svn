from graphics.IDL import IDL
m = IDL()

def test():
    '''test(); simple test of getarr and setattr'''
    print "testing..."
    from numarray import array
    x = 69
    y = [[2,4],[7,8]]
    z = 'foobar'
    a = [1,2,3]
    b = array(a)
    c = array(z)
#   n = None     #XXX: FAIL -- can't pass undefined
    n = 1.5
    s = ['foo','bar']
    input = [x,y,z,a,b,c,n,s]
    print 'Input: %s' % input
    m.x = x
    m.y = y
    m.z = z
    m.a = a
    m.b = b
    m.c = c
    m.n = n
    m.s = s
    print 'Local variables: %s' % m.who(local=True)
    print 'IDL variables: %s' % m.who(local=False)
    x = m.x
    y = m.y
    z = m.z
    a = m.a
    b = m.b
    c = m.c
    n = m.n
    s = m.s
    output = [x,y,z,a,b,c,n,s]
    print 'Output: %s' % output
    print '\n'
    print 'sin(0.5) = ',m.sin(0.5)
    m.help('x')
    return

def test2():
    '''test2(); testing Numeric workaround'''
    #print "testing..."
    try:
        from Numeric import array
        from Numeric import arange
        from Numeric import pi
    except ImportError:
        print 'Numeric not installed.'
        return
    x = arange(6)
    z = array([[1,2],[3,4]])
    m.x = x
    m('print, x')
    print m.x
    m.z = z
    m('print, z')
    print m.z
    print m.sin(pi*x/5)
    print m.sin(pi*z/4)
    m.plot(x,x)
    raw_input('press return')
    m.plot(z,z)
    raw_input('press return')
    return

if __name__ == '__main__':
    test()
    test2()
