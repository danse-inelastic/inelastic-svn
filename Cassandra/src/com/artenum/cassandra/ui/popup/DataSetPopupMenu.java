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

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

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
 * <b>Description  :</b> Dataset popup menu.
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
public class DataSetPopupMenu extends JPopupMenu implements ActionListener, VtkObjectPopupMenu {
    // Actions
    public final static String DATASET_REMOVE = "dataset.remove";
    private PipeLineManager pipeLineManager;
    private CascadeRemoveManager cascadeRemoveManager;
    private VtkObject currentVtkObject;

    // UI components
    private RenameVtkObject datasetRename;
    private JMenuItem datasetRemove;

    public DataSetPopupMenu(PipeLineManager pipeLineManager, CascadeRemoveManager cascadeRemoveManager) {
        this.pipeLineManager = pipeLineManager;
        this.cascadeRemoveManager = cascadeRemoveManager;
        // Init popup ui
        datasetRename = new RenameVtkObject("Rename", "Rename dataset", null);
        add(datasetRename);
        addSeparator();
        datasetRemove = new JMenuItem("Remove");
        datasetRemove.setActionCommand(DATASET_REMOVE);
        datasetRemove.addActionListener(this);
        add(datasetRemove);
    }

    public void setCurrentVtkOject(VtkObject currentVtkObject) {
        this.currentVtkObject = currentVtkObject;
        datasetRename.setVtkObject(currentVtkObject);
        // init popup with current vtkObject
    }

    public void actionPerformed(ActionEvent e) {
        String command = e.getActionCommand();
        if (command.equals(DATASET_REMOVE)) {
            cascadeRemoveManager.removeDataSet(currentVtkObject);
        }
    }
}
