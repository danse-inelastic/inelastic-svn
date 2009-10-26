Overview
========

The atom, lattice, and structure classes are built with several principles in mind:

* Most users will want "out-of-the-box" functionality in as many ways as possible.  They would like the ability to access diffraction thermal factors, forces, pseudopotentials, neutron-scattering cross sections, and so on

* A smaller group of users will want slim data objects with a bare minimum of methods and information.  Although the speed gains will be very small, the speed-up from using simpler dataobjects is absolutely critical.  Another rationale for wanting as-slim-as-possible dataobjects is because they do not want to continue to develop these data objects for their own purposes and do not want to take the time to learn about all the available methods and attributes.  

Fortunately, both of these aims can be met through metaclasses, which are classes that build other classes.  The two types of Atoms, for example, are shown in the class diagrams below:



The two base libraries the metaclasses use to construct these data objects are: