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

import com.artenum.cassandra.pipeline.PipeLineManager;
import com.artenum.cassandra.pipeline.VtkObject;
import com.artenum.cassandra.pipeline.VtkObjectListModel;

import java.awt.BorderLayout;
import java.awt.Color;

import javax.swing.BorderFactory;
import javax.swing.BoxLayout;
import javax.swing.JPanel;
import javax.swing.JTable;
import javax.swing.event.ListDataEvent;
import javax.swing.event.ListDataListener;
import javax.swing.event.TableModelEvent;
import javax.swing.table.AbstractTableModel;

/**
 * <pre>
 * <b>Project ref           :</b> CASSANDRA project
 * <b>Copyright and license :</b> See relevant sections
 * <b>Status                :</b> under development
 * <b>Creation              :</b> 04/03/2005
 * <b>Modification          :</b>
 *
 * <b>Description  :</b> JTable of 3D actors with checkbox for changing the visibility of those actors.
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
public class ActorList extends JPanel {
    private ActorTableModel[] model;
    private PipeLineManager pipeLineManager;
    private JTable[] table;

    public ActorList(String[] titles, VtkObjectListModel[] listModel, PipeLineManager pipeLineManager) {
        this.pipeLineManager = pipeLineManager;
        this.model = new ActorTableModel[listModel.length];
        this.table = new JTable[listModel.length];
        // 
        setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
        for (int i = 0; i < listModel.length; i++) {
            this.model[i] = new ActorTableModel(listModel[i]);
            this.table[i] = new JTable(this.model[i]);
            this.table[i].getColumnModel().getColumn(0).setPreferredWidth(40);
            this.table[i].getColumnModel().getColumn(0).setMaxWidth(40);
            this.table[i].getColumnModel().getColumn(0).setMinWidth(40);
            this.table[i].getColumnModel().getColumn(1).setPreferredWidth(150);
            this.table[i].getColumnModel().getColumn(1).setMaxWidth(2000);
            this.table[i].getColumnModel().getColumn(1).setMinWidth(20);
            JPanel content = new JPanel(new BorderLayout());
            content.add(table[i], BorderLayout.CENTER);
            content.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.BLACK), titles[i]));
            add(content);
        }
    }

    class ActorTableModel extends AbstractTableModel implements ListDataListener {
        private VtkObjectListModel model;
        private String[] columnNames;

        public ActorTableModel(VtkObjectListModel model) {
            this.model = model;
            model.addListDataListener(this);
            columnNames = new String[] { "Visible", "Actor name" };
        }

        public int getColumnCount() {
            return 2;
        }

        public int getRowCount() {
            return model.getSize();
        }

        public Object getValueAt(int rowIndex, int columnIndex) {
            VtkObject vtkObject = model.getVtkObject(rowIndex);
            switch (columnIndex) {
            case 0:
                return Boolean.valueOf((String) vtkObject.getMetaData().get(VtkObject.ACTOR_VISIBLE));
            case 1:
                return vtkObject.getName();
            }

            return null;
        }

        public void contentsChanged(ListDataEvent e) {
            TableModelEvent te = new TableModelEvent(this, e.getIndex0(), e.getIndex1());
            fireTableChanged(te);
        }

        public void intervalAdded(ListDataEvent e) {
            fireTableRowsInserted(e.getIndex0(), e.getIndex1());
        }

        public void intervalRemoved(ListDataEvent e) {
            fireTableRowsDeleted(e.getIndex0(), e.getIndex1());
        }

        public boolean isCellEditable(int row, int col) {
            return col == 0;
        }

        public Class getColumnClass(int c) {
            if (c == 0) {
                return Boolean.class;
            }

            return getValueAt(0, c).getClass();
        }

        public void setValueAt(Object value, int row, int col) {
            VtkObject vtkObject = model.getVtkObject(row);
            pipeLineManager.setActorVisible(vtkObject, ((Boolean) value).booleanValue());
            pipeLineManager.validateViewAndGo();
            //vtkObject.getMetaData().put(VtkObject.ACTOR_VISIBLE, value.toString());
            fireTableCellUpdated(row, col);
        }

        public String getColumnName(int col) {
            return columnNames[col];
        }
    }
}
