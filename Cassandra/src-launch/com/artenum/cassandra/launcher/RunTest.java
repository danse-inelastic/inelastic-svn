/*
 * (c) Copyright: Artenum SARL, 101-103 Boulevard Mac Donald, 
 *                75019, Paris, France 2005.
 *                http://www.artenum.com
 *
 * License:
 *
 *  This program is free software; you can redistribute it 
 *  and/or modify it under the terms of the Q Public License; 
 *  either version 1 of the License.
 * 
 *  This program is distributed in the hope that it will be
 *  useful, but WITHOUT ANY WARRANTY; without even the implied
 *  warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
 *  PURPOSE. See the Q Public License for more details.
 * 
 *  You should have received a copy of the Q Public License 
 *  License along with this program;
 *  if not, write to:
 *    Artenum SARL, 101-103 Boulevard Mac Donald,
 *    75019, PARIS, FRANCE, e-mail: contact@artenum.com
 */

package com.artenum.cassandra.launcher;

import java.io.File;

import java.util.ArrayList;

/**
 * @author Sebastien
 */
public class RunTest {
    public static void main(String[] args) throws Exception {
        try {
            PropertyLoader.loadProperties("./config.properties");
        } catch (Exception e) {
            e.printStackTrace();
        }

        /*
           DynamicClassLoader.getInstance().addJar(new File(System.getProperty("java.library.path")));
           Runtime.getRuntime().loadLibrary("vtkHybridJava");
           Runtime.getRuntime().loadLibrary("vtkCommonJava");
           Runtime.getRuntime().loadLibrary("vtkFilteringJava");
           Runtime.getRuntime().loadLibrary("vtkIOJava");
           Runtime.getRuntime().loadLibrary("vtkImagingJava");
           Runtime.getRuntime().loadLibrary("vtkGraphicsJava");
           Runtime.getRuntime().loadLibrary("vtkRenderingJava");
           Runtime.getRuntime().loadLibrary("vtkHybridJava");
         */

        // Load thirdpart
        if (System.getProperty("java.class.path") != null) {
            String[] classPath = System.getProperty("java.class.path").split(";");
            File jarFile = null;
            for (int i = 0; i < classPath.length; i++) {
                jarFile = new File(classPath[i]);
                DynamicClassLoader.getInstance().addJar(jarFile);
            }
        }

        // Load main parameters
        int index = 1;
        ArrayList params = new ArrayList();
        while (System.getProperty("java.main.param." + index) != null) {
            params.add(System.getProperty("java.main.param." + index++));
        }

        Class runnerClass = DynamicClassLoader.getInstance().loadClass(System.getProperty("java.main.class"));
        runnerClass.getMethod("main", new Class[] { String[].class }).invoke(runnerClass.newInstance(), params.toArray());
    }
}
