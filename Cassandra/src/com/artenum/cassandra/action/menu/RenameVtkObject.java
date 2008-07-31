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
package com.artenum.cassandra.action.menu;

import com.artenum.cassandra.pipeline.VtkObject;
import com.artenum.cassandra.pipeline.graph.VtkObjectCellAdapter;
import com.artenum.cassandra.pipeline.graph.VtkObjectUI;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JMenuItem;
import javax.swing.JOptionPane;

/**
 * <pre>
 * <b>Project ref           :</b> CASSANDRA project
 * <b>Copyright and license :</b> See relevant sections
 * <b>Status                :</b> under development
 * <b>Creation              :</b> 04/03/2005
 * <b>Modification          :</b>
 *
 * <b>Description  :</b> MenuItem for renaming a VtkObject.
 *                This menu item can be used in any popup menu
 *                that require this function.
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
public class RenameVtkObject extends JMenuItem implements ActionListener {
    private VtkObject currentVtkObject;
    private String title;

    public RenameVtkObject(String itemName, String title, VtkObject object) {
        super(itemName);
        addActionListener(this);
        //
        this.currentVtkObject = object;
        this.title = title;
    }

    public void setVtkObject(VtkObject obj) {
        this.currentVtkObject = obj;
    }

    public void setTitle(String newTitle) {
        this.title = newTitle;
    }

    public void actionPerformed(ActionEvent e) {
        String newName = JOptionPane.showInputDialog(this, title);
        if (newName != null) {
            currentVtkObject.setName(newName);
            ((VtkObjectUI) ((VtkObjectCellAdapter) currentVtkObject.getMetaData().get(VtkObject.CELL)).getUI()).setName(newName);
        }
    }
}
