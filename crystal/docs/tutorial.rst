Tutorial
========

One can initialize the data structures from atom types and positions:

>>> from matter import Structure, Lattice, Atom
>>> at1 = Atom('Fe', [0, 0, 0])
>>> at2 = Atom('Fe', [0.5, 0.5, 0.5])
>>> stru = Structure( [ at1, at2], lattice=Lattice(2.87, 2.87, 2.87, 90, 90, 90) )
>>> print str(stru)
lattice=Lattice(a=2.87, b=2.87, c=2.87, alpha=90, beta=90, gamma=90)
Fe   0.000000 0.000000 0.000000 1.0000
Fe   0.500000 0.500000 0.500000 1.0000

or by reading a cif file:

>>> stru.read('PbTe.cif', format='cif')
<matter.Parsers.P_cif.P_cif instance at 0x93196ec>
>>> print str(stru)
lattice=Lattice(a=6.461, b=6.461, c=6.461, alpha=90, beta=90, gamma=90)
Pb2+ 0.500000 0.500000 0.500000 1.0000
Pb2+ 0.500000 0.000000 0.000000 1.0000
Pb2+ 0.000000 0.500000 0.000000 1.0000
Pb2+ 0.000000 0.000000 0.500000 1.0000
Te   0.000000 0.000000 0.000000 1.0000
Te   0.000000 0.500000 0.500000 1.0000
Te   0.500000 0.000000 0.500000 1.0000
Te   0.500000 0.500000 0.000000 1.0000

or a pdb file, or an xyz file, for example. We note the asymmetric unit cell is expanded by default.  To find the space group:

>>> 

To query information about a given Wyckoff point:

>>> stru.


Eventually it may be possible to calculate the symmetry directly from a list of atoms, but for now, input of the space group is necessary. 

To create a supercell, simply import the supercell utility and specify the new lattice directions:

>>> from matter.expansion import supercell
>>> strucTall = supercell(stru, (1,1,2))
>>> print strucTall
lattice=Lattice(a=6.461, b=6.461, c=12.922, alpha=90, beta=90, gamma=90)
Pb2+ 0.500000 0.500000 0.250000 1.0000
Pb2+ 0.500000 0.500000 0.750000 1.0000
Pb2+ 0.500000 0.000000 0.000000 1.0000
Pb2+ 0.500000 0.000000 0.500000 1.0000
Pb2+ 0.000000 0.500000 0.000000 1.0000
Pb2+ 0.000000 0.500000 0.500000 1.0000
Pb2+ 0.000000 0.000000 0.250000 1.0000
Pb2+ 0.000000 0.000000 0.750000 1.0000
Te   0.000000 0.000000 0.000000 1.0000
Te   0.000000 0.000000 0.500000 1.0000
Te   0.000000 0.500000 0.250000 1.0000
Te   0.000000 0.500000 0.750000 1.0000
Te   0.500000 0.000000 0.250000 1.0000
Te   0.500000 0.000000 0.750000 1.0000
Te   0.500000 0.500000 0.000000 1.0000
Te   0.500000 0.500000 0.500000 1.0000

To set/get the forces, positions, or other settable properties for atoms in the structure:

>>> stru = Structure( [ at1, at2], lattice=Lattice(2.87, 2.87, 2.87, 90, 90, 90) )
>>> forces = [[0.0, 0.61, 0.7], [1.8, 0.9, 1.1]]
>>> stru.forces = forces
>>> stru[0].force
[0.0, 0.60999999999999999, 0.69999999999999996]
 

To calculate a Monkhorst-Pack mesh over the reciprocal space of the lattice:

>>> stru.lattice.getMonkhorstPackGrid()
 [[[-0.52359878 -0.52359878  0.52359878]
   [-0.52359878  0.52359878  0.52359878]]
  [[ 0.52359878 -0.52359878  0.52359878]
   [ 0.52359878  0.52359878  0.52359878]]]]
>>> stru.lattice.getFracMonkhorstPackGrid()
[[[[-0.25 -0.25 -0.25]
   [-0.25  0.25 -0.25]]
  [[ 0.25 -0.25 -0.25]
   [ 0.25  0.25 -0.25]]]
 [[[-0.25 -0.25  0.25]
   [-0.25  0.25  0.25]]
  [[ 0.25 -0.25  0.25]
   [ 0.25  0.25  0.25]]]]

To generate equivalent neighbors and their distances:

>>> stru.getFirstNN()
>>> stru.getFirstNNDistance()
>>> stru.getSecNN()
>>> stru.getThirdNN()

To get the bond matrix for a BvK calculation: 

>>> stru.getBondMatrix()


.. todo:: (lattice test)
