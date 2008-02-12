#backend='matplotlibBackend'
backend='vtkBackend'

def use(plt, namespace=globals()):
    """Export the namespace of backend instance to namespace."""
    plt_dict = {}
    plt_dict[backend] = plt
    for item in plt.__dict__:
        plt_dict[item] = eval(backend+'.'+item)                                   
    for item in dir(plt.__class__):
        if not '__' in item:  
            plt_dict[item] = eval(backend+'.'+item) 
    namespace.update(plt_dict)  # Add to global namespace 

    # If this module is imported
    try:
        __all__
    except:
        __all__ = ['vtkBackend']
    try:
        for item in plt_dict.keys():
            __all__.append(item)
    except:
        pass
    del(__all__)

def setBackend(parent, backend2, namespace):
    '''insert the necessary namespace'''
    if backend2=='vtk':
        from graphics.vtk_ import VtkBackend
        plt = VtkBackend(parent) # Create backend instance
        use(plt, namespace) # Export public namespace of vtkBackend to globals()
    elif backend2=='matplotlib':
        import pylab
        use(pylab, namespace)