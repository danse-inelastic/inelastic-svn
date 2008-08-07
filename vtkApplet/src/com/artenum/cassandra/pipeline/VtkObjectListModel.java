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
package com.artenum.cassandra.pipeline;

import java.awt.Color;
import java.awt.Component;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Iterator;

import javax.swing.AbstractListModel;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.ListCellRenderer;

/**
 * <pre>
 * <b>Project ref           :</b> CASSANDRA project
 * <b>Copyright and license :</b> See relevant sections
 * <b>Status                :</b> under development
 * <b>Creation              :</b> 04/03/2005
 * <b>Modification          :</b>
 *
 * <b>Description  :</b> A ListModel model made for VtkObjects
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
public class VtkObjectListModel extends AbstractListModel implements ListCellRenderer {
    private ArrayList vtkObjectList;
    private JLabel renderer;
    private Color selectedColor;
    private Color defaultColor;
    private int modelType;
    private boolean showTypeError = false;

    public VtkObjectListModel(int modelType) {
        vtkObjectList = new ArrayList();
        renderer = new JLabel();
        renderer.setOpaque(true);
        selectedColor = new Color(100, 100, 200);
        defaultColor = Color.white;
        this.modelType = modelType;
    }

    public void setPrefference(Color selectedColor, Color defaultColor, boolean showTypeError) {
        if (selectedColor != null) {
            this.selectedColor = selectedColor;
        }

        if (defaultColor != null) {
            this.defaultColor = defaultColor;
        }

        this.showTypeError = showTypeError;
    }

    public int getSize() {
        return vtkObjectList.size();
    }

    public Object getElementAt(int index) {
        return vtkObjectList.get(index);
    }

    public void addVtkObject(VtkObject vtkObject) {
        if (vtkObject.getType() == modelType) {
            vtkObjectList.add(vtkObject);
            fireIntervalAdded(this, getSize() - 1, getSize() - 1);
        } else if (showTypeError) {
            System.err.println("Try to ADD invalide type in the VtkObjectListModel. (Expected: " + modelType + " / Got: " + vtkObject.getType() + ")");
        }
    }

    public void removeVtkObject(VtkObject vtkObject) {
        if (vtkObject.getType() == modelType) {
            int index = vtkObjectList.indexOf(vtkObject);
            if (index != -1) {
                vtkObjectList.remove(index);
            }

            fireIntervalRemoved(this, index, index);
        } else if (showTypeError) {
            System.err.println("Try to REMOVE invalide type in the VtkObjectListModel. (Expected: " + modelType + " / Got: " + vtkObject.getType() + ")");
        }
    }

    public VtkObject getVtkObject(int index) {
        return ((VtkObject) getElementAt(index));
    }

    public VtkObject getVtkObject(Object encapsulateObject) {
        VtkObject currentObject;
        for (Iterator i = vtkObjectList.iterator(); i.hasNext();) {
            currentObject = ((VtkObject) i.next());
            if (currentObject.getVtkObject().equals(encapsulateObject)) {
                return currentObject;
            }
        }

        return null;
    }

    public int getVtkObjectIndex(VtkObject vtkObject) {
        return vtkObjectList.indexOf(vtkObject);
    }

    public VtkObject getLastVtkObject() {
        return getVtkObject(getSize() - 1);
    }

    public Component getListCellRendererComponent(JList list, Object value, int index, boolean isSelected, boolean cellHasFocus) {
        renderer.setBackground(isSelected ? selectedColor : defaultColor);
        VtkObject vtkObject = (VtkObject) value;
        renderer.setText(vtkObject.getName() + " (" + index + ")");
        return renderer;
    }

    public Collection getData() {
        return vtkObjectList;
    }
}
