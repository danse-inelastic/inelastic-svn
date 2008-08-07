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
package com.artenum.cassandra.util;

import com.artenum.cassandra.pipeline.VtkObject;
import com.artenum.cassandra.pipeline.VtkObjectListModel;

import javax.swing.ComboBoxModel;
import javax.swing.event.ListDataEvent;
import javax.swing.event.ListDataListener;

/**
 * <pre>
 * <b>Project ref           :</b> CASSANDRA project
 * <b>Copyright and license :</b> See relevant sections
 * <b>Status                :</b> under development
 * <b>Creation              :</b> 04/03/2005
 * <b>Modification          :</b>
 *
 * <b>Description  :</b> Convert a VtkObjectListModel to a VtkObjectComboBoxModel
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
public class VtkObjectComboBoxModel implements ComboBoxModel, ListDataListener {
    private VtkObject filteredItem;
    private VtkObject selectedItem;
    private VtkObjectListModel listModel;
    private int filteredIndex = -1;

    public VtkObjectComboBoxModel(VtkObjectListModel listModel, VtkObject filteredItem) {
        this.filteredItem = filteredItem;
        this.listModel = listModel;
        this.filteredIndex = listModel.getVtkObjectIndex(filteredItem);
        this.listModel.addListDataListener(this);
    }

    public Object getSelectedItem() {
        return selectedItem;
    }

    public void setSelectedItem(Object anItem) {
        this.selectedItem = (VtkObject) anItem;
    }

    public void setSelectedEncapsulateItem(Object anItem) {
        this.selectedItem = listModel.getVtkObject(anItem);
    }

    public int getSize() {
        return listModel.getSize() - ((filteredIndex != -1) ? 1 : 0);
    }

    public Object getElementAt(int index) {
        if ((filteredIndex != -1) && (filteredIndex < index)) {
            index--;
        }

        return listModel.getElementAt(index);
    }

    public void addListDataListener(ListDataListener l) {
        listModel.addListDataListener(l);
    }

    public void removeListDataListener(ListDataListener l) {
        listModel.removeListDataListener(l);
    }

    public void contentsChanged(ListDataEvent e) {
        this.filteredIndex = listModel.getVtkObjectIndex(filteredItem);
    }

    public void intervalAdded(ListDataEvent e) {
        this.filteredIndex = listModel.getVtkObjectIndex(filteredItem);
    }

    public void intervalRemoved(ListDataEvent e) {
        this.filteredIndex = listModel.getVtkObjectIndex(filteredItem);
    }
}
