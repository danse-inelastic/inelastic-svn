import graphics.Matlab.pymatlab as pymatlab

def test():
    '''test(); simple test of shape for Matlab Arrays'''
    print "testing..."
    a = 1
    b = [1,2]
    c = [[1,2,3],[4,5,6]]
    #s = 'foo'
    #local = {'a':a, 'b':b, 'c':c, 's':s}
    local = {'a':a, 'b':b, 'c':c}
    print 'Input: %r' % local
    m = pymatlab.matlab()
    m.put('a',a)
    m.put('b',b)
    m.put('c',c)
    m.put('a_',a,shape=(1,))
    m.put('b_',b,shape=(2,1))
    #m.put('s',s)
    print 'Local variables: %s' % m.show(local=True)
    print 'PRINTED Local variables: '
    m.show(local=True,stdout=True)
    print ''
    print 'Matlab variables: %s' % m.show(local=False)
    print 'PRINTED Matlab variables: '
    m.show(local=False,stdout=True)
    print "Matlab 'whos':"
    m.who(terse=False)
    local['a'] = m.get('a')
    local['b'] = m.get('b')
    local['c'] = m.get('c')
    local['a_'] = m.get('a_',shape=None)
    local['b_'] = m.get('b_',shape=(1,2))
    #local['s'] = m.get('s')
    print 'Output: %r' % local
    return

if __name__ == '__main__':
    test()
