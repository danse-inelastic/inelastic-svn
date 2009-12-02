/*
  Automatically Converted from Java Source 
  
  by java2groovy v0.0.1   Copyright Jeremy Rayner 2007
  
  !! NOT FIT FOR ANY PURPOSE !! 
  'java2groovy' cannot be used to convert one working program into another  */

package cod

import java.io.File
import java.util.ArrayList

import javax.swing.JOptionPane

class TestCifs 
    {static void main(String[] args) {
        if (args.length == 1) {
            File f = new File(args[0])
            ArrayList<String> no = new ArrayList<String>()
            ArrayList<String> two = new ArrayList<String>()

            File[] files = f.listFiles()

            for <FOR_EACH_CLAUSE>File file</FOR_EACH_CLAUSE>{
                if (!file.isDirectory() && file.getName().endsWith("cif")) {
                    System.out.println(file.getPath())
                    CifParser cp = null
                    try {
                        cp = new CifParser(file)
                        cp.parseCoordinates("_atom_site_fract_x")


                        for (int i = 0 ; i < cp.coordinates.size() ; i++){
                            double[] d = cp.coordinates.get(i)
                            System.out.println(cp.species.get(i) + " " + d[0] + " " + d[1] + " " + d[2])
}



                        cp.parseOperators()
                        JOptionPane.showMessageDialog(null, "Hi")
}










                     catch (Exception e) {
                        if (e.getMessage() == null) {
                            System.out.println(file.getName())

                            for <FOR_EACH_CLAUSE>StackTraceElement ste</FOR_EACH_CLAUSE>
                            System.out.println(ste)
} else 




                        if (e.getMessage().equals("Error, no coordinates!")) 
                        no.add(file.getPath()) else 
                        if (e.getMessage().equals("Error! More than one set of coordinates.")) 
                        two.add(file.getPath()) else {
                            System.out.println(file.getName())

                            for <FOR_EACH_CLAUSE>StackTraceElement ste</FOR_EACH_CLAUSE>
                            System.out.println(ste)
}
}
}
}


































            System.out.println("Files with no coordinates")
            for <FOR_EACH_CLAUSE>String s</FOR_EACH_CLAUSE>
            System.out.println(s)
            System.out.println("Files with more than one set of coordinates")
            for <FOR_EACH_CLAUSE>String s</FOR_EACH_CLAUSE>
            System.out.println(s)
}
}
}
