import graphics.Matlab.pymatlab as pymatlab

def test():
    '''test(); simple test of show for variable and array'''
    print "testing..."
    x = 69
    y = [[2,4],[7,8]]
    #z = 'foobar'
    a = [1,2,3]
    b = []
    #input = [x,y,z,a,b]
    input = [x,y,a,b]
    print 'Input: %s' % input
    m = pymatlab.matlab()
    m.put('x',x)
    m.put('y',y)
    #m.put('z',z)
    m.put('a',a)
    m.put('b',b)
    print 'Local variables: %s' % m.show(local=True)
    print 'PRINTED Local variables: '
    m.show(local=True,stdout=True)
    print 'Matlab variables: %s' % m.show(local=False)
    print 'PRINTED Matlab variables: '
    m.show(local=False,stdout=True)
    print "Matlab 'who': "
    m.who()
    print "Matlab 'whos': "
    m.who(terse=False)
    x = m.get('x')
    y = m.get('y')
    #z = m.get('z')
    a = m.get('a',array=True,reduce=True)
    b = m.get('b',array=True,reduce=True)
    #output = [x,y,z,a,b]
    output = [x,y,a,b]
    print 'Output: %s' % output
    return

if __name__ == '__main__':
    test()
