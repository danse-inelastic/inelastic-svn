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
package com.artenum.cassandra.ui;

import com.artenum.cassandra.action.CassandraActionListener;
import com.artenum.cassandra.plugin.DynamicPluginMenu;

import java.awt.Component;

import java.util.ArrayList;

import javax.swing.JCheckBoxMenuItem;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;

/**
 * <pre>
 * <b>Project ref           :</b> CASSANDRA project
 * <b>Copyright and license :</b> See relevant sections
 * <b>Status                :</b> under development
 * <b>Creation              :</b> 04/03/2005
 * <b>Modification          :</b>
 *
 * <b>Description  :</b> The Cassandra Menu
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
public class CassandraMenu extends JMenuBar implements DynamicPluginMenu {
    private CassandraActionListener listener;
    private ArrayList pluginClassNameList;

    // File menu
    private JMenu file;
    private JMenuItem open;
    private JMenuItem save;
    private JMenu importFile;
    private JMenu exportFile;
    private JMenuItem saveImage;
    private JMenuItem exit;

    // Edit menu
    private JMenu edit;
    private JMenuItem loadPlugin;

    // View menu
    private JMenu view;
    private JCheckBoxMenuItem pipeLineManager;
    private JCheckBoxMenuItem renderer;
    private JCheckBoxMenuItem console;
    private JMenuItem setBg;
    private JMenuItem setAmbiantLight;
    private JCheckBoxMenuItem axis;
    private JMenuItem setTitle;

    // Source menu
    private JMenu source;

    // Filter menu
    private JMenu filter;

    // Tool menu
    private JMenu tool;

    // Help menu
    private JMenu help;
    private JMenuItem about;

    public CassandraMenu(CassandraActionListener listener) {
        this.listener = listener;
        this.pluginClassNameList = new ArrayList();
        //
        listener.setDynamicPluginMenu(this);
        listener.setParentComponent(this);
        //
        // Init global menu bar
        file = new JMenu("File");
        edit = new JMenu("Edit");
        view = new JMenu("View");
        source = new JMenu("Sources");
        filter = new JMenu("Filters");
        tool = new JMenu("Tools");
        help = new JMenu("Help");

        // File menu
        open = new JMenuItem("Open");
        open.setActionCommand(CassandraActionListener.OPEN_VTK_FILE);
        open.addActionListener(listener);
        save = new JMenuItem("Save");
        save.setActionCommand(CassandraActionListener.SAVE_VTK_FILE);
        save.addActionListener(listener);
        importFile = new JMenu("Import");
        importFile.setActionCommand(CassandraActionListener.IMPORT_DATA_FILE);
        importFile.addActionListener(listener);
        exportFile = new JMenu("Export");
        exportFile.setActionCommand(CassandraActionListener.EXPORT_DATA_FILE);
        exportFile.addActionListener(listener);
        saveImage = new JMenuItem("Save image");
        saveImage.setActionCommand(CassandraActionListener.SAVE_VTK_VIEW);
        saveImage.addActionListener(listener);
        exit = new JMenuItem("Exit");
        exit.setActionCommand(CassandraActionListener.EXIT);
        exit.addActionListener(listener);

        //
        file.add(open);
        file.add(save);
        file.addSeparator();
        file.add(importFile);
        file.add(exportFile);
        file.addSeparator();
        file.add(saveImage);
        file.addSeparator();
        file.add(exit);

        // Edit menu
        loadPlugin = new JMenuItem("Load plugin");
        loadPlugin.setActionCommand(CassandraActionListener.LOAD_PLUGIN);
        loadPlugin.addActionListener(listener);

        // 
        edit.addSeparator();
        edit.add(loadPlugin);

        // View menu
        pipeLineManager = new JCheckBoxMenuItem("View Pipeline");
        pipeLineManager.setActionCommand(CassandraActionListener.VIEW_PIPELINE);
        pipeLineManager.addActionListener(listener);
        pipeLineManager.setSelected(true);
        renderer = new JCheckBoxMenuItem("View renderer");
        renderer.setActionCommand(CassandraActionListener.VIEW_RENDERER);
        renderer.addActionListener(listener);
        renderer.setSelected(true);
        console = new JCheckBoxMenuItem("View console");
        console.setActionCommand(CassandraActionListener.VIEW_CONSOLE);
        console.addActionListener(listener);
        console.setSelected(false);
        setBg = new JMenuItem("Background color");
        setBg.setActionCommand(CassandraActionListener.SET_BG_COLOR);
        setBg.addActionListener(listener);
        setAmbiantLight = new JMenuItem("Ambiant light");
        setAmbiantLight.setActionCommand(CassandraActionListener.SET_AMBIANT_LIGHT);
        setAmbiantLight.addActionListener(listener);
        setTitle = new JMenuItem("Title");
        setTitle.setActionCommand(CassandraActionListener.SET_TITLE);
        setTitle.addActionListener(listener);
        axis = new JCheckBoxMenuItem("View axis");
        axis.setActionCommand(CassandraActionListener.VIEW_AXIS);
        axis.addActionListener(listener);
        axis.setSelected(false);

        // 
        view.add(pipeLineManager);
        view.add(renderer);
        view.add(console);
        view.addSeparator();
        view.add(setAmbiantLight);
        view.add(setBg);

        //view.add(setTitle);
        view.add(axis);

        // Help menu
        about = new JMenuItem("About");
        about.setActionCommand(CassandraActionListener.ABOUT_CASSANDRA);
        about.addActionListener(listener);

        //
        help.add(about);

        // Build menu bar
        add(file);
        add(edit);
        add(view);
        add(source);
        add(filter);
        add(tool);
        add(help);
    }

    public void addImportMenuComponent(Component importComponent) {
        importFile.add(importComponent);
    }

    public void addExportMenuComponent(Component exportComponent) {
        exportFile.add(exportComponent);
    }

    public void addSourceMenuComponent(Component sourceComponent) {
        source.add(sourceComponent);
    }

    public void addFilterMenuComponent(Component filterComponent) {
        filter.add(filterComponent);
    }

    public void addToolMenuComponent(Component toolComponent) {
        tool.add(toolComponent);
    }
}
