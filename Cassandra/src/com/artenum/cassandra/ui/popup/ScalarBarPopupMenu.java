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
import com.artenum.cassandra.ui.dialog.ScalarBarControlDialog;
import com.artenum.cassandra.util.CassandraToolBox;

import vtk.vtkLookupTable;
import vtk.vtkScalarBarActor;

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
 * <b>Description  :</b> Scalar bar popup menu.
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
public class ScalarBarPopupMenu extends JPopupMenu implements ActionListener, VtkObjectPopupMenu {
    // Actions
    public final static String SCALAR_BAR_REMOVE = "scalar.bar.remove";
    public final static String SCALAR_BAR_CONTROL = "scalar.bar.control";
    private PipeLineManager pipeLineManager;
    private CascadeRemoveManager cascadeRemoveManager;
    private VtkObject currentVtkObject;
    private Hashtable controlDialogTable;

    // UI components
    private ActorPopupMenu actorMenu;
    private JMenuItem showControl;
    private RenameVtkObject scalarBarRename;
    private JMenuItem scalarBarRemove;
    private JMenu lookupTableList;

    public ScalarBarPopupMenu(PipeLineManager pipeLineManager, CascadeRemoveManager cascadeRemoveManager) {
        this.pipeLineManager = pipeLineManager;
        this.cascadeRemoveManager = cascadeRemoveManager;
        this.controlDialogTable = new Hashtable();
        // UI init
        actorMenu = new ActorPopupMenu(pipeLineManager, cascadeRemoveManager);
        add(actorMenu.getActorVisibleMenuItem());
        add(actorMenu.getActorOpacityMenuItem());
        addSeparator();
        showControl = new JMenuItem("Show control");
        showControl.setActionCommand(SCALAR_BAR_CONTROL);
        showControl.addActionListener(this);
        add(showControl);
        lookupTableList = new JMenu("Link to lookup table...");
        add(lookupTableList);
        scalarBarRename = new RenameVtkObject("Rename", "Rename scalar bar", null);
        add(scalarBarRename);
        addSeparator();
        scalarBarRemove = new JMenuItem("Remove");
        scalarBarRemove.setActionCommand(SCALAR_BAR_REMOVE);
        scalarBarRemove.addActionListener(this);
        add(scalarBarRemove);
    }

    public void setCurrentVtkOject(VtkObject currentVtkObject) {
        this.currentVtkObject = currentVtkObject;
        scalarBarRename.setVtkObject(currentVtkObject);
        // init popup with current vtkObject
        updateLookupTableList();
        actorMenu.setCurrentVtkOject(currentVtkObject);
        if (controlDialogTable.get(currentVtkObject) != null) {
            ((ScalarBarControlDialog) controlDialogTable.get(currentVtkObject)).setScalarBar(currentVtkObject);
        }
    }

    private void updateLookupTableList() {
        VtkObject lookupTable = null;
        lookupTableList.removeAll();
        JMenuItem item = null;
        for (Iterator i = pipeLineManager.getLookupTableList().getData().iterator(); i.hasNext();) {
            lookupTable = (VtkObject) i.next();
            item = new JMenuItem(lookupTable.getName());
            item.addActionListener(new LookupTableSetter((vtkLookupTable) lookupTable.getVtkObject()));
            lookupTableList.add(item);
        }
    }

    public void actionPerformed(ActionEvent e) {
        String command = e.getActionCommand();
        if (command.equals(SCALAR_BAR_REMOVE)) {
            cascadeRemoveManager.removeScalarBar(currentVtkObject);
        } else if (command.equals(SCALAR_BAR_CONTROL)) {
            ((ScalarBarControlDialog) controlDialogTable.get(currentVtkObject)).setVisible(true);
        }
    }

    public void show(Component invoker, int x, int y) {
        if (((ScalarBarControlDialog) controlDialogTable.get(currentVtkObject)) == null) {
            controlDialogTable.put(currentVtkObject, new ScalarBarControlDialog(CassandraToolBox.getParentFrame(invoker), pipeLineManager));
            ((ScalarBarControlDialog) controlDialogTable.get(currentVtkObject)).setScalarBar(currentVtkObject);
        }

        super.show(invoker, x, y);
    }

    private class LookupTableSetter implements ActionListener {
        private vtkLookupTable lookupTable;

        public LookupTableSetter(vtkLookupTable lookupTable) {
            this.lookupTable = lookupTable;
        }

        public void actionPerformed(ActionEvent e) {
            ((vtkScalarBarActor) currentVtkObject.getVtkObject()).SetLookupTable(lookupTable);
            pipeLineManager.notifyConnectivityChange(currentVtkObject);
            pipeLineManager.validateViewAndGo();
        }
    }
}
