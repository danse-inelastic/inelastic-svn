import journal
debug = journal.debug('sampleassembly.elements.elementTypes')


from Element import Element


def register( package ):
    global _types
    newtypes = getTypes( package )
    _types.update( newtypes )
    return



def getTypes( package ):
    f = package.__file__
    package_name = package.__name__
    import os
    d = os.path.dirname( f )
    if d == '': d = '.'
    debug.log( 'directory: %s' % d )

    pyexts = ['.py', '.pyc', '.pyd' , '.pyo' ]
    _modules = []
    types = {}
    for f in os.listdir( d ):
        for ext in pyexts:
            if f.endswith( ext ):
                name = f[: -len(ext)]
                debug.log('module %s' % name)
                #debug.log('_modules = %s' % _modules)
                if name in _modules: break
                if name.startswith( '_' ): break # ignore private modules
                _modules.append( name )
                try:
                    exec "from %s.%s import %s" % (package_name, name, name )
                except Exception, msg:
                    debug.log( '%s:%s' % (msg.__class__.__name__, msg) )
                    break
                klass = eval( name )
                debug.log('class %s' % klass)
                try:
                    if issubclass( klass, Element ): types[name] = klass
                    pass
                except:
                    print "Error for ", name, klass
                    raise
                break
            continue
        continue
    return types


def typeFromName( name ):
    global _types
    if len(_types) == 0: _init_types()
    if name not in _types:
        raise "Unknown element type: %s" % name
    return _types[name]


def _init_types( ):
    import sampleassembly.elements
    register( sampleassembly.elements )
    return



#debug.activate()

_types = {}


if __name__ == '__main__':
    print typeFromName( 'SampleAssembly' )


