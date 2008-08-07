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

import com.artenum.cassandra.pipeline.CassandraTreeModel;
import com.artenum.cassandra.pipeline.PipeLineManager;
import com.artenum.cassandra.pipeline.VtkObject;
import com.artenum.cassandra.plugin.CassandraPlugin;
import com.artenum.cassandra.plugin.PluginManager;

import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;

import javax.swing.JTree;
import javax.swing.tree.DefaultMutableTreeNode;

/**
 * <pre>
 * <b>Project ref           :</b> CASSANDRA project
 * <b>Copyright and license :</b> See relevant sections
 * <b>Status                :</b> under development
 * <b>Creation              :</b> 04/03/2005
 * <b>Modification          :</b>
 *
 * <b>Description  :</b> The JTree pipeline view.
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
public class CassandraTree extends JTree {
    private CassandraTreeModel treeModel;
    private VtkObjectPopupMenuDipatcher vtkPopupMenu;
    private PluginPopupMenuManager pluginPopupMenu;

    public CassandraTree(PipeLineManager pipeLineManager, PluginManager pluginManager) {
        treeModel = new CassandraTreeModel(pipeLineManager, pluginManager);
        vtkPopupMenu = new VtkObjectPopupMenuDipatcher(pipeLineManager, pluginManager);
        pluginPopupMenu = new PluginPopupMenuManager();
        addMouseListener(new PopupListener());
        setModel(treeModel);
    }

    class PopupListener extends MouseAdapter {
        public void mousePressed(MouseEvent e) {
            maybeShowPopup(e);
        }

        public void mouseReleased(MouseEvent e) {
            maybeShowPopup(e);
        }

        private void maybeShowPopup(MouseEvent e) {
            if (e.isPopupTrigger()) {
                if (getPathForLocation(e.getX(), e.getY()) == null) {
                    return;
                }

                Object node = ((DefaultMutableTreeNode) getPathForLocation(e.getX(), e.getY()).getLastPathComponent()).getUserObject();
                if (node instanceof VtkObject) {
                    vtkPopupMenu.showPopupMenu(e.getComponent(), e.getX(), e.getY(), (VtkObject) node);
                }

                if (node instanceof CassandraPlugin) {
                    pluginPopupMenu.showPopupMenu(e.getComponent(), e.getX(), e.getY(), (CassandraPlugin) node);
                }
            }
        }
    }
}
