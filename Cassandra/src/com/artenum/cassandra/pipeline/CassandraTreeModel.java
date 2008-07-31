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

import com.artenum.cassandra.plugin.PluginManager;

import java.util.Iterator;

import javax.swing.event.ListDataEvent;
import javax.swing.event.ListDataListener;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.MutableTreeNode;

/**
 * <pre>
 * <b>Project ref           :</b> CASSANDRA project
 * <b>Copyright and license :</b> See relevant sections
 * <b>Status                :</b> under development
 * <b>Creation              :</b> 04/03/2005
 * <b>Modification          :</b>
 *
 * <b>Description  :</b> A tree model of the VTK pipeline
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
public class CassandraTreeModel extends DefaultTreeModel implements ListDataListener {
    private PipeLineManager pipelineManager;
    private PluginManager pluginModel;
    private VtkObjectListModel actorModel;
    private VtkObjectListModel mapperModel;
    private VtkObjectListModel datasetModel;
    private VtkObjectListModel lookupTableModel;
    private VtkObjectListModel scalarBarModel;
    private VtkObjectListModel txtActorModel;
    private DefaultMutableTreeNode actorParentNode;
    private DefaultMutableTreeNode mapperParentNode;
    private DefaultMutableTreeNode datasetParentNode;
    private DefaultMutableTreeNode lookupTableParentNode;
    private DefaultMutableTreeNode scalarParentNode;
    private DefaultMutableTreeNode txtActorParentNode;
    private DefaultMutableTreeNode pluginParentNode;
    private DefaultMutableTreeNode root;

    public CassandraTreeModel(PipeLineManager pipelineManager, PluginManager pluginManager) {
        super(new DefaultMutableTreeNode("Vtk components"));
        this.pipelineManager = pipelineManager;
        actorModel = pipelineManager.getActorList();
        mapperModel = pipelineManager.getMapperList();
        datasetModel = pipelineManager.getDataSetList();
        txtActorModel = pipelineManager.getTextActorList();
        scalarBarModel = pipelineManager.getScalarBarList();
        lookupTableModel = pipelineManager.getLookupTableList();
        pluginModel = pluginManager;
        datasetModel.addListDataListener(this);
        mapperModel.addListDataListener(this);
        actorModel.addListDataListener(this);
        lookupTableModel.addListDataListener(this);
        txtActorModel.addListDataListener(this);
        scalarBarModel.addListDataListener(this);
        pluginModel.addListDataListener(this);
        //
        root = (DefaultMutableTreeNode) getRoot();
        actorParentNode = new DefaultMutableTreeNode("Actors");
        mapperParentNode = new DefaultMutableTreeNode("Mappers");
        datasetParentNode = new DefaultMutableTreeNode("Dataset");
        pluginParentNode = new DefaultMutableTreeNode("Plugins");
        scalarParentNode = new DefaultMutableTreeNode("ScalarBar");
        txtActorParentNode = new DefaultMutableTreeNode("Text");
        lookupTableParentNode = new DefaultMutableTreeNode("Lookup Table");
        insertNodeInto(actorParentNode, root, root.getChildCount());
        insertNodeInto(scalarParentNode, root, root.getChildCount());
        insertNodeInto(txtActorParentNode, root, root.getChildCount());
        insertNodeInto(mapperParentNode, root, root.getChildCount());
        insertNodeInto(lookupTableParentNode, root, root.getChildCount());
        insertNodeInto(datasetParentNode, root, root.getChildCount());
        insertNodeInto(pluginParentNode, root, root.getChildCount());
        //
        reload();
    }

    public void reload() {
        actorParentNode.removeAllChildren();
        mapperParentNode.removeAllChildren();
        datasetParentNode.removeAllChildren();
        pluginParentNode.removeAllChildren();
        scalarParentNode.removeAllChildren();
        txtActorParentNode.removeAllChildren();
        lookupTableParentNode.removeAllChildren();

        // build tree
        for (Iterator i = actorModel.getData().iterator(); i.hasNext();) {
            insertNodeInto(new DefaultMutableTreeNode(i.next()), actorParentNode, actorParentNode.getChildCount());
        }

        for (Iterator i = mapperModel.getData().iterator(); i.hasNext();) {
            insertNodeInto(new DefaultMutableTreeNode(i.next()), mapperParentNode, mapperParentNode.getChildCount());
        }

        for (Iterator i = datasetModel.getData().iterator(); i.hasNext();) {
            insertNodeInto(new DefaultMutableTreeNode(i.next()), datasetParentNode, datasetParentNode.getChildCount());
        }

        for (Iterator i = pluginModel.getData().iterator(); i.hasNext();) {
            insertNodeInto(new DefaultMutableTreeNode(i.next()), pluginParentNode, pluginParentNode.getChildCount());
        }

        for (Iterator i = txtActorModel.getData().iterator(); i.hasNext();) {
            insertNodeInto(new DefaultMutableTreeNode(i.next()), txtActorParentNode, txtActorParentNode.getChildCount());
        }

        for (Iterator i = scalarBarModel.getData().iterator(); i.hasNext();) {
            insertNodeInto(new DefaultMutableTreeNode(i.next()), scalarParentNode, scalarParentNode.getChildCount());
        }

        for (Iterator i = lookupTableModel.getData().iterator(); i.hasNext();) {
            insertNodeInto(new DefaultMutableTreeNode(i.next()), lookupTableParentNode, lookupTableParentNode.getChildCount());
        }
    }

    public void contentsChanged(ListDataEvent e) {
        reload();
    }

    public void intervalAdded(ListDataEvent e) {
        if (e.getSource().equals(actorModel)) {
            insertNodeInto(new DefaultMutableTreeNode(actorModel.getLastVtkObject()), actorParentNode, actorParentNode.getChildCount());
        }

        if (e.getSource().equals(mapperModel)) {
            insertNodeInto(new DefaultMutableTreeNode(mapperModel.getLastVtkObject()), mapperParentNode, mapperParentNode.getChildCount());
        }

        if (e.getSource().equals(datasetModel)) {
            insertNodeInto(new DefaultMutableTreeNode(datasetModel.getLastVtkObject()), datasetParentNode, datasetParentNode.getChildCount());
        }

        if (e.getSource().equals(pluginModel)) {
            insertNodeInto(new DefaultMutableTreeNode(pluginModel.getLastPlugin()), pluginParentNode, pluginParentNode.getChildCount());
        }

        if (e.getSource().equals(txtActorModel)) {
            insertNodeInto(new DefaultMutableTreeNode(txtActorModel.getLastVtkObject()), txtActorParentNode, txtActorParentNode.getChildCount());
        }

        if (e.getSource().equals(scalarBarModel)) {
            insertNodeInto(new DefaultMutableTreeNode(scalarBarModel.getLastVtkObject()), scalarParentNode, scalarParentNode.getChildCount());
        }

        if (e.getSource().equals(lookupTableModel)) {
            insertNodeInto(new DefaultMutableTreeNode(lookupTableModel.getLastVtkObject()), lookupTableParentNode, lookupTableParentNode.getChildCount());
        }
    }

    public void intervalRemoved(ListDataEvent e) {
        if (e.getSource().equals(actorModel)) {
            removeNodeFromParent((MutableTreeNode) actorParentNode.getChildAt(e.getIndex0()));
        }

        if (e.getSource().equals(mapperModel)) {
            removeNodeFromParent((MutableTreeNode) mapperParentNode.getChildAt(e.getIndex0()));
        }

        if (e.getSource().equals(datasetModel)) {
            removeNodeFromParent((MutableTreeNode) datasetParentNode.getChildAt(e.getIndex0()));
        }

        if (e.getSource().equals(pluginModel)) {
            removeNodeFromParent((MutableTreeNode) pluginParentNode.getChildAt(e.getIndex0()));
        }

        if (e.getSource().equals(txtActorModel)) {
            removeNodeFromParent((MutableTreeNode) txtActorParentNode.getChildAt(e.getIndex0()));
        }

        if (e.getSource().equals(scalarBarModel)) {
            removeNodeFromParent((MutableTreeNode) scalarParentNode.getChildAt(e.getIndex0()));
        }

        if (e.getSource().equals(lookupTableModel)) {
            removeNodeFromParent((MutableTreeNode) lookupTableParentNode.getChildAt(e.getIndex0()));
        }
    }
}
