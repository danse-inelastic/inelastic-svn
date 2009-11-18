Tutorial
========

One can initialize the data structures from atom types, positions, and lattice constants:

>>> from matter import Structure, Lattice, Atom
>>> at1 = Atom('Fe', [0, 0, 0])
>>> at2 = Atom('Fe', [0.5, 0.5, 0.5])
>>> stru1 = Structure( [ at1, at2], lattice=Lattice(2.87, 2.87, 2.87, 90, 90, 90) )
>>> print stru1
lattice=Lattice(a=2.87, b=2.87, c=2.87, alpha=90, beta=90, gamma=90)
Fe   0.000000 0.000000 0.000000 1.0000
Fe   0.500000 0.500000 0.500000 1.0000

or by reading a cif file:

>>> stru2 = Structure()
>>> stru2.read('PbTe.cif', format='cif')
<matter.Parsers.P_cif.P_cif instance at 0x93196ec>
>>> print stru2
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

>>> stru.sg.number
225
>>> stru.sg.short_name
Fm-3m

(should show how to get symmetry operations)

To query information about occupied Wyckoff points:

(coming)
(embed Wyckoff point information in each atom?)

One can also set the space group:

(this is a property where one can set it with a space group object or a number, in which latter case it will lookup the default setting and try the sym ops of each setting it has on the atoms...if they don't work, it will issue warning the atom positions are inconsistent with space group operations and recommend you specify a new list of ops...eventually it will just recompute the space group (best soln).)

Eventually it may be possible to calculate the symmetry directly from a list of atoms, but for now, input of the space group is necessary. 

To create a supercell, simply import the supercell utility and specify the new lattice directions:

>>> from matter.expansion import supercell
>>> strucTall = supercell(stru2, (1,1,2))
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

>>> forces = [[0.0, 0.61, 0.7], [1.8, 0.9, 1.1]]
>>> stru1.forces = forces
>>> stru1[0].force
[0.0, 0.60999999999999999, 0.69999999999999996]
 
To calculate a Monkhorst-Pack mesh over the reciprocal space of the lattice:

>>> stru1.lattice.getMonkhorstPackGrid()
 [[[-0.52359878 -0.52359878  0.52359878]
   [-0.52359878  0.52359878  0.52359878]]
  [[ 0.52359878 -0.52359878  0.52359878]
   [ 0.52359878  0.52359878  0.52359878]]]]
>>> stru1.lattice.getFracMonkhorstPackGrid()
[[[[-0.25 -0.25 -0.25]
   [-0.25  0.25 -0.25]]
  [[ 0.25 -0.25 -0.25]
   [ 0.25  0.25 -0.25]]]
 [[[-0.25 -0.25  0.25]
   [-0.25  0.25  0.25]]
  [[ 0.25 -0.25  0.25]
   [ 0.25  0.25  0.25]]]]

To generate equivalent neighbors and their distances:

>>> stru1.getFirstNN()
>>> stru1.getFirstNNDistance()
>>> stru1.getSecNN()
>>> stru1.getThirdNN()

To get the bond matrix for a BvK calculation: 

>>> stru.getBondMatrix()


.. todo:: (lattice test)
