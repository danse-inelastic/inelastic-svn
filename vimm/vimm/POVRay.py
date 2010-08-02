#!/usr/bin/env python
"""\
NAME  
        POVRay.py - Construct/render POV-Ray scenes

DESCRIPTION
        An object-oriented front-end to the functions in POV-Ray. A
        POV-Ray scene is constructed using the Scene class, and
        different types of objects can be added to that scene.
        Optionally, the scene can be rendered (using the 'povray_prog'
        variable to point to the POV-Ray program) and displayed
        (using the 'display_prog' variable to point to ImageMagick's
        display program (although any other command-line-driven
        graphics display program can be substituted here)).

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import os, shutil


povray_incl = '/usr/local/share/povray-3.6/include'
povray_prog = '/usr/bin/povray'   
display_prog = 'open' 
      
class Scene:
    def __init__(self,name="pov",camera_pos=(0,10,0),bgcolor=(1,1,1),
                 height=480,width=640):
        self.name = name
        self.items = []
        self.bgcolor = bgcolor
        self.camera = Camera(camera_pos)
        self.lights = [Light((0,0,10.)),
                       Light((0,0,-10.)),
                       Light((0,10.,0)),
                       Light((0,-10.,0)),
                       Light((10.,0,0)),
                       Light((-10.,0,0))]
        self.height = height
        self.width = width
        return

    def add(self,item):
        self.items.append(item)

    def set_bgcolor(self,r,g,b): self.bgcolor = (r,g,b)

    def set_camera(self,position,lookat=None):
        self.camera.set_position(position)
        if lookat: self.camera.set_lookat(lookat)

    def strarray(self):
        val = ["background { rgb %s }\n" % vec3(self.bgcolor)]
        val += self.camera.strarray()
        for item in self.lights: val += item.strarray()
        for item in self.items: val += item.strarray()
        return val

    def write_pov(self, outputFile=None):
        if outputFile:
            from Utilities import assureCorrectFileEnding
            self.povname = assureCorrectFileEnding(outputFile,'pov')
        else:
            self.povname = self.name + ".pov"
        file = open(self.povname,"w")
        file.writelines(self.strarray())
        file.close()
        return

    #TODO: replace this with python bindings to povray as soon as someone writes some    
    def render(self,prog=povray_prog, include_dir =povray_incl, outputFile=None):
#        if outputFile:
#            from Utilities import assureCorrectFileEnding
#            self.outputFile = assureCorrectFileEnding(outputFile,'png')
#        else:
#            self.outputFile = self.name + ".png"
        # this writes out to the current directory
        os.system("%s +I%s +H%d +W%d +FN +A0.5" %\
                  (prog, self.povname, self.height, self.width))
        # move the file instead of just writing it out to the desired directory because povray only writes to /tmp or . 
        #outputFileDir,outputFileName = os.path.split(self.outputFile)
        #shutil.move(os.path.join(os.path.abspath('.'),outputFileName), self.outputFile)
        return
    

    def display(self,prog=display_prog):
        self.pngname = self.name + '.png'
        os.system("%s %s" % (prog,self.pngname))
        return        

class Camera:
    def __init__(self,position=(0,10,0),lookat=(0,0,0),sky=None):
        self.type = "Camera"
        self.position = position
        self.lookat = lookat
        self.sky = sky # which way is up for the camera
        return

    def set_position(self,position): self.position = position
    def set_lookat(self,lookat): self.lookat = lookat

    def strarray(self):
        val = ["camera{\n",
               " location %s\n" % vec3(self.position),
               " look_at %s\n" % vec3(self.lookat)]
        if self.sky:
            val += [" sky %s\n" % vec3((0,-1,0))]
        val += ["}\n"]
        return val

class Light:
    def __init__(self,position=(10,10,10),color=(1,1,1)):
        self.type = "Light"
        self.position = position
        self.color = color
        return

    def strarray(self):
        return ["light_source{\n",
                " %s\n" % vec3(self.position),
                " color rgb %s\n" % vec3(self.color),
                "}\n"]

class Reflection:
    def __init__(self,value,ismetallic=1):
        self.value = value
        self.ismetallic = ismetallic
        return

    def strarray(self):
        val = ["reflection {\n",
               " %.2f\n" % self.value]
        if self.ismetallic:
            val += [" metallic\n"]
        val += ["}\n"]
        return val

class Pigment:
    def __init__(self,color,transparency=0):
        self.color = color
        self.transparency = transparency
        return

    def strarray(self):
        return ["pigment {\n",
                " rgbt %s\n" % vec4(self.color,self.transparency),
                "}\n"]

class CheckeredPigment:
    def __init__(self,color1,color2):
        self.color1 = color1
        self.color2 = color2
        return

    def strarray(self):
        return ["pigment {\n",
                " checker\n",
                " rgb %s,\n" % vec3(self.color1),
                " rgb %s\n" % vec3(self.color2),
                "}\n"]

class Finish:
    def __init__(self,ambient=0.2,diffuse=0.6,phong=1,specular=0):
        self.ambient = ambient
        self.diffuse = diffuse
        self.phong = phong
        self.specular = specular
        self.reflection = None
        return

    def reflective(self): self.reflection = Reflection(0.8)

    def strarray(self):
        val = ["finish{\n",
                " ambient %.2f diffuse %.2f phong %.2f specular %.2f\n" %\
                (self.ambient,self.diffuse,self.phong,self.specular)]
        if self.reflection:
            val += self.reflection.strarray()
        val +=  ["}\n"]
        return val
               

class Texture:
    def __init__(self,color,ambient=0.2,diffuse=0.6,phong=1,specular=0,
                 transparency=0):
        self.pigment = Pigment(color,transparency)
        self.finish = Finish(ambient,diffuse,phong,specular)
        return

    def strarray(self):
        return ["texture{\n"] + self.pigment.strarray() + \
              self.finish.strarray() + ["}\n"]

class Sphere:
    def __init__(self,position,radius,color=(0.8,0.8,1.0)):
        self.type = "Sphere"
        self.position = position
        self.radius = radius
        self.texture = Texture(color)
        return

    def strarray(self):
        return ["sphere{\n",
                " %s,%.3f\n" % (vec3(self.position),self.radius)] \
                + self.texture.strarray() \
                + ["}\n"]

class Cylinder:
    def __init__(self,start,end,radius,color=(0.5,0.5,0.5)):
        self.type = "Cylinder"
        self.start = start
        self.end = end
        self.radius = radius
        self.texture = Texture(color)
        return

    def strarray(self):
        return ["cylinder{\n",
                " %s, %s, %.3f\n" % (vec3(self.start),vec3(self.end),
                                     self.radius),
                " open\n"] \
                + self.texture.strarray() \
                + ["}\n"]

class Line(Cylinder):
    def __init__(self,start,end,color=(0,0,0)):
        Cylinder.__init__(self,start,end,0.02,color)
        return

class Polygon:
    def __init__(self,points,color):
        self.type = "Polygon"
        self.points = points
        self.pigment = Pigment(color)
        return

    def strarray(self):
        np = len(self.points)
        val = ["polygon {\n",
                " %d,\n" % np]
        for i in range(np):
            val.append("%s" % vec3(self.points[i]))
            if i < np-1:
                val.append(",\n")
            else:
                val.append("\n")
        val += self.pigment.strarray()
        val += ["}\n"]
        return val


class TriangleMesh:
    # The point in the mesh can either be a triangle or a smooth triangle
    def __init__(self,points,color,transparency=0.4):
        self.color = color
        self.texture = Texture(color=color,phong=0,
                               transparency=transparency)
        self.points = points
        return

    def strarray(self):
        val = ["#declare MeshCol%d%d%d = \n" % self.color] +\
              self.texture.strarray() +\
              [";\n",
               "mesh {\n"]
        for point in self.points:
            if len(point) == 3: # normal triangle
                val += ["triangle {\n",
                        "%s,\n" % vec3(point[0]),
                        "%s,\n" % vec3(point[1]),
                        "%s\n" % vec3(point[2]),
                        "}\n"]
            elif len(point) == 6: # smooth triangle
                val += ["smooth_triangle {\n",
                        "%s,%s,\n" % (vec3(point[0]),vec3(point[1])),
                        "%s,%s,\n" % (vec3(point[2]),vec3(point[3])),
                        "%s,%s\n"  % (vec3(point[4]),vec3(point[5])),
                        "}\n"]
            else:
                raise "Bad point: " + `point`
        val += ["texture { MeshCol%d%d%d}\n" % self.color,
                "}\n"]
        return val

class Plane:
    def __init__(self,orientation,color=(0.5,0.5,0.5)):
        self.type = "Plane"
        self.orientation = orientation
        self.texture = Texture(color)
        return

    def strarray(self):
        return ["plane{\n",
                " %s,-1\n" % vec3(self.orientation)] \
                + self.texture.strarray() \
                + ["}\n"]

class SkySphere:
    def __init__(self):
        self.type = "SkySphere"
        return

    def strarray(self):
        return ["sky_sphere{\n",
                " pigment {\n",
                "  gradient y\n",
                "  color_map {\n",
                "   [0.0 rgb <0.6,0.7,1.0>]\n",
                "   [0.7 rgb <0.0,0.1,0.8>]\n",
                "  }\n",
                " }\n",
                "}\n"]

class Text:
    def __init__(self,text,origin,thickness=1):
        self.text = text
        self.origin = origin
        self.thickness = thickness
        return

    def strarray(self):
        return ["text {\n",
                " ttf \"timrom.ttf\" \n",
                "\"%s\" %d,%s\n" % (self.text,self.thickness,
                                    vec3(self.origin)),
                "}\n"]

class Fog:
    def __init__(self,type=1,distance=10,color=(0.4,0.4,0.4)):
        self.type = "Fog"
        self.fog_type = type #1=constant, 2=ground frog
        self.distance = distance # 63% vis at distance
        self.color = color
        self.turbulance = None
        return

    def set_turbulance(self,turbulance=(0.5,0.5,1.0),depth=0.5,
                       omega=0.5,lamb = 2.0, octaves=6):
        self.turbulance = turbulance
        self.depth = depth
        self.omega = omega
        self.lamb = lamb
        self.octaves = octaves

    def set_ground(self,offset=0.5,alt=0.5):
        self.type = 2
        self.offset = offset # height of constant fog
        self.alt = alt # at offset+alt, dens = 25%

    def strarray(self):
        val = ["fog{\n",
               " fog_type %d\n" % self.fog_type,
               " distance %d\n" % self.distance,
               " color rgb %s\n" % vec3(self.color)]
        if self.turbulance:
            val += [" turbulance %s\n" % vec3(self.turbulance),
                    " turb_depth %.2f\n" % self.depth,
                    " omega %.2f\n" % self.omega,
                    " lambda %.2f\n" % self.lamb,
                    " octaves %d\n" % self.octaves]
        if self.type == 2:
            val += [" fog_offset %.2f\n" % self.offset,
                    " fog_alt %.2f\n" % self.alt]
        val += ["}\n"]
        return val
    
def vec3(vec): return "<%.3f,%.3f,%.3f>" % vec
def vec4((r,g,b),t): return "<%.3f,%.3f,%.3f,%.3f>" % (r,g,b,t)

# routines that can be called externally to do the rendering
def render_old(povname,pov_prog,include_dir,height=240,width=320):
    # version 3.1 compliant render (Molden writes to this)
    os.system("%s +I%s +H%d +W%d +FN +MV3.1 +A0.5 +L%s" %\
              (pov_prog,povname,height,width,include_dir))
    return

def render(povname,pov_prog,include_dir,height=240,width=320):
    os.system("%s +I%s +H%d +W%d +FN +A0.5 +L%s" %\
              (pov_prog,povname,height,width,include_dir))
    return

def display(pngname,display_prog):
    os.system("%s %s" % (display_prog,pngname))
    return        

if __name__ == '__main__':
    scene = Scene("test")
    scene.set_camera((0,0.5,-5))
    plane = Plane((0,1,0),(0,0,1))
    plane.texture.pigment = CheckeredPigment((1,1,1),(0,0,1))
    scene.add(plane)
    scene.add(SkySphere())
    sphere = Sphere((0,0,0),1)
    sphere.texture.finish.reflective()
    scene.add(sphere)

    # Test for the mesh 
    #points = [
    #    ((0,0,0),(1,0,0),(1,1,0)),
    #    ((0,0,0),(1,1,0),(0,1,0))
    #    ]
    #scene.add(TriangleMesh(points,(0,0,1)))

    # Test for the polygon:
    #points = [(0,0,-2),(1,0,-2),(1,1,-2),(0,1,-2),(0,0,-2)]
    #scene.add(Polygon(points,(0,0,0)))

    # Test for the line
    scene.add(Line((0,0,-2),(1,1,-2),(0,0,0)))

    # Test for the text. Isn't quite working yet. Takes a long time
    #  to render. Orientation seems off
    #scene.add(Text("Hi Rick",(0,2,2)))

    scene.write_pov()
    scene.render()
    scene.display()


