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
package com.artenum.cassandra.action;

import com.artenum.cassandra.PreferenceListener;
import com.artenum.cassandra.launcher.DynamicClassLoader;
import com.artenum.cassandra.pipeline.PipeLineManager;
import com.artenum.cassandra.plugin.CassandraPluginIntegrator;
import com.artenum.cassandra.plugin.DynamicPluginMenu;
import com.artenum.cassandra.plugin.PluginManager;
import com.artenum.cassandra.ui.CassandraGUI;
import com.artenum.cassandra.ui.CassandraHelp;
import com.artenum.cassandra.util.CassandraToolBox;

import java.awt.Color;
import java.awt.Component;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import java.io.File;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.Iterator;

import javax.swing.JCheckBoxMenuItem;
import javax.swing.JColorChooser;
import javax.swing.JDialog;
import javax.swing.JFileChooser;
import javax.swing.filechooser.FileFilter;

/**
 * <pre>
 * <b>Project ref           :</b> CASSANDRA project
 * <b>Copyright and license :</b> See relevant sections
 * <b>Status                :</b> under development
 * <b>Creation              :</b> 04/03/2005
 * <b>Modification          :</b>
 *
 * <b>Description  :</b> Manage menu and toolbar actions of Cassandra
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
public class CassandraActionListener implements ActionListener, PreferenceListener {
    public final static String LOAD_PLUGIN = "LOAD_PLUGIN";
    public final static String OPEN_VTK_FILE = "OPEN_VTK_FILE";
    public final static String SAVE_VTK_FILE = "SAVE_VTK_FILE";
    public final static String IMPORT_DATA_FILE = "IMPORT_DATA_FILE";
    public final static String EXPORT_DATA_FILE = "EXPORT_DATA_FILE";
    public final static String SAVE_VTK_VIEW = "SAVE_VTK_VIEW";
    public final static String EXIT = "EXIT";
    public final static String ABOUT_CASSANDRA = "ABOUT_CASSANDRA";
    public final static String VIEW_RENDERER = "RENDERER";
    public final static String VIEW_CONSOLE = "CONSOLE";
    public final static String VIEW_PIPELINE = "PIPELINE";
    public final static String SET_BG_COLOR = "SET_BG_COLOR";
    public final static String SET_AMBIANT_LIGHT = "SET_AMBIANT_LIGHT";
    public final static String VIEW_AXIS = "AXIS";
    public final static String SET_TITLE = "SET_TITLE";
    public final static String SET_VIEW_XY = "SET_VIEW_XY";
    public final static String SET_VIEW_XZ = "SET_VIEW_XZ";
    public final static String SET_VIEW_YZ = "SET_VIEW_YZ";
    public final static String RESET_VIEW = "RESET_VIEW";

    // pref
    public static final String PREF_PLUGIN_OPEN_DIR = "cassandra.pref.plugin.dir";
    public static final String PREF_VTK_FILE_OPEN_DIR = "cassandra.pref.vtk.file.dir";
    public static final String PREF_IMAGE_SAVE_DIR = "cassandra.pref.image.save.dir";
    private PipeLineManager pipeLineManager;
    private CassandraGUI view;
    private PluginManager pluginManager;
    private Component parentComponent;
    private DynamicPluginMenu dynamicPluginMenu;
    private ArrayList pluginClassNameList;
    private JDialog about;
    private ExitAction exitAction;
    private Hashtable prefTable;
    private File pluginDir;
    private File openVtkFileDir;
    private File imageSaveDir;

    public CassandraActionListener(CassandraGUI view, PipeLineManager pipeLineManager, PluginManager pluginManager) {
        this.pipeLineManager = pipeLineManager;
        this.pluginManager = pluginManager;
        this.view = view;
        pluginClassNameList = new ArrayList();
    }

    public void actionPerformed(ActionEvent e) {
        String actionCommand = e.getActionCommand();
        if (actionCommand.equals(LOAD_PLUGIN)) {
            JFileChooser chooser = new JFileChooser();
            if (pluginDir != null) {
                chooser.setCurrentDirectory(pluginDir);
            }

            chooser.setMultiSelectionEnabled(true);
            chooser.setFileFilter(new FileFilter() {
                    public boolean accept(File f) {
                        return f.isDirectory() || f.getName().endsWith(".jar");
                    }

                    public String getDescription() {
                        return "Jar files";
                    }
                });
            if (chooser.showOpenDialog(parentComponent) == JFileChooser.APPROVE_OPTION) {
                File[] jarFiles = chooser.getSelectedFiles();
                for (int i = 0; i < jarFiles.length; i++) {
                    if (jarFiles[i].isFile()) {
                        DynamicClassLoader.getInstance().addJar(jarFiles[i]);
                    }
                }

                reloadPlugings();
            }
        } else if (actionCommand.equals(SET_VIEW_XY)) {
            pipeLineManager.getCassandraView().setXYView();
            pipeLineManager.validateViewAndGo();
        } else if (actionCommand.equals(SET_VIEW_XZ)) {
            pipeLineManager.getCassandraView().setXZView();
            pipeLineManager.validateViewAndGo();
        } else if (actionCommand.equals(SET_VIEW_YZ)) {
            pipeLineManager.getCassandraView().setYZView();
            pipeLineManager.validateViewAndGo();
        } else if (actionCommand.equals(RESET_VIEW)) {
            pipeLineManager.getCassandraView().resetCamera();
            pipeLineManager.validateViewAndGo();
        } else if (actionCommand.equals(EXIT)) {
            if (exitAction == null) {
                System.exit(0);
            } else {
                exitAction.exit();
            }
        } else if (actionCommand.equals(OPEN_VTK_FILE)) {
            JFileChooser chooser = new JFileChooser();
            if (openVtkFileDir != null) {
                chooser.setCurrentDirectory(openVtkFileDir);
            }

            chooser.setMultiSelectionEnabled(true);
            chooser.setFileFilter(new FileFilter() {
                    public boolean accept(File f) {
                        return f.isDirectory() || f.getName().endsWith(".vtk");
                    }

                    public String getDescription() {
                        return "Vtk files";
                    }
                });

            if (chooser.showOpenDialog(view) == JFileChooser.APPROVE_OPTION) {
                File[] vtkFiles = chooser.getSelectedFiles();
                CassandraToolBox.sortFileList(vtkFiles);
                for (int i = 0; i < vtkFiles.length; i++)
                    pipeLineManager.addVtkFile(vtkFiles[i]);
            }

            pipeLineManager.validateViewAndGo();
        } else if (actionCommand.equals(VIEW_CONSOLE)) {
            if (((JCheckBoxMenuItem) e.getSource()).isSelected()) {
                view.showConsole();
            } else {
                view.hideConsole();
            }

            pipeLineManager.deepValidateView();
        } else if (actionCommand.equals(SET_BG_COLOR)) {
            Color c = JColorChooser.showDialog(view, "Background color", Color.BLACK);
            if (c != null) {
                pipeLineManager.getCassandraView().setBackground(c);
            }

            pipeLineManager.validateViewAndGo();
        } else if (actionCommand.equals(SET_AMBIANT_LIGHT)) {
            Color c = JColorChooser.showDialog(view, "Ambiant light", Color.BLACK);
            if (c != null) {
                pipeLineManager.getCassandraView().setAmbiantLight(c);
            }

            pipeLineManager.validateViewAndGo();
        } else if (actionCommand.equals(SET_TITLE)) {}
        else if (actionCommand.equals(VIEW_AXIS)) {
            pipeLineManager.setAxisVisible(((JCheckBoxMenuItem) e.getSource()).isSelected());
            pipeLineManager.validateViewAndGo();
        } else if (actionCommand.equals(VIEW_PIPELINE)) {
            if (((JCheckBoxMenuItem) e.getSource()).isSelected()) {
                view.showPipeLine();
            } else {
                view.hidePipeLine();
            }

            pipeLineManager.deepValidateView();
        } else if (actionCommand.equals(SAVE_VTK_VIEW)) {
            JFileChooser chooser = new JFileChooser();
            if (imageSaveDir != null) {
                chooser.setCurrentDirectory(imageSaveDir);
            }

            chooser.setFileFilter(new FileFilter() {
                    public boolean accept(File f) {
                        if (f.isDirectory()) {
                            return true;
                        }

                        if (f.isFile() && (f.getName().toLowerCase().endsWith(".tif") || f.getName().toLowerCase().endsWith(".tiff"))) {
                            return true;
                        }

                        return false;
                    }

                    public String getDescription() {
                        return "Tiff image file";
                    }
                });
            chooser.showSaveDialog(view);
            File fileToSave = chooser.getSelectedFile();
            if (fileToSave != null) {
                String filePath = fileToSave.getAbsolutePath();
                if (!(filePath.toLowerCase().endsWith(".tif") || filePath.toLowerCase().endsWith(".tiff"))) {
                    filePath += ".tiff";
                }

                pipeLineManager.getCassandraView().HardCopy(filePath, 1);
            }
        } else if (actionCommand.equals(VIEW_RENDERER)) {
            if (((JCheckBoxMenuItem) e.getSource()).isSelected()) {
                view.showRenderer();
            } else {
                view.hideRenderer();
            }

            pipeLineManager.deepValidateView();
        } else if (actionCommand.equals(ABOUT_CASSANDRA)) {
            if (about == null) {
                about = new CassandraHelp(view);
            }

            about.setLocationRelativeTo(null);
            about.setVisible(true);
        } else {
            System.out.println(actionCommand);
        }
    }

    public void reloadPlugings() {
        // Update menus
        for (Iterator i = DynamicClassLoader.getInstance().getPluginIntegratorList().iterator(); i.hasNext();) {
            String className = (String) i.next();
            if (!pluginClassNameList.contains(className)) {
                pluginClassNameList.add(className);
                try {
                    ((CassandraPluginIntegrator) DynamicClassLoader.getInstance().getPluginIntegrator(className)).integratePluginsInFramework(pipeLineManager,
                        pluginManager, dynamicPluginMenu);
                } catch (Exception e1) {
                    e1.printStackTrace();
                }
            }
        }
    }

    public void setDynamicPluginMenu(DynamicPluginMenu dynaPluginMenu) {
        this.dynamicPluginMenu = dynaPluginMenu;
    }

    public void setParentComponent(Component parentComponent) {
        this.parentComponent = parentComponent;
    }

    public void setExitAction(ExitAction exitAction) {
        this.exitAction = exitAction;
    }

    public void setPreferences(Hashtable prefTable) {
        this.prefTable = prefTable;
    }

    public void preferenceChanged() {
        if (prefTable != null) {
            imageSaveDir = (File) prefTable.get(PREF_IMAGE_SAVE_DIR);
            pluginDir = (File) prefTable.get(PREF_PLUGIN_OPEN_DIR);
            openVtkFileDir = (File) prefTable.get(PREF_VTK_FILE_OPEN_DIR);
        }
    }
}
