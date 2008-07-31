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
package com.artenum.cassandra;

import com.artenum.cassandra.action.CassandraActionListener;
import com.artenum.cassandra.action.SystemExit;
import com.artenum.cassandra.action.menu.AddArrow;
import com.artenum.cassandra.action.menu.AddCone;
import com.artenum.cassandra.action.menu.AddCube;
import com.artenum.cassandra.action.menu.AddLookupTable;
import com.artenum.cassandra.action.menu.AddPlaque;
import com.artenum.cassandra.action.menu.AddScalarBar;
import com.artenum.cassandra.action.menu.AddTxtActor;
import com.artenum.cassandra.launcher.DynamicClassLoader;
import com.artenum.cassandra.pipeline.PipeLineManager;
import com.artenum.cassandra.plugin.PluginManager;
import com.artenum.cassandra.ui.CassandraGUI;
import com.artenum.cassandra.ui.CassandraMenu;
import com.artenum.cassandra.ui.CassandraToolBar;
import com.artenum.cassandra.vtk.CassandraView;

import java.awt.BorderLayout;

import java.io.File;

import java.util.ArrayList;
import java.util.Enumeration;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.Properties;

import javax.swing.JComponent;
import javax.swing.JFrame;

/**
 * <pre>
 * <b>Project ref           :</b> CASSANDRA project
 * <b>Copyright and license :</b> See relevant sections
 * <b>Status                :</b> under development
 * <b>Creation              :</b> 04/03/2005
 * <b>Modification          :</b>
 *      - 21/04/2005: Add the SkinLF part
 *      - 17/05/2005: Add runtime configuration file
 *
 * <b>Description  :</b> Launch and set the default components for Cassandra
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
public class Cassandra {
    private CassandraGUI gui;
    private CassandraMenu menu;
    private PipeLineManager pipeLineManager;
    private PluginManager pluginManager;
    private CassandraActionListener actionListener;
    private CassandraToolBar toolBar;
    private Hashtable preferences;
    private ArrayList prefListener;

    public Cassandra() throws Exception {
        preferences = new Hashtable();
        prefListener = new ArrayList();
        pipeLineManager = (PipeLineManager) DynamicClassLoader.getInstance().loadClass("com.artenum.cassandra.pipeline.SimplePipeLineManager").newInstance(); //new SimplePipeLineManager();
        pluginManager = new PluginManager();
        gui = new CassandraGUI(pipeLineManager, pluginManager);
        actionListener = new CassandraActionListener(gui, pipeLineManager, pluginManager);
        menu = new CassandraMenu(actionListener);
        toolBar = new CassandraToolBar(actionListener);
        actionListener.reloadPlugings();
        gui.update();

        // register preference listener
        addPreferenceListener(actionListener);
        addPreferenceListener(gui);

        // init view
        gui.hideConsole();
        gui.getPyConsole().getPythonInterpreter().set("cassandra", this);

        // Add action menu
        menu.addToolMenuComponent(new AddLookupTable("Add a Lookup Table", pipeLineManager));
        menu.addToolMenuComponent(new AddScalarBar("Add a ScalarBar", pipeLineManager));
        menu.addSourceMenuComponent(new AddCone("Add a cone", pipeLineManager));
        menu.addSourceMenuComponent(new AddCube("Add a cube", pipeLineManager));
        menu.addSourceMenuComponent(new AddPlaque("Add a plaque", pipeLineManager));
        menu.addSourceMenuComponent(new AddArrow("Add a arrow", pipeLineManager));
        menu.addSourceMenuComponent(new AddTxtActor("Add a text", pipeLineManager));

        // Set general properties
        File tmpFile = null;
        if (System.getProperty(CassandraActionListener.PREF_IMAGE_SAVE_DIR) != null) {
            tmpFile = new File(System.getProperty(CassandraActionListener.PREF_IMAGE_SAVE_DIR));
            if (tmpFile.exists()) {
                setPreference(CassandraActionListener.PREF_IMAGE_SAVE_DIR, tmpFile);
            }
        }

        if (System.getProperty(CassandraActionListener.PREF_PLUGIN_OPEN_DIR) != null) {
            tmpFile = new File(System.getProperty(CassandraActionListener.PREF_PLUGIN_OPEN_DIR));
            if (tmpFile.exists()) {
                setPreference(CassandraActionListener.PREF_PLUGIN_OPEN_DIR, tmpFile);
            }
        }

        if (System.getProperty(CassandraActionListener.PREF_VTK_FILE_OPEN_DIR) != null) {
            tmpFile = new File(System.getProperty(CassandraActionListener.PREF_VTK_FILE_OPEN_DIR));
            if (tmpFile.exists()) {
                setPreference(CassandraActionListener.PREF_VTK_FILE_OPEN_DIR, tmpFile);
            }
        }

        if (System.getProperty(CassandraGUI.PREF_SCRIPT_DIR) != null) {
            tmpFile = new File(System.getProperty(CassandraGUI.PREF_SCRIPT_DIR));
            if (tmpFile.exists()) {
                setPreference(CassandraGUI.PREF_SCRIPT_DIR, tmpFile);
            }
        }
    }

    public JComponent getDefaultUI() {
        return gui;
    }

    public CassandraMenu getDefaultMenu() {
        return menu;
    }

    public PipeLineManager getPipeLineManager() {
        return pipeLineManager;
    }

    public CassandraView getRendererPanel() {
        return pipeLineManager.getCassandraView();
    }

    public CassandraToolBar getDefaultToolBar() {
        return toolBar;
    }

    public PluginManager getPluginManager() {
        return pluginManager;
    }

    public CassandraActionListener getActionManager() {
        return actionListener;
    }

    public void loadPluginInDirectory(File pluginDir) {
        DynamicClassLoader.getInstance().loadDirectory(pluginDir);
        actionListener.reloadPlugings();
    }

    public void addPreferenceListener(PreferenceListener pl) {
        pl.setPreferences(getPreferences());
        prefListener.add(pl);
    }

    public void removePreferenceListener(PreferenceListener pl) {
        prefListener.remove(pl);
    }

    public void setPreference(String key, Object value) {
        preferences.put(key, value);
        notifyPreferenceListener();
    }

    public Hashtable getPreferences() {
        return preferences;
    }

    public void notifyPreferenceListener() {
        for (Iterator i = prefListener.iterator(); i.hasNext();) {
            ((PreferenceListener) i.next()).preferenceChanged();
        }
    }

    public static void main(String[] args) throws Exception {
        /*
           if ((System.getProperty("cassandra.skin") != null) && new File(System.getProperty("cassandra.skin")).exists()) {
           try {
           File f = new File(System.getProperty("cassandra.skin"));
           if (f.exists()) {
           // first tell SkinLF which theme to use
           Skin theSkinToUse = SkinLookAndFeel.loadThemePack(f.getAbsolutePath());
           SkinLookAndFeel.setSkin(theSkinToUse);
           }
           } catch (Exception e) {
           JOptionPane.showMessageDialog(null, "Skin error: " + e.getMessage());
           }
           }
         */
        Properties props = System.getProperties();
        String key = null;
        for (Enumeration e = props.keys(); e.hasMoreElements();) {
            key = (String) e.nextElement();
            System.out.println(key + " : " + System.getProperty(key));
        }

        Cassandra cassandra = new Cassandra();

        // Build the JFrame
        JFrame f = new JFrame("Cassandra VTK viewer");
        f.setJMenuBar(cassandra.getDefaultMenu());
        f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        f.getContentPane().add(cassandra.getDefaultToolBar(), BorderLayout.NORTH);
        f.getContentPane().add(cassandra.getDefaultUI(), BorderLayout.CENTER);
        f.setSize(600, 400);
        f.setLocationRelativeTo(null);
        //
        if (args.length == 1) {
            cassandra.loadPluginInDirectory(new File(args[0]));
        } else if (System.getProperty("cassandra.plugin.dir") != null) {
            File pluginDir = new File(System.getProperty("cassandra.plugin.dir"));
            if (pluginDir.exists()) {
                cassandra.loadPluginInDirectory(pluginDir);
            }
        }

        // set preferences done in config file now...
        /*
           File localDir = new File(".");
           cassandra.setPreference(CassandraActionListener.PREF_IMAGE_SAVE_DIR, localDir);
           cassandra.setPreference(CassandraActionListener.PREF_PLUGIN_OPEN_DIR, new File(localDir, "plugin"));
           cassandra.setPreference(CassandraActionListener.PREF_VTK_FILE_OPEN_DIR, new File(localDir, "data"));
           cassandra.setPreference(CassandraGUI.PREF_SCRIPT_DIR, new File(localDir, "script"));
         */

        // exit method
        cassandra.getActionManager().setExitAction(new SystemExit());

        //
        f.setVisible(true);
        cassandra.gui.showPipeLine();
    }
}
