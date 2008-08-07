/**
 * Copyright (c) Artenum SARL 2004-2005
 * @author Sebastien Jourdain
 *
 * All rights reserved. This software can
 * not be used or copy or diffused without
 * an explicit license of Artenum SARL, Paris-France
 */
package com.artenum.cassandra.pipeline;

import com.artenum.cassandra.vtk.CassandraView;
import com.artenum.cassandra.vtk.DefaultAxes;

import vtk.vtkActor;
import vtk.vtkDataSetMapper;
import vtk.vtkDataSetReader;
import vtk.vtkLookupTable;
import vtk.vtkProp;
import vtk.vtkScalarBarActor;
import vtk.vtkTextActor;

import java.io.File;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.Observable;

/**
 * @author seb
 */
public class SimplePipeLineManager extends Observable implements PipeLineManager {
    private CassandraView view;
    private ArrayList connectivityListener;
    private Hashtable vtkObjectHashtable;
    private VtkObjectListModel actorList;
    private VtkObjectListModel mapperList;
    private VtkObjectListModel datasetList;
    private VtkObjectListModel filterList;
    private VtkObjectListModel lookupTableList;
    private VtkObjectListModel scalarBarList;
    private VtkObjectListModel txtActorList;
    private Integer vtkObjectIndex = new Integer(0);
    private int pluginNumber = 1;
    private int actorNumber = 1;
    private int sourceNumber = 1;
    private int mapperNumber = 1;
    private int filterNumber = 1;
    private int lookupNumber = 1;
    private int scalarBarNumber = 1;
    private int txtActorNumber = 1;

    //
    private DefaultAxes axes;

    public SimplePipeLineManager() {
        view = new CassandraView();
        vtkObjectHashtable = new Hashtable();
        actorList = new VtkObjectListModel(VtkObject.ACTOR);
        mapperList = new VtkObjectListModel(VtkObject.MAPPER);
        datasetList = new VtkObjectListModel(VtkObject.DATASET);
        filterList = new VtkObjectListModel(VtkObject.FILTER);
        lookupTableList = new VtkObjectListModel(VtkObject.LOOKUP_TABLE);
        scalarBarList = new VtkObjectListModel(VtkObject.SCALAR_BAR);
        txtActorList = new VtkObjectListModel(VtkObject.TXT_ACTOR);
        axes = new DefaultAxes(this);
        connectivityListener = new ArrayList();
    }

    // Pipeline management
    synchronized public void addVtkFile(File vtkFile) {
        if (!vtkFile.exists()) {
            System.err.println("File does not exist: " + vtkFile.getAbsolutePath());
            return;
        }

        vtkDataSetReader dataset = new vtkDataSetReader();
        dataset.SetFileName(vtkFile.getAbsolutePath());
        dataset.Update();

        // Set pipeline
        vtkDataSetMapper mapper = new vtkDataSetMapper();
        mapper.SetInput(dataset.GetOutput());
        mapper.Update();
        vtkActor actor = new vtkActor();
        actor.SetMapper(mapper);

        //vtkScalarBarWidget scalBarWidget = new vtkScalarBarWidget();
        //scalBarWidget.SetScalarBarActor(scalBar);
        //vtkRenderWindowInteractor iren = new vtkRenderWindowInteractor();
        //scalBarWidget.SetInteractor(getCassandraView().GetRenderWindow().GetInteractor());
        //scalBarWidget.SetInteractor(iren);
        //iren.SetRenderWindow(getCassandraView().GetRenderWindow());
        //scalBarWidget.SetInteractor(iren);
        //iren.Initialize();
        //iren.Start();
        //
        // Register vtkObject in pipeline
        addDataSet(dataset.GetOutput(), vtkFile.getName());
        addMapper(mapper, vtkFile.getName());

        // Show actors
        setActorVisible(addActor(actor, vtkFile.getName()), true);

        // lookup table
        if (dataset.GetOutput().GetScalarRange() != null) {
            vtkLookupTable lookupTable = new vtkLookupTable();
            lookupTable.SetHueRange(0.66667, 0);
            lookupTable.SetTableRange(dataset.GetOutput().GetScalarRange());
            lookupTable.Build();
            mapper.SetLookupTable(lookupTable);
            mapper.SetScalarRange(dataset.GetOutput().GetScalarRange());

            // Scalar bar
            vtkScalarBarActor scalBar = new vtkScalarBarActor();
            scalBar.SetLookupTable(lookupTable);

            // register 
            addLookupTable(lookupTable, vtkFile.getName());
            setActorVisible(addScalarBar(scalBar, vtkFile.getName()), true);
        }
    }

    // Connection mamagement
    public void setActorVisible(Integer vtkObjectId, boolean viewActor) {
        setActorVisible((VtkObject) vtkObjectHashtable.get(vtkObjectId), viewActor);
    }

    public void setActorVisible(VtkObject vtkObject, boolean viewActor) {
        if ((vtkObject.getType() == VtkObject.ACTOR) || (vtkObject.getType() == VtkObject.TXT_ACTOR) || (vtkObject.getType() == VtkObject.SCALAR_BAR)) {
            if (!vtkObject.isValide()) {
                return;
            }

            vtkObject.getMetaData().put(VtkObject.ACTOR_VISIBLE, Boolean.toString(viewActor));
            if (vtkObject.getVtkObject() instanceof vtkActor) {
                // 3D
                if (viewActor) {
                    view.GetRenderer().AddActor((vtkProp) vtkObject.getVtkObject());
                } else {
                    view.GetRenderer().RemoveActor((vtkProp) vtkObject.getVtkObject());
                }
            } else {
                // 2D
                if (viewActor) {
                    view.GetRenderer().AddActor2D((vtkProp) vtkObject.getVtkObject());
                } else {
                    view.GetRenderer().RemoveActor2D((vtkProp) vtkObject.getVtkObject());
                }
            }
        }

        this.setChanged();
        this.notifyObservers(vtkObjectHashtable);
    }

    // Model management
    public VtkObject getVtkObject(Integer vtkObjectId) {
        return (VtkObject) vtkObjectHashtable.get(vtkObjectId);
    }

    public Integer getNextVtkObjectId() {
        vtkObjectIndex = new Integer(vtkObjectIndex.intValue() + 1);
        return vtkObjectIndex;
    }

    public VtkObjectListModel getActorList() {
        return actorList;
    }

    public VtkObjectListModel getDataSetList() {
        return datasetList;
    }

    public VtkObjectListModel getFilterList() {
        return filterList;
    }

    public VtkObjectListModel getMapperList() {
        return mapperList;
    }

    public VtkObjectListModel getLookupTableList() {
        return lookupTableList;
    }

    public VtkObjectListModel getScalarBarList() {
        return scalarBarList;
    }

    public VtkObjectListModel getTextActorList() {
        return txtActorList;
    }

    synchronized public VtkObject addActor(Object actor, String name) {
        int id = actorNumber++;
        String actorId = name + " (" + id + ")";
        VtkObjectAdapter vtkObject = new VtkObjectAdapter(actor, VtkObject.ACTOR, actorId, getNextVtkObjectId());
        vtkObject.setLocalTypeId(id);
        vtkObjectHashtable.put(vtkObject.getId(), vtkObject);
        actorList.addVtkObject(vtkObject);
        this.setChanged();
        this.notifyObservers(vtkObjectHashtable);
        return vtkObject;
    }

    synchronized public VtkObject addMapper(Object mapper, String name) {
        int id = mapperNumber++;
        String mapperId = name + " (" + id + ")";
        VtkObjectAdapter vtkObject = new VtkObjectAdapter(mapper, VtkObject.MAPPER, mapperId, getNextVtkObjectId());
        vtkObject.setLocalTypeId(id);
        vtkObjectHashtable.put(vtkObject.getId(), vtkObject);
        mapperList.addVtkObject(vtkObject);
        this.setChanged();
        this.notifyObservers(vtkObjectHashtable);
        return vtkObject;
    }

    synchronized public VtkObject addDataSet(Object dataset, String name) {
        int id = sourceNumber++;
        String datasetId = name + " (" + id + ")";
        VtkObjectAdapter vtkObject = new VtkObjectAdapter(dataset, VtkObject.DATASET, datasetId, getNextVtkObjectId());
        vtkObject.setLocalTypeId(id);
        vtkObjectHashtable.put(vtkObject.getId(), vtkObject);
        datasetList.addVtkObject(vtkObject);
        this.setChanged();
        this.notifyObservers(vtkObjectHashtable);
        return vtkObject;
    }

    synchronized public VtkObject addFilter(Filter filter, String name) {
        int id = filterNumber++;
        String filterId = name + " (" + id + ")";
        VtkObjectAdapter vtkObject = new VtkObjectAdapter(filter, VtkObject.FILTER, filterId, getNextVtkObjectId());
        vtkObject.setLocalTypeId(id);
        vtkObjectHashtable.put(vtkObject.getId(), vtkObject);
        filterList.addVtkObject(vtkObject);
        this.setChanged();
        this.notifyObservers(vtkObjectHashtable);
        return vtkObject;
    }

    synchronized public VtkObject addLookupTable(vtkLookupTable lookupTable, String name) {
        int id = lookupNumber++;
        String lookupTableId = name + " (" + id + ")";
        VtkObjectAdapter vtkObject = new VtkObjectAdapter(lookupTable, VtkObject.LOOKUP_TABLE, lookupTableId, getNextVtkObjectId());
        vtkObject.setLocalTypeId(id);
        vtkObjectHashtable.put(vtkObject.getId(), vtkObject);
        lookupTableList.addVtkObject(vtkObject);
        this.setChanged();
        this.notifyObservers(vtkObjectHashtable);
        return vtkObject;
    }

    synchronized public VtkObject addScalarBar(vtkScalarBarActor scalarBar, String name) {
        int id = scalarBarNumber++;
        String scalarBarId = name + " (" + id + ")";
        VtkObjectAdapter vtkObject = new VtkObjectAdapter(scalarBar, VtkObject.SCALAR_BAR, scalarBarId, getNextVtkObjectId());
        vtkObject.setLocalTypeId(id);
        vtkObjectHashtable.put(vtkObject.getId(), vtkObject);
        scalarBarList.addVtkObject(vtkObject);
        this.setChanged();
        this.notifyObservers(vtkObjectHashtable);
        return vtkObject;
    }

    synchronized public VtkObject addTxtActor(vtkTextActor txtActor, String name) {
        int id = txtActorNumber++;
        String txtActorId = name + " (" + id + ")";
        VtkObjectAdapter vtkObject = new VtkObjectAdapter(txtActor, VtkObject.TXT_ACTOR, txtActorId, getNextVtkObjectId());
        vtkObject.setLocalTypeId(id);
        vtkObjectHashtable.put(vtkObject.getId(), vtkObject);
        txtActorList.addVtkObject(vtkObject);
        this.setChanged();
        this.notifyObservers(vtkObjectHashtable);
        return vtkObject;
    }

    synchronized public void removeVtkObject(Integer vtkObjectId) {
        VtkObject vtkObject = (VtkObject) vtkObjectHashtable.remove(vtkObjectId);
        if (vtkObject != null) {
            switch (vtkObject.getType()) {
            case VtkObject.ACTOR:
                setActorVisible(vtkObject, false);
                actorList.removeVtkObject(vtkObject);
                break;
            case VtkObject.MAPPER:
                mapperList.removeVtkObject(vtkObject);
                break;
            case VtkObject.DATASET:
                datasetList.removeVtkObject(vtkObject);
                break;
            case VtkObject.FILTER:
                filterList.removeVtkObject(vtkObject);
                break;
            case VtkObject.LOOKUP_TABLE:
                lookupTableList.removeVtkObject(vtkObject);
                break;
            case VtkObject.SCALAR_BAR:
                setActorVisible(vtkObject, false);
                scalarBarList.removeVtkObject(vtkObject);
                break;
            case VtkObject.TXT_ACTOR:
                setActorVisible(vtkObject, false);
                txtActorList.removeVtkObject(vtkObject);
                break;
            }

            this.setChanged();
            this.notifyObservers(vtkObjectHashtable);
        }
    }

    synchronized public void removeVtkObject(VtkObject vtkObject) {
        removeVtkObject(vtkObject.getId());
    }

    // View management
    public CassandraView getCassandraView() {
        return view;
    }

    public void setAxisVisible(boolean viewAxis) {
        axes.setVisible(viewAxis);
    }

    public void validateViewAndGo() {
        getCassandraView().validateViewAndGo();
    }

    public void validateViewAndWait() {
        getCassandraView().validateViewAndWait();
    }

    public void deepValidateView() {
        getCassandraView().deepValidateView();
    }

    synchronized public void addConnectivityListener(ConnectivityListener l) {
        connectivityListener.add(l);
    }

    public void notifyConnectivityChange(VtkObject obj) {
        for (Iterator i = connectivityListener.iterator(); i.hasNext();) {
            ((ConnectivityListener) i.next()).connectivityChange(obj);
        }
    }

    synchronized public void removeConnectivityListener(ConnectivityListener l) {
        connectivityListener.remove(l);
    }
}
