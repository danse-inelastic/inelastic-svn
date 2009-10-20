import sys
print sys.path
from pyrev.main import PyrevCommand


if __name__ == '__main__':
    # md examples
    PyrevCommand(['-o','png','-p','Gulp','memd.gulp.Gulp'])
    PyrevCommand(['-o','png','-p','Mmtk','memd.mmtk.Mmtk'])
    # matter data objects
    PyrevCommand(['-o','png','-p','Structure','matter.Structure'])
    PyrevCommand(['-o','png','-p','Lattice','matter.Lattice'])
    PyrevCommand(['-o','png','-p','Atom','matter.Atom'])
    