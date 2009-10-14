Tutorial
========

Here are a set of operations one might try:  

One can initialize the data structures from atom types and positions:

>>>from matter import Structure, Lattice, Atom
>>>at1 = Atom('Fe', [0, 0, 0])
>>>at2 = Atom('Fe', [0.5, 0.5, 0.5])
>>>stru = Structure( [ at1, at2], lattice=Lattice(2.87, 2.87, 2.87, 90, 90, 90) )
>>> str(stru)
'lattice=Lattice(a=2.87, b=2.87, c=2.87, alpha=90, beta=90, gamma=90)\nAtom Z=26,mass=55.847,average_mass=55.847,atomic_number=26,symbol=Fe\nAtom Z=26,mass=55.847,average_mass=55.847,atomic_number=26,symbol=Fe'

or by reading a cif file:

>>>stru = Structure( [ at1, at2], lattice=Lattice(2.87, 2.87, 2.87, 90, 90, 90) )

To expand the asymmetric unit cell we call:

>>>