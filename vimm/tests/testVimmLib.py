

from vimm.vimmLib import *

import os
files = ["../testfiles/caffeine.xyz","../testfiles/co2ftf4-c2a.xyz"]
absFiles = []
for file in files:
    absFiles.append(os.path.abspath(file))

m1 = load_file(absFiles[0])
print m1.get_name()

m2 = load_file(absFiles[1])
print m2.get_name()
dump_movie(m2, "testmeout.png")

m2 = create_nanotube(10,10,10)
save_file("nano.xyz", m2)

atoms = m1.get_atoms()
d = measure_distance(atoms[0], atoms[1])
print d

m3 = build_crystal_from_db("Diamond")
v2 = Viewer(m3)

#v1 = Viewer(absFiles[0])
#camera = v1.get_camera()
#render_options = v1.get_render_options()
#screen_capture(m1, "testmeout.png", camera, render_options)
