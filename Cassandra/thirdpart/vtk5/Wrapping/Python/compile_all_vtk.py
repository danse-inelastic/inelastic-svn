import compileall
compileall.compile_dir('/home/juju/VTK5.0/VTK/Wrapping/Python')
file = open('/home/juju/VTK5.0/VTK/Wrapping/Python/vtk_compile_complete', 'w')
file.write('Done')
