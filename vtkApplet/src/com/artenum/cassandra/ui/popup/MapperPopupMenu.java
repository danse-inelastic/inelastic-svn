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

import vtk.vtkLookupTable;
import vtk.vtkMapper;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import java.util.Iterator;

import javax.swing.JCheckBoxMenuItem;
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
 * <b>Description  :</b> Mapper popup menu.
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
public class MapperPopupMenu extends JPopupMenu implements ActionListener, VtkObjectPopupMenu {
    // Actions
    public final static String MAPPER_SCALAR_VISIBILITY = "mapper.scalar.visibility";
    public final static String MAPPER_REMOVE = "mapper.remove";
    private PipeLineManager pipeLineManager;
    private CascadeRemoveManager cascadeRemoveManager;
    private VtkObject currentVtkObject;

    // UI components
    private JCheckBoxMenuItem viewScalarData;
    private JCheckBoxMenuItem chooseLookupTable;
    private RenameVtkObject mapperRename;
    private JMenuItem mapperRemove;
    private JMenu lookupTableList;

    public MapperPopupMenu(PipeLineManager pipeLineManager, CascadeRemoveManager cascadeRemoveManager) {
        this.pipeLineManager = pipeLineManager;
        this.cascadeRemoveManager = cascadeRemoveManager;
        // Init popup ui
        viewScalarData = new JCheckBoxMenuItem("View scalar data");
        viewScalarData.setActionCommand(MAPPER_SCALAR_VISIBILITY);
        viewScalarData.addActionListener(this);
        add(viewScalarData);
        lookupTableList = new JMenu("Link to lookup table...");
        add(lookupTableList);
        mapperRename = new RenameVtkObject("Rename", "Rename mapper", null);
        add(mapperRename);
        addSeparator();
        mapperRemove = new JMenuItem("Remove");
        mapperRemove.setActionCommand(MAPPER_REMOVE);
        mapperRemove.addActionListener(this);
        add(mapperRemove);
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

    public void setCurrentVtkOject(VtkObject currentVtkObject) {
        this.currentVtkObject = currentVtkObject;
        mapperRename.setVtkObject(currentVtkObject);
        // init popup with current vtkObject
        updateLookupTableList();
        viewScalarData.setSelected(((vtkMapper) currentVtkObject.getVtkObject()).GetScalarVisibility() == 1);
    }

    public void actionPerformed(ActionEvent e) {
        String command = e.getActionCommand();
        if (command.equals(MAPPER_SCALAR_VISIBILITY)) {
            ((vtkMapper) currentVtkObject.getVtkObject()).SetScalarVisibility((((vtkMapper) currentVtkObject.getVtkObject()).GetScalarVisibility() + 1) % 2);
            pipeLineManager.validateViewAndGo();
        } else if (command.equals(MAPPER_REMOVE)) {
            cascadeRemoveManager.removeMapper(currentVtkObject);
        }
    }

    private class LookupTableSetter implements ActionListener {
        private vtkLookupTable lookupTable;

        public LookupTableSetter(vtkLookupTable lookupTable) {
            this.lookupTable = lookupTable;
        }

        public void actionPerformed(ActionEvent e) {
            ((vtkMapper) currentVtkObject.getVtkObject()).SetLookupTable(lookupTable);
            pipeLineManager.notifyConnectivityChange(currentVtkObject);
            pipeLineManager.validateViewAndGo();
        }
    }
}
