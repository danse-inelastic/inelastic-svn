from crystal.Structure import Structure,UnitCell,Atom
from crystal.UnitCell import Site

def uc_test():
    uc = UnitCell()

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
    uc.addSite(site3, "Zr1")
    uc.addSite(site4, "Zr2")
    uc.addSite(site5, "Zr3")
    
    atoms= uc.getAtoms()
    print atoms
    
    structure=Structure(atoms,uc)
    print structure

    from atomeyecontrol import plot
    
    plot(structure,'/home/jbk/atomEye/A.i686')
        
if __name__ == "__main__":
    uc_test()
