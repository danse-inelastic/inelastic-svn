#!/usr/bin/env python

#default instllation modules
#defaultModules = ['Matlab','grace','IDL','Matplotlib','gnuplot'] #install all
defaultModules = ['grace','Matplotlib','gnuplot']  #install freeware only
#defaultModules = ['Matplotlib']  #minimal to install

def parseOptions( argv, keywords ):
    "get values for input keywords"
    res = {}
    for keyword in keywords:
        for i, item in enumerate(argv):
            if item.startswith(keyword):
                value = item[ len(keyword) + 1: ]
                if value == "": value = True
                res[keyword] = value
                del argv[i]
                pass
            continue
        continue
    return res

def parseCommandLine():
    import sys, getopt
    argv = sys.argv

    keywords = ['--modules']
    options = parseOptions( argv, keywords )

    modules = []
    if options.get('--modules'): modules = options['--modules'].split(',')

    if not modules:
        #we need a default list of modules
        modules = defaultModules
        pass
    else:
        #otherwise, we must have modules that is not empty. that is good
        pass
    
    print '='*70
    print ' '*2, "Modules to be installed are"
    print ' '*4, modules
    print '='*70
    return modules


def preparePackage( package, sourceRoot = ".", modules=defaultModules ):
    package.changeRoot( sourceRoot )
    #------------------------------------------------------------
    #dependencies
    #
    #------------------------------------------------------------
    # build procedure config includes
    #from distutils_adpt.paths.CaltechBuildProcedureConfig import paths as configPaths
    if 'Matlab' in modules:
        from distutils_adpt.paths.Matlab import name as pathsName
    if 'grace' in modules:
        from distutils_adpt.paths.Grace import name as pathsName
    if 'gnuplot' in modules:
        from distutils_adpt.paths.Gnuplot import name as pathsName
    if 'IDL' in modules:
        from distutils_adpt.paths.IDL import name as pathsName

    #------------------------------------------------------------
    #include directories
    #package.addIncludeDirs( configPaths.includes )


    #--------------------------------------------------------
    # now add subdirs
    #
    #graphics_Matlab
    if 'Matlab' in modules:
        package.addPurePython(
            sourceDir = 'Matlab',
            destModuleName = 'graphics.Matlab')

    #graphics_grace
    if 'grace' in modules:
        package.addPurePython(
            sourceDir = 'grace',
            destModuleName = 'graphics.grace')

    #graphics_IDL
    if 'IDL' in modules:
        package.addPurePython(
            sourceDir = 'IDL',
            destModuleName = 'graphics.IDL')

    #graphics_Matplotlib
    if 'Matplotlib' in modules:
        package.addPurePython(
            sourceDir = 'Matplotlib',
            destModuleName = 'graphics.Matplotlib')

    #graphics_gnuplot
    if 'gnuplot' in modules:
        package.addPurePython(
            sourceDir = 'gnuplot',
            destModuleName = 'graphics.gnuplot')

    #graphics_root
    package.addPurePython(
        sourceDir = 'graphics',
        destModuleName = 'graphics')
    return package


if __name__ == "__main__":
    #------------------------------------------------------------
    #parse user inputs
    modules = parseCommandLine()

    #init the package
    from distutils_adpt.Package import Package
    package = Package('graphics', '0.1.0a')

    preparePackage( package, modules=modules )

    package.setup()

