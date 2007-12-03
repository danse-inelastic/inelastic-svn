
def getModules( package ):
    "get and import a list of python modules under given python package"
    packagename = package.__name__
    path = package.__path__[0]
    import os
    rt = []
    for entry in os.listdir( path ):
        f = os.path.join( path, entry )
        if os.path.isdir( f ): continue
        if entry == "__init__.py": continue
        modulename, ext = os.path.splitext( entry )
        if ext != ".py" : continue
        exec "import %s.%s as m" % (packagename, modulename)
        rt.append( m )
        continue
    return rt



def test_getModules():
    import atomic_properties
    print getModules( atomic_properties )
    return 


def main():
    test_getModules()
    return 

if __name__ == "__main__": main()
