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

import java.awt.BorderLayout;
import java.io.File;

import javax.swing.JComponent;
import javax.swing.JFrame;
import javax.swing.JMenuBar;

/**
 * @author Sebastien
 */
public class Run {

    public static void main(String[] args) throws Exception {
        try {
        	if(args.length>0)
        		PropertyLoader.loadProperties(args[0]);
        	else
        		PropertyLoader.loadProperties("./config.properties");
        } catch (Exception e) {
            e.printStackTrace();
        }

        // Load thirdpart
        if (System.getProperty("java.class.path") != null) {
            String[] classPath = System.getProperty("java.class.path").split(";");
            File jarFile = null;
            for (int i = 0; i < classPath.length; i++) {
                jarFile = new File(classPath[i]);
                DynamicClassLoader.getInstance().addJar(jarFile);
            }
        }

        Class cassandraClass = DynamicClassLoader.getInstance().loadClass("com.artenum.cassandra.Cassandra");
        Object cassandra = cassandraClass.newInstance();

        // Build the JFrame
        JFrame f = new JFrame("Cassandra VTK viewer");
        f.setJMenuBar((JMenuBar) cassandraClass.getMethod("getDefaultMenu", new Class[] {}).invoke(cassandra, new Object[] {}));
        f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        f.getContentPane().add((JComponent) cassandraClass.getMethod("getDefaultToolBar", new Class[] {}).invoke(cassandra, new Object[] {}),
                BorderLayout.NORTH);
        f.getContentPane().add((JComponent) cassandraClass.getMethod("getDefaultUI", new Class[] {}).invoke(cassandra, new Object[] {}), BorderLayout.CENTER);
        f.setSize(600, 400);
        f.setLocationRelativeTo(null);
        //
        if (System.getProperty("cassandra.plugin.dir") != null) {
            File pluginDir = new File(System.getProperty("cassandra.plugin.dir"));
            if (pluginDir.exists()) {
                cassandraClass.getMethod("loadPluginInDirectory", new Class[] { File.class }).invoke(cassandra, new Object[] { pluginDir });
            }
        }

        // set preferences done in config file now...
        File localDir = new File(".");
        cassandraClass.getMethod("setPreference", new Class[] { String.class, Object.class }).invoke(cassandra,
                new Object[] { "cassandra.pref.image.save.dir", new File(System.getProperty("cassandra.pref.image.save.dir")) });
        cassandraClass.getMethod("setPreference", new Class[] { String.class, Object.class }).invoke(cassandra,
                new Object[] { "cassandra.pref.plugin.dir", new File(System.getProperty("cassandra.pref.plugin.dir")) });
        cassandraClass.getMethod("setPreference", new Class[] { String.class, Object.class }).invoke(cassandra,
                new Object[] { "cassandra.pref.vtk.file.dir", new File(System.getProperty("cassandra.pref.vtk.file.dir")) });
        cassandraClass.getMethod("setPreference", new Class[] { String.class, Object.class }).invoke(cassandra,
                new Object[] { "cassandra.pref.script.dir", new File(System.getProperty("cassandra.pref.script.dir")) });
        // exit method
        Object cassandraActionManager = cassandraClass.getMethod("getActionManager", new Class[] {}).invoke(cassandra, new Object[] {});
        cassandraActionManager.getClass().getMethod("setExitAction",
                new Class[] { DynamicClassLoader.getInstance().loadClass("com.artenum.cassandra.action.ExitAction") }).invoke(cassandraActionManager,
                new Object[] { DynamicClassLoader.getInstance().loadClass("com.artenum.cassandra.action.SystemExit").newInstance() });
        //
        f.setVisible(true);
        //cassandra.gui.showPipeLine();
    }
}