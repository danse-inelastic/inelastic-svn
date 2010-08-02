#!/usr/bin/env python
"""\
 CML Chemical XML Markup Language Loader/Saver
 Author: Richard P. Muller

 Limitations:
 1. Currently supports only the old (1.0) form of XML files, since
    this is all that JMol has. This version uses a 3x3 matrix for
    the unit cell. And only uses cartesian coordinates for atoms.
 2. Currently supports loading or saving only one structure per file
"""
from vimm.Material import Material
from vimm.Atom import Atom
from vimm.Utilities import path_split,cleansym
from vimm.Element import sym2no,symbol
from vimm.NumWrap import array

extensions=["cml"]
filetype="CML Chemical XML Markup Language"

from xml.sax import ContentHandler,make_parser,ErrorHandler
from xml.sax.handler import feature_namespaces

class DocumentRoot:
    def __init__(self):
        self.geos = []
    def wrap(self, parent): return self.geos
    def on_cml(self,cml): self.geos.extend(cml.geos)
    def on_molecule(self,mol): self.geos.append(mol)
    def body(self): return self.geos

class cml:
    tag = "cml"
    def __init__(self,attr):
        self.attr = attr
        self.geos = []
    def on_molecule(self,molecule): self.geos.append(molecule)
    def on_list(self,geos): self.geos.extend(geos)
    def wrap(self,parent): parent.on_cml(self)

class molecule:
    tag = "molecule"
    def __init__(self,attr):
        self.attr = attr
        self.cell = None
        self.atoms = []
        return

    def on_atom(self,atuple): self.atoms.append(atuple)
    def on_atomArray(self,atoms): self.atoms = atoms
    def on_crystal(self,a,b,c): self.cell = (a,b,c)
    def wrap(self,parent): parent.on_molecule(self)

class crystal:
    tag = "crystal"
    def __init__(self,attr): self.attr = attr
    def on_floatArray(self,type,vals):
        if type == "a": self.avec = vals
        elif type == "b": self.bvec = vals
        elif type == "c": self.cvec = vals
        else:
            raise "Unsupported type %s in crystal:on_floatArray()" % type
        return
    def on_string(self,type,vals): pass
    def wrap(self,parent): parent.on_crystal(self.avec,self.bvec,self.cvec)
    
class atomArray:
    tag = "atomArray"
    def __init__(self,attr):
        self.attr = attr
        self.atoms = []

    def on_atom(self,atuple): self.atoms.append(atuple)
    def on_stringArray(self,type,vals):
        if type == 'id': self.ids = vals
        elif type == 'elementType': self.els = vals
    def on_floatArray(self,type,vals):
        if type == 'x3': self.xs = vals
        elif type == 'y3': self.ys = vals
        elif type == 'z3': self.zs = vals
    def wrap(self, parent):
        if not self.atoms:
            assert len(self.els) == len(self.xs) == len(self.ys) == len(self.zs)
            for i in range(len(self.els)):
                self.atoms.append((self.els[i],
                                   (self.xs[i],self.ys[i],self.zs[i])))
        parent.on_atomArray(self.atoms)
            

class atom:
    tag = "atom"
    def __init__(self,attr): self.attr = attr2dict(attr)
    def on_float(self,type,val): self.attr[type] = val
    def on_string(self,type,val): self.attr[type] = val

    def on_coordinate3(self,type,val):
        if type == 'xyz3': self.attr[type] = "%f %f %f" % tuple(val)

    def wrap(self, parent):
        if self.attr.has_key('x3'):
            x = float(self.attr['x3'])
            y = float(self.attr['y3'])
            z = float(self.attr['z3'])
        elif self.attr.has_key('x2'):
            x = float(self.attr['x2'])
            y = float(self.attr['y2'])
            z = float(0)
        elif self.attr.has_key('xyz3'):
            x,y,z = map(float,self.attr['xyz3'].split())
        type = str(self.attr['elementType'])
        parent.on_atom((type,(x,y,z)))
        return

class floatArray:
    tag = "floatArray"
    def __init__(self,attr):
        self.val = []
        self.attr = attr
    def on_chars(self,chars):
        self.val.extend(map(float,chars.split()))
    def wrap(self,parent):
        if self.attr.has_key('builtin'):
            type = self.attr['builtin']
        elif self.attr.has_key('title'):
            type = self.attr['title']
        else:
            type = None
        if type: parent.on_floatArray(type,self.val)
        return

class afloat:
    tag = "float"
    def __init__(self,attr): self.attr = attr
    def on_chars(self,chars): self.val = float(chars)
    def wrap(self,parent):
        type = self.attr['builtin']
        parent.on_float(type,self.val)

class astring:
    tag = "string"
    def __init__(self,attr): self.attr = attr
    def on_chars(self, chars): self.val = chars.strip()
    def wrap(self,parent):
        if self.attr.has_key('builtin'):
            type = self.attr['builtin']
        else:
            type = None
        if type: parent.on_string(type,self.val)
        return

class bondArray:
    tag = "bondArray"
    def __init__(self,attr): self.attr = attr
    def wrap(self,parent): pass
    def on_string(self,type,val): pass

class bond:
    tag = "bond"
    def __init__(self,attr): self.attr = attr
    def wrap(self,parent): pass
    def on_string(self,type,val): pass

class stringArray:
    tag = "stringArray"
    def __init__(self,attr): self.attr = attr
    def on_chars(self, chars): self.val = chars.split()
    def wrap(self,parent):
        if self.attr.has_key('builtin'):
            type = self.attr['builtin']
        else:
            type = None
        if type: parent.on_stringArray(type,self.val)

class coordinate3:
    tag = "coordinate3"
    def __init__(self,attr): self.attr = attr
    def on_chars(self,chars): self.val = map(float,chars.split())
    def wrap(self,parent):
        if self.attr.has_key('builtin'):
            type = self.attr['builtin']
        else:
            type = None
        if type: parent.on_coordinate3(type,self.val)

class list:
    tag = "list"
    def __init__(self,attr):
        self.attr = attr
        self.geos = []
    def wrap(self,parent): parent.on_list(self.geos)
    def on_molecule(self,molecule): self.geos.append(molecule)

# Largely unimplimented
class nullhandler:
    def __init__(self,attr): self.attr = attr
    def wrap(self,parent): pass

class scalar(nullhandler): tag = "scalar"
class bibliography(nullhandler):
    tag = "bibliography"
    def on_string(self,*args): pass

class person(nullhandler): tag="person"

class CMLParser(ContentHandler):
    handlers = [cml, molecule, crystal, atomArray, atom, coordinate3,
                stringArray, floatArray, afloat, astring,
                bond, bondArray, list, scalar, bibliography, person]

    def __init__(self):
        ContentHandler.__init__(self)
        self.currentNode = None
        self.nodeStack = []
        self.registerHandlers()
        return

    def process(self,filename):
        root = DocumentRoot()
        self.currentNode = root
        parser = make_parser()
        parser.setFeature(feature_namespaces,0)
        parser.setContentHandler(self)
        parser.parse(filename)
        return root.body()

    def startElement(self, name, attributes):
        self.nodeStack.append(self.currentNode)
        self.currentNode = self.tagHandlers[name](attributes)
        return

    def characters(self, characters):
        import string
        characters = string.strip(characters)
        if characters: self.currentNode.on_chars(characters)
        return

    def endElement(self, name):
        node = self.currentNode
        self.currentNode = self.nodeStack.pop()
        node.wrap(self.currentNode)
        return

    def registerHandlers(self):
        self.tagHandlers = {}
        for handler in self.handlers:
            self.tagHandlers[handler.tag] = handler
        return

def load(fullfilename):
    filedir, fileprefix, fileext = path_split(fullfilename)
    material=Material(fileprefix)

    parser = CMLParser()
    geos = parser.process(fullfilename)

    molecule = geos[0]
    atoms = molecule.atoms
    cell = molecule.cell
    nat = len(atoms)

    for i in range(nat):
        sym,pos = atoms[i]
        pos = array(pos)
        atno = sym2no[sym]
        material.add_atom(Atom(atno,pos,sym,sym+str(i)))
    if cell:
        the_cell = Cell(cell[0],cell[1],cell[2])
        material.set_cell(the_cell)
    material.bonds_from_distance()
    return material

def save(filename, material):
    dir, prefix, ext = path_split(filename)
    atoms = material.get_atom_list()
    cell = material.get_cell()
    flines = ["<?xml version=\"1.0\" ?>"]
    flines.append("<cml title=\"%s\">" % prefix)
    flines.append("<molecule id=\"%s\">" % prefix)
    if cell:
        ax,ay,az = cell.axyz
        bx,by,bz = cell.bxyz
        cx,cy,cz = cell.cxyz
        flines.append(" <crystal>")
        flines.append("  <floatArray convention=\"PMP\" title=\"a\">%f %f %f</floatArray>" % (ax,ay,az))
        flines.append("  <floatArray convention=\"PMP\" title=\"b\">%f %f %f</floatArray>" % (bx,by,bz))
        flines.append("  <floatArray convention=\"PMP\" title=\"c\">%f %f %f</floatArray>" % (cx,cy,cz))
        flines.append(" </crystal>")

    flines.append(" <atomArray>")
    for atom in atoms:
        x,y,z = atom.get_position()
        flines.append("  <atom id=\"%s\" elementType=\"%s\" x3=\"%f\" y3=\"%f\" z3=\"%f\"/>" % (atom.get_label(),atom.get_symbol(),x,y,z))
    flines.append(" </atomArray>")
    flines.append("</molecule>")
    flines.append("</cml>\n")
    
    open(filename, 'w').write("\n".join(flines))
    return

def attr2dict(attr):
    "Convert the attr from the sax parser to a normal dict"
    adict = {}
    for key,val in attr.items(): adict[key] = val
    return adict

