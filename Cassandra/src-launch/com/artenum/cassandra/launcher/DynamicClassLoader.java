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

import java.net.URL;
import java.net.URLClassLoader;

import java.util.ArrayList;
import java.util.Collection;
import java.util.jar.JarFile;

/**
 * <pre>
 * <b>Project ref           :</b> CASSANDRA project
 * <b>Copyright and license :</b> See relevant sections
 * <b>Status                :</b> under development
 * <b>Creation              :</b> 04/03/2005
 * <b>Modification          :</b>
 *
 * <b>Description  :</b> Plugin class loader, and plugin integration manager.
 *
 * </pre>
 * <table cellpadding="3" cellspacing="0" border="1" width="100%">
 * <tr BGCOLOR="#CCCCFF" CLASS="TableHeadingColor"><td><b>Version number</b></td><td><b>Author (name, e-mail)</b></td><td><b>Corrections/Modifications</b></td></tr>
 * <tr><td>0.1</td><td>Sebastien Jourdain, jourdain@artenum.com</td><td>Creation</td></tr>
 * </table>
 *
 * @author        Sebastien Jourdain
 * @version       0.1
 */
public class DynamicClassLoader extends URLClassLoader {
    private static DynamicClassLoader pluginManager;
    private ArrayList pluginList;

    private DynamicClassLoader() {
        super(new URL[] {  }, DynamicClassLoader.class.getClassLoader());
        pluginList = new ArrayList();
    }

    public static DynamicClassLoader getInstance() {
        if (pluginManager == null) {
            pluginManager = new DynamicClassLoader();
        }

        return pluginManager;
    }

    public void loadDirectory(File pluginDir) {
    	System.out.println(pluginDir);
        File[] jarFileList = pluginDir.listFiles();
        for (int i = 0; i < jarFileList.length; i++) {
            pluginManager.addJar(jarFileList[i]);
        }
    }

    public void addJar(File file) {
        if (file.exists() && file.isFile() && file.getName().endsWith(".jar")) {
            try {
                URL url = new URL("file", "", file.getAbsolutePath());
                addURL(url);
                System.out.println("Loading jar: " + url);
                JarFile jarFile = new JarFile(file);
                String pluginList = jarFile.getManifest().getMainAttributes().getValue("Cassandra-Plugin");
                if (pluginList != null) {
                    String[] plugins = pluginList.split(",");
                    for (int j = 0; j < plugins.length; j++) {
                        if (plugins[j].length() > 0) {
                            System.out.println("Plugin Loaded : " + plugins[j]);
                            this.pluginList.add(plugins[j]);
                        }
                    }
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public Object getPluginIntegrator(String pluginIntegratorClassName)
        throws InstantiationException, IllegalAccessException, ClassNotFoundException {
        return loadClass(pluginIntegratorClassName).newInstance();
    }

    public Collection getPluginIntegratorList() {
        return pluginList;
    }
}
