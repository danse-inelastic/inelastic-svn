

                   VTK 5.0
      binary version for Linux/Suse 10 32 bit,
      Python 2.4, JAVA/JRE 1.5

    This native version of VTK 5.0 has been compiled and 
packaged bu Artenum SARL, Paris, 2006/03/16 on Medusa.

This package includes the Python and Java wrapping. Native
libraries have been compiled and linked in shared mode and 
accept to be re-located. 

For further information and questions on this binary package, 
please see:
              http://www.artenum.com
     or 
              contact@artenum.com
            
For further information and question about VTK source code, 
please see: 
              http://public.kitware.com/VTK/


1. PYTHON settings

Before to use python or vtkpython, please set the 
LD_LIBRARY_PATH as folow:

   export LD_LIBRARY_PATH=$VTK_ROOT_DIR/lib/:$LD_LIBRARY_PATH


2. JAVA settings

The JNI wrapping has been done with a SUN JRE 1.5 and requires
a JVM 1.5 and higer. The vtk.jar file is in the 
$VTK_ROOT_DIR/bin directory. 


			Artenum, Paris (France), March 2006.


