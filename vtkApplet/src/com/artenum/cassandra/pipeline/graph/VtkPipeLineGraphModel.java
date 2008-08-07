/**
 * Copyright (c) Artenum SARL 2004-2005
 * @author Sebastien Jourdain
 *
 * All rights reserved. This software can
 * not be used or copy or diffused without
 * an explicit license of Artenum SARL, Paris-France
 */
package com.artenum.cassandra.pipeline.graph;

import com.artenum.cassandra.pipeline.ConnectivityListener;
import com.artenum.cassandra.pipeline.Filter;
import com.artenum.cassandra.pipeline.PipeLineManager;
import com.artenum.cassandra.pipeline.VtkObject;
import com.artenum.cassandra.plugin.PluginManager;

import com.artenum.graph.impl.DefaultGraphModel;
import com.artenum.graph.interfaces.Cell;
import com.artenum.graph.interfaces.GraphViewListener;

import vtk.vtkActor;
import vtk.vtkMapper;
import vtk.vtkScalarBarActor;

import java.util.Iterator;

import javax.swing.event.ListDataEvent;
import javax.swing.event.ListDataListener;

/**
 * @author Sebastien
 */
public class VtkPipeLineGraphModel extends DefaultGraphModel implements ListDataListener, ConnectivityListener {
    private PipeLineManager pipeLineManager;
    private PluginManager pluginManager;
    private int lastYPos = 0;

    public VtkPipeLineGraphModel(PipeLineManager pipeLineManager, PluginManager pluginManager) {
        this.pipeLineManager = pipeLineManager;
        this.pluginManager = pluginManager;
        pipeLineManager.getActorList().addListDataListener(this);
        pipeLineManager.getMapperList().addListDataListener(this);
        pipeLineManager.getDataSetList().addListDataListener(this);
        pipeLineManager.getFilterList().addListDataListener(this);
        pipeLineManager.getLookupTableList().addListDataListener(this);
        pipeLineManager.getScalarBarList().addListDataListener(this);
        pipeLineManager.getTextActorList().addListDataListener(this);
        pipeLineManager.addConnectivityListener(this);
    }

    public void contentsChanged(ListDataEvent e) {
        updateCell();
        updateConnection();
        reload();
    }

    public void reload() {
        // save pos
        Object[] cell = getCellList().toArray();
        for (int i = 0; i < cell.length; i++)
            ((VtkObjectCellAdapter) cell[i]).savePosition();

        super.reload();
    }

    public void updateCell() {
        VtkObject tmp = null;
        VtkObjectCellAdapter tmpCell = null;
        for (Iterator i = pipeLineManager.getActorList().getData().iterator(); i.hasNext();) {
            tmp = (VtkObject) i.next();
            if (tmp.getMetaData().get(VtkObject.CELL) == null) {
                tmpCell = new VtkObjectCellAdapter(tmp);
                tmp.getMetaData().put(VtkObject.CELL, tmpCell);
            } else {
                tmpCell = (VtkObjectCellAdapter) tmp.getMetaData().get(VtkObject.CELL);
            }

            if (!getCellList().contains(tmpCell)) {
                insertCell((Cell) tmpCell);
            }
        }

        for (Iterator i = pipeLineManager.getMapperList().getData().iterator(); i.hasNext();) {
            tmp = (VtkObject) i.next();
            if (tmp.getMetaData().get(VtkObject.CELL) == null) {
                tmpCell = new VtkObjectCellAdapter(tmp);
                tmp.getMetaData().put(VtkObject.CELL, tmpCell);
            } else {
                tmpCell = (VtkObjectCellAdapter) tmp.getMetaData().get(VtkObject.CELL);
            }

            if (!getCellList().contains(tmpCell)) {
                insertCell((Cell) tmpCell);
            }
        }

        for (Iterator i = pipeLineManager.getDataSetList().getData().iterator(); i.hasNext();) {
            tmp = (VtkObject) i.next();
            if (tmp.getMetaData().get(VtkObject.CELL) == null) {
                tmpCell = new VtkObjectCellAdapter(tmp);
                tmp.getMetaData().put(VtkObject.CELL, tmpCell);
                VtkObjectUI cellUI = (VtkObjectUI) tmpCell.getUI();
                if (cellUI.getPosition().y > lastYPos) {
                    lastYPos = cellUI.getPosition().y;
                }
            } else {
                tmpCell = (VtkObjectCellAdapter) tmp.getMetaData().get(VtkObject.CELL);
            }

            if (!getCellList().contains(tmpCell)) {
                insertCell((Cell) tmpCell);
            }
        }

        for (Iterator i = pipeLineManager.getFilterList().getData().iterator(); i.hasNext();) {
            tmp = (VtkObject) i.next();
            if (tmp.getMetaData().get(VtkObject.CELL) == null) {
                tmpCell = new VtkObjectCellAdapter(tmp);
                tmp.getMetaData().put(VtkObject.CELL, tmpCell);
                VtkObjectUI cellUI = (VtkObjectUI) tmpCell.getUI();
                if (cellUI.getPosition().y < lastYPos) {
                    cellUI.getPosition().y = lastYPos;
                }
            } else {
                tmpCell = (VtkObjectCellAdapter) tmp.getMetaData().get(VtkObject.CELL);
            }

            if (!getCellList().contains(tmpCell)) {
                insertCell((Cell) tmpCell);
            }
        }

        for (Iterator i = pipeLineManager.getLookupTableList().getData().iterator(); i.hasNext();) {
            tmp = (VtkObject) i.next();
            if (tmp.getMetaData().get(VtkObject.CELL) == null) {
                tmpCell = new VtkObjectCellAdapter(tmp);
                tmp.getMetaData().put(VtkObject.CELL, tmpCell);
            } else {
                tmpCell = (VtkObjectCellAdapter) tmp.getMetaData().get(VtkObject.CELL);
            }

            if (!getCellList().contains(tmpCell)) {
                insertCell((Cell) tmpCell);
            }
        }

        for (Iterator i = pipeLineManager.getScalarBarList().getData().iterator(); i.hasNext();) {
            tmp = (VtkObject) i.next();
            if (tmp.getMetaData().get(VtkObject.CELL) == null) {
                tmpCell = new VtkObjectCellAdapter(tmp);
                tmp.getMetaData().put(VtkObject.CELL, tmpCell);
            } else {
                tmpCell = (VtkObjectCellAdapter) tmp.getMetaData().get(VtkObject.CELL);
            }

            if (!getCellList().contains(tmpCell)) {
                insertCell((Cell) tmpCell);
            }
        }

        for (Iterator i = pipeLineManager.getTextActorList().getData().iterator(); i.hasNext();) {
            tmp = (VtkObject) i.next();
            if (tmp.getMetaData().get(VtkObject.CELL) == null) {
                tmpCell = new VtkObjectCellAdapter(tmp);
                tmp.getMetaData().put(VtkObject.CELL, tmpCell);
            } else {
                tmpCell = (VtkObjectCellAdapter) tmp.getMetaData().get(VtkObject.CELL);
            }

            if (!getCellList().contains(tmpCell)) {
                insertCell((Cell) tmpCell);
            }
        }
    }

    public void updateConnection() {
        getConnections().clear();
        Object[] cellList = getCellList().toArray();
        for (int i = 0; i < cellList.length; i++) {
            ((Cell) cellList[i]).getConnections().clear();
        }

        // Actor
        for (Iterator i = pipeLineManager.getActorList().getData().iterator(); i.hasNext();) {
            VtkObject actor = ((VtkObject) i.next());
            if (actor.getVtkObject() instanceof vtkActor) {
                vtkMapper actorMapper = ((vtkActor) actor.getVtkObject()).GetMapper();
                for (Iterator iMap = pipeLineManager.getMapperList().getData().iterator(); iMap.hasNext();) {
                    VtkObject mapper = ((VtkObject) iMap.next());
                    if (mapper.getVtkObject().equals(actorMapper)) {
                        connect((Cell) actor.getMetaData().get(VtkObject.CELL), (Cell) mapper.getMetaData().get(VtkObject.CELL));
                    }
                }
            }
        }

        // Dataset
        for (Iterator i = pipeLineManager.getDataSetList().getData().iterator(); i.hasNext();) {
            VtkObject dataset = ((VtkObject) i.next());
            for (Iterator iMap = pipeLineManager.getMapperList().getData().iterator(); iMap.hasNext();) {
                VtkObject mapper = ((VtkObject) iMap.next());
                if (((vtkMapper) mapper.getVtkObject()).GetInputAsDataSet() == null) {
                    continue;
                }

                if (((vtkMapper) mapper.getVtkObject()).GetInputAsDataSet().equals(dataset.getVtkObject())) {
                    connect((Cell) dataset.getMetaData().get(VtkObject.CELL), (Cell) mapper.getMetaData().get(VtkObject.CELL));
                }
            }
        }

        // LookupTable
        for (Iterator i = pipeLineManager.getLookupTableList().getData().iterator(); i.hasNext();) {
            VtkObject lookupTable = ((VtkObject) i.next());

            // Mapper link ?
            for (Iterator iMap = pipeLineManager.getMapperList().getData().iterator(); iMap.hasNext();) {
                VtkObject mapper = ((VtkObject) iMap.next());
                if (((vtkMapper) mapper.getVtkObject()).GetLookupTable() == null) {
                    continue;
                }

                if (((vtkMapper) mapper.getVtkObject()).GetLookupTable().equals(lookupTable.getVtkObject())) {
                    connect((Cell) lookupTable.getMetaData().get(VtkObject.CELL), (Cell) mapper.getMetaData().get(VtkObject.CELL));
                }
            }

            for (Iterator iScalar = pipeLineManager.getScalarBarList().getData().iterator(); iScalar.hasNext();) {
                VtkObject scalarBar = ((VtkObject) iScalar.next());
                if (((vtkScalarBarActor) scalarBar.getVtkObject()).GetLookupTable() == null) {
                    continue;
                }

                if (((vtkScalarBarActor) scalarBar.getVtkObject()).GetLookupTable().equals(lookupTable.getVtkObject())) {
                    connect((Cell) lookupTable.getMetaData().get(VtkObject.CELL), (Cell) scalarBar.getMetaData().get(VtkObject.CELL));
                }
            }
        }

        // Filter
        for (Iterator i = pipeLineManager.getFilterList().getData().iterator(); i.hasNext();) {
            VtkObject filter = ((VtkObject) i.next());
            Object vtkConnection;
            for (Iterator iMap = pipeLineManager.getMapperList().getData().iterator(); iMap.hasNext();) {
                VtkObject mapper = ((VtkObject) iMap.next());
                for (Iterator fMapperInIterator = ((Filter) filter.getVtkObject()).getInputMapper().iterator(); fMapperInIterator.hasNext();) {
                    vtkConnection = fMapperInIterator.next();
                    if (vtkConnection.equals(mapper.getVtkObject())) {
                        connect((Cell) filter.getMetaData().get(VtkObject.CELL), (Cell) mapper.getMetaData().get(VtkObject.CELL));
                    }
                }

                for (Iterator fMapperOutIterator = ((Filter) filter.getVtkObject()).getOutputMapper().iterator(); fMapperOutIterator.hasNext();) {
                    vtkConnection = fMapperOutIterator.next();
                    if (vtkConnection.equals(mapper.getVtkObject())) {
                        connect((Cell) filter.getMetaData().get(VtkObject.CELL), (Cell) mapper.getMetaData().get(VtkObject.CELL));
                    }
                }
            }

            for (Iterator iActor = pipeLineManager.getActorList().getData().iterator(); iActor.hasNext();) {
                VtkObject actor = ((VtkObject) iActor.next());
                for (Iterator fMapperInIterator = ((Filter) filter.getVtkObject()).getInputActor().iterator(); fMapperInIterator.hasNext();) {
                    vtkConnection = fMapperInIterator.next();
                    if (vtkConnection.equals(actor.getVtkObject())) {
                        connect((Cell) filter.getMetaData().get(VtkObject.CELL), (Cell) actor.getMetaData().get(VtkObject.CELL));
                    }
                }

                for (Iterator fMapperOutIterator = ((Filter) filter.getVtkObject()).getOutputActor().iterator(); fMapperOutIterator.hasNext();) {
                    vtkConnection = fMapperOutIterator.next();
                    if (vtkConnection.equals(actor.getVtkObject())) {
                        connect((Cell) filter.getMetaData().get(VtkObject.CELL), (Cell) actor.getMetaData().get(VtkObject.CELL));
                    }
                }
            }

            for (Iterator iDataSet = pipeLineManager.getDataSetList().getData().iterator(); iDataSet.hasNext();) {
                VtkObject dataset = ((VtkObject) iDataSet.next());
                for (Iterator fMapperInIterator = ((Filter) filter.getVtkObject()).getInputDataSet().iterator(); fMapperInIterator.hasNext();) {
                    vtkConnection = fMapperInIterator.next();
                    if (vtkConnection.equals(dataset.getVtkObject())) {
                        connect((Cell) filter.getMetaData().get(VtkObject.CELL), (Cell) dataset.getMetaData().get(VtkObject.CELL));
                    }
                }

                for (Iterator fMapperOutIterator = ((Filter) filter.getVtkObject()).getOutputDataSet().iterator(); fMapperOutIterator.hasNext();) {
                    vtkConnection = fMapperOutIterator.next();
                    if (vtkConnection.equals(dataset.getVtkObject())) {
                        connect((Cell) filter.getMetaData().get(VtkObject.CELL), (Cell) dataset.getMetaData().get(VtkObject.CELL));
                    }
                }
            }
        }
    }

    public void intervalAdded(ListDataEvent e) {
        updateCell();
        updateConnection();
        reload();
    }

    public void intervalRemoved(ListDataEvent e) {
        VtkObjectCellAdapter cellAdapter = null;
        Object[] vtkObjectCellAdapterList = getCellList().toArray();
        for (int index = 0; index < vtkObjectCellAdapterList.length; index++) {
            cellAdapter = (VtkObjectCellAdapter) vtkObjectCellAdapterList[index];
            if (pipeLineManager.getVtkObject(cellAdapter.getVtkObject().getId()) == null) {
                for (Iterator i = viewListenerList.iterator(); i.hasNext();) {
                    ((GraphViewListener) i.next()).removeCell(cellAdapter);
                }

                getCellList().remove(cellAdapter);
            }
        }

        updateCell();
        updateConnection();
        reload();
    }

    public void connectivityChange(VtkObject vtkObject) {
        updateConnection();
        reload();
    }

    public PipeLineManager getPipelineManager() {
        return pipeLineManager;
    }

    public PluginManager getPluginManager() {
        return pluginManager;
    }
}
