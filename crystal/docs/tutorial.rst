Tutorial
========

Here are a set of operations one might try:  

One can initialize the data structures from atom types and positions:

>>> from matter import Structure, Lattice, Atom
>>> at1 = Atom('Fe', [0, 0, 0])
>>> at2 = Atom('Fe', [0.5, 0.5, 0.5])
>>> stru = Structure( [ at1, at2], lattice=Lattice(2.87, 2.87, 2.87, 90, 90, 90) )
>>> print str(stru)
'lattice=Lattice(a=2.87, b=2.87, c=2.87, alpha=90, beta=90, gamma=90)\nAtom Z=26,mass=55.847,average_mass=55.847,atomic_number=26,symbol=Fe\nAtom Z=26,mass=55.847,average_mass=55.847,atomic_number=26,symbol=Fe'

or by reading a cif file:

>>> stru.read('PbTe.cif', format='cif')
>>> print str(stru)
lattice=Lattice(a=6.461, b=6.461, c=6.461, alpha=90, beta=90, gamma=90)
Atom Z=82,mass=207.2,average_mass=207.2,atomic_number=82,symbol=Pb2+
Atom Z=82,mass=207.2,average_mass=207.2,atomic_number=82,symbol=Pb2+
Atom Z=82,mass=207.2,average_mass=207.2,atomic_number=82,symbol=Pb2+
Atom Z=82,mass=207.2,average_mass=207.2,atomic_number=82,symbol=Pb2+
Atom Z=52,mass=127.6,average_mass=127.6,atomic_number=52,symbol=Te
Atom Z=52,mass=127.6,average_mass=127.6,atomic_number=52,symbol=Te
Atom Z=52,mass=127.6,average_mass=127.6,atomic_number=52,symbol=Te
Atom Z=52,mass=127.6,average_mass=127.6,atomic_number=52,symbol=Te

or pdb or xyz file, for example. We note the asymmetric unit cell is expanded by default.  

>>>