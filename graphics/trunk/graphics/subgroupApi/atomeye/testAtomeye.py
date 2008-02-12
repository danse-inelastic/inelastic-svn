from crystal.Structure import UnitCell,Site,Atom

def uc_test():
    uc = UnitCell( )

    at1 = Atom(symbol='Fe', mass=57)
    at2 = Atom(symbol='Al')
    at3 = Atom(symbol="Zr")

    site1 = Site((0,0,0), at1)
    site2 = Site((0.5,0.5,0.5), at2)
    site3 = Site((0.5, 0.5, 0.0), at3)
    site4 = Site((0.5, 0.0, 0.5), at3)
    site5 = Site((0.0, 0.5, 0.5), at3)
    
    uc.addSite(site1, "Fe1" )
    uc.addSite(site2, "Al1" )
    uc.addSite(site3, "")
    uc.addSite(site4, "")
    uc.addSite(site5, "")

    from atomeyecontrol import plot
    
    plot(uc,'/home/jbk/atomEye/A.i686')
        
if __name__ == "__main__":
    uc_test()