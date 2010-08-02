Scripting interface
===================

In addition to viewing a variety of file formats, Vimm can conveniently view directly many of the data structures produced by the computational engines in VNF.  

Viewing Vibrations:
"""""""""""""""""""


Getting Motion:
"""""""""""""""




GUI Tutorial
============

Architecture
---------------

Most of the functionality of the main GUI is available in the library vimmLib.

.. autoclass vimm.Frame
   :members: set_properties, quit, addshapes, newshapes, dump, set_bg_color, new_file, load_file, load_file_nodialog, save_as, render, render_povray, set_render_lines, set_render_ballstick, set_render_balls, set_render_cylinders, set_unit_cell, set_cell_labels, set_atom_labels, set_hide_h, measurements, clean, animate, advance_frame, create_xyz_file
   
VIMM also contains a number of interfaces which data structures it uses should implement.  As such it has a set of data structures users can also just convert their data objects to, either through file input/output or through a converter class.  A short list of these data structures include:

* vimm.Material
* vimm.Atom

The main frame GUI itself has several smaller GUIs, or panels, within it.  These are:

Sketcher

CoordEditor

Cartesians

CrystalBuilder

CrystalDatabase

Supercell

SlabBuilder

AddUC

NanoBuilder

AlkaneBuilder

ZBuilder

BondAdjustor

OrbitalViewer

The functionality of each of these should also be accessible from vimmLib.

Renderers
---------

Although the data structures and builders are in python, the renders can be

* OpenGL, a well-known fixed function graphics pipeline.  In this environment, algorithms for calculating transformations, lighting, texture coordinates, and other environmental effects are pre-programmed, which controls the graphics hardware. Global states are set up for lights, materials, and textures, and then the shape information is passed into this pipeline.  OpenGL allows real-time rendering of the scene while it is being manipulated.

* Povray, a well-known ray-tracing technique suitable for single snapshots.

* O3D, a new web-based programmable graphics pipeline sponsored by Google.  This programmable pipeline makes use of a shader language, based on HLSL and Cg, that enables you to program the GPU directly through the use of vertex shaders and pixel shaders. Before this era of programmable GPUs, the graphics programmer was limited to a fixed-function pipeline such as OpenGL.  With a programmable graphics pipeline, however, the developer has complete control over the algorithms used in the vertex shader and the pixel shader. In addition, rasterizing and frame-buffer operations can be configured using the O3D API.  O3D is also suitable for real-time rendering of the scene while it is being manipulated.