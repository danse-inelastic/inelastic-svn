Tutorial
========

Here are a set of operations one might try::  

	>>>from matter import Structure, Lattice, Atom
	>>>at1 = Atom('Fe', [0, 0, 0])
	>>>at2 = Atom('Fe', [0.5, 0.5, 0.5])
	>>>stru = Structure( [ at1, at2], lattice=Lattice(2.87, 2.87, 2.87, 90, 90, 90) )

