Tutorial
========

Here is a brief tutorial to get up and running with the structure classes::  

	>>>from matter import Structure, Lattice, Atom
	>>>at1 = Atom('C', [0,0,0])
	>>>at2 = Atom('C', [1,1,1])
	>>>stru = Structure( [ at1, at2], lattice=Lattice(1, 1, 1, 90, 90, 120) )

and here is a normal python block::

	>>>from matter import Structure, Lattice, Atom
	>>>at1 = Atom('C', [0,0,0])
	>>>at2 = Atom('C', [1,1,1])
	>>>stru = Structure( [ at1, at2], lattice=Lattice(1, 1, 1, 90, 90, 120) )