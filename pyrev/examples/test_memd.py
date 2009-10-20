import sys
print sys.path
from pyrev.main import PyrevCommand


if __name__ == '__main__':
    #md examples
    PyrevCommand(['-o','png','-p','Gulp','memd.gulp.Gulp'])
    