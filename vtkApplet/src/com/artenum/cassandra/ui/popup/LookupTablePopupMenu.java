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
package com.artenum.cassandra.ui.popup;

import com.artenum.cassandra.action.menu.RenameVtkObject;
import com.artenum.cassandra.pipeline.CascadeRemoveManager;
import com.artenum.cassandra.pipeline.PipeLineManager;
import com.artenum.cassandra.pipeline.VtkObject;
import com.artenum.cassandra.ui.dialog.LookUpTableControlDialog;
import com.artenum.cassandra.util.CassandraToolBox;

import vtk.vtkLookupTable;
import vtk.vtkMapper;

import java.awt.Component;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import java.util.Hashtable;
import java.util.Iterator;

import javax.swing.JMenu;
import javax.swing.JMenuItem;
import javax.swing.JPopupMenu;

/**
 * <pre>
 * <b>Project ref           :</b> CASSANDRA project
 * <b>Copyright and license :</b> See relevant sections
 * <b>Status                :</b> under development
 * <b>Creation              :</b> 04/03/2005
 * <b>Modification          :</b>
 *
 * <b>Description  :</b> Lookup table popup menu.
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
public class LookupTablePopupMenu extends JPopupMenu implements ActionListener, VtkObjectPopupMenu {
    // Actions
    public final static String LOOKUP_TABLE_SHOW_CONTROL = "lookup.table.control";
    public final static String LOOKUP_TABLE_REMOVE = "lookup.table.remove";
    private PipeLineManager pipeLineManager;
    private CascadeRemoveManager cascadeRemoveManager;
    private VtkObject currentVtkObject;
    private Hashtable controlDialogTable;

    // UI components
    private JMenuItem showControl;
    private RenameVtkObject lookupTableRename;
    private JMenuItem lookupTableRemove;
    private JMenu mapperList;

    public LookupTablePopupMenu(PipeLineManager pipeLineManager, CascadeRemoveManager cascadeRemoveManager) {
        this.pipeLineManager = pipeLineManager;
        this.cascadeRemoveManager = cascadeRemoveManager;
        this.controlDialogTable = new Hashtable();
        // Init popup ui
        showControl = new JMenuItem("Show control");
        showControl.setActionCommand(LOOKUP_TABLE_SHOW_CONTROL);
        showControl.addActionListener(this);
        add(showControl);
        mapperList = new JMenu("Link to mapper...");
        add(mapperList);
        lookupTableRename = new RenameVtkObject("Rename", "Rename lookup table", null);
        add(lookupTableRename);
        addSeparator();
        lookupTableRemove = new JMenuItem("Remove");
        lookupTableRemove.setActionCommand(LOOKUP_TABLE_REMOVE);
        lookupTableRemove.addActionListener(this);
        add(lookupTableRemove);
    }

    private void updateMapperList() {
        VtkObject mapper = null;
        mapperList.removeAll();
        JMenuItem item = null;
        for (Iterator i = pipeLineManager.getMapperList().getData().iterator(); i.hasNext();) {
            mapper = (VtkObject) i.next();
            item = new JMenuItem(mapper.getName());
            item.addActionListener(new LookupTableSetter((vtkMapper) mapper.getVtkObject()));
            mapperList.add(item);
        }
    }

    public void setCurrentVtkOject(VtkObject currentVtkObject) {
        this.currentVtkObject = currentVtkObject;
        lookupTableRename.setVtkObject(currentVtkObject);
        // init popup with current vtkObject
        updateMapperList();
        if (controlDialogTable.get(currentVtkObject) != null) {
            ((LookUpTableControlDialog) controlDialogTable.get(currentVtkObject)).setLookupTable(currentVtkObject);
        }
    }

    public void actionPerformed(ActionEvent e) {
        String command = e.getActionCommand();
        if (command.equals(LOOKUP_TABLE_REMOVE)) {
            cascadeRemoveManager.removeLookupTable(currentVtkObject);
        } else if (command.equals(LOOKUP_TABLE_SHOW_CONTROL)) {
            ((LookUpTableControlDialog) controlDialogTable.get(currentVtkObject)).setVisible(true);
        }
    }

    public void show(Component invoker, int x, int y) {
        if (((LookUpTableControlDialog) controlDialogTable.get(currentVtkObject)) == null) {
            controlDialogTable.put(currentVtkObject, new LookUpTableControlDialog(CassandraToolBox.getParentFrame(invoker), pipeLineManager));
            ((LookUpTableControlDialog) controlDialogTable.get(currentVtkObject)).setLookupTable(currentVtkObject);
        }

        updateMapperList();

        super.show(invoker, x, y);
    }

    private class LookupTableSetter implements ActionListener {
        private vtkMapper mapper;

        public LookupTableSetter(vtkMapper mapper) {
            this.mapper = mapper;
        }

        public void actionPerformed(ActionEvent e) {
            mapper.SetLookupTable((vtkLookupTable) currentVtkObject.getVtkObject());
            CassandraToolBox.updateMapper(pipeLineManager, (vtkLookupTable) currentVtkObject.getVtkObject());
            pipeLineManager.notifyConnectivityChange(currentVtkObject);
            pipeLineManager.validateViewAndGo();
        }
    }
}
