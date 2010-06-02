Tutorial
========

One can initialize the data structures from atom types, positions, and lattice constants:

>>> from matter import Structure, Lattice, Atom
>>> at1 = Atom('Fe', [0, 0, 0])
>>> at2 = Atom('Fe', [0.5, 0.5, 0.5])
>>> bccFe = Structure( [ at1, at2], lattice=Lattice(2.87, 2.87, 2.87, 90, 90, 90), sgid = 229 )
>>> print bccFe
lattice=Lattice(a=2.87, b=2.87, c=2.87, alpha=90, beta=90, gamma=90)
Fe   0.000000 0.000000 0.000000 1.0000
Fe   0.500000 0.500000 0.500000 1.0000

or by reading a cif file:

>>> pbte = Structure()
>>> pbte.read('PbTe.cif', format='cif')
<matter.Parsers.P_cif.P_cif instance at 0x93196ec>
>>> print pbte
lattice=Lattice(a=6.461, b=6.461, c=6.461, alpha=90, beta=90, gamma=90)
Pb2+ 0.500000 0.500000 0.500000 1.0000
Pb2+ 0.500000 0.000000 0.000000 1.0000
Pb2+ 0.000000 0.500000 0.000000 1.0000
Pb2+ 0.000000 0.000000 0.500000 1.0000
Te   0.000000 0.000000 0.000000 1.0000
Te   0.000000 0.500000 0.500000 1.0000
Te   0.500000 0.000000 0.500000 1.0000
Te   0.500000 0.500000 0.000000 1.0000

or a pdb file, or an xyz file, for example. We note the asymmetric unit cell is expanded by default.  To verify the space group number and name::

    >>> pbte.sg.number
    225
    >>> pbte.sg.num_sym_equiv
    192
    >>> pbte.sg.num_primitive_sym_equiv
    48
    >>> pbte.sg.short_name
    Fm-3m
    >>> pbte.sg.alt_name
    F M 3 M
    >>> pbte.sg.point_group_name
    PGm3barm
    >>> pbte.sg.crystal_system
    CUBIC
    >>> pbte.sg.pdb_name
    F 4/m -3 2/m
    >>> for symop in pbte.sg.symop_list:
    ...  print symop
    [ 1.000  0.000  0.000  0.000]
    [ 0.000  1.000  0.000  0.000]
    [ 0.000  0.000  1.000  0.000]
    
    [ 1.000  0.000  0.000  0.000]
    [ 0.000  1.000  0.000  0.500]
    [ 0.000  0.000  1.000  0.500]
    
    [ 1.000  0.000  0.000  0.500]
    [ 0.000  1.000  0.000  0.000]
    [ 0.000  0.000  1.000  0.500]
    
	...
    
    [ 0.000  0.000  1.000  0.000]
    [ 0.000  1.000  0.000  0.500]
    [ 1.000  0.000  0.000  0.500]
    
    [ 0.000  0.000  1.000  0.500]
    [ 0.000  1.000  0.000  0.000]
    [ 1.000  0.000  0.000  0.500]
    
    [ 0.000  0.000  1.000  0.500]
    [ 0.000  1.000  0.000  0.500]
    [ 1.000  0.000  0.000  0.000]


To query information about occupied Wyckoff points:

(coming)
(embed Wyckoff point information in each atom?)

(space group is a property where one can set it with a space group object or a number, in which latter case it will lookup the default setting and try the sym ops of each setting it has on the atoms...if they don't work, it will issue warning the atom positions are inconsistent with space group operations and recommend you specify a new list of ops...eventually it will just recompute the space group (best soln).)

Eventually it may be possible to calculate the symmetry directly from a list of atoms, but for now, input of the space group is necessary. 

To create a supercell, simply import the supercell utility and specify the new lattice directions:

>>> from matter.expansion import supercell
>>> strucTall = supercell(pbte, (1,1,2))
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
>>> bccFe.forces = forces
>>> bccFe[0].force
[0.0, 0.60999999999999999, 0.69999999999999996]
 
To calculate a Monkhorst-Pack mesh over the reciprocal space of the lattice:

>>> bccFe.lattice.getMonkhorstPackGrid()
 [[[-0.52359878 -0.52359878  0.52359878]
   [-0.52359878  0.52359878  0.52359878]]
  [[ 0.52359878 -0.52359878  0.52359878]
   [ 0.52359878  0.52359878  0.52359878]]]]
>>> bccFe.lattice.getFracMonkhorstPackGrid()
[[[[-0.25 -0.25 -0.25]
   [-0.25  0.25 -0.25]]
  [[ 0.25 -0.25 -0.25]
   [ 0.25  0.25 -0.25]]]
 [[[-0.25 -0.25  0.25]
   [-0.25  0.25  0.25]]
  [[ 0.25 -0.25  0.25]
   [ 0.25  0.25  0.25]]]]

To generate equivalent bonded neighbors and their distances:

>>> bccFe.getFirstNN()
>>> bccFe.getFirstNNDistance()
>>> bccFe.getSecNN()
>>> bccFe.getThirdNN()

To get equivalent bonded neighbors and their distances, which is the bond matrix for a BvK calculation: 
(1.get nearest neighbors...2. apply symmetry operations of space group to see which ones are equivalent...3. sort and assign BvK force constants)

>>> bccFe.getBondMatrix()

To store a lattice in a database:

.. literalinclude:: ../examples/storeLattice.py

To store an atom in a database:

.. literalinclude:: ../examples/storeAtom.py

To store a structure in a database:

.. literalinclude:: ../examples/storeStructure.py

.. todo:: (lattice test)
