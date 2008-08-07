/**
 * Copyright (c) Artenum SARL 2004-2005
 * @author Sebastien Jourdain
 *
 * All rights reserved. This software can
 * not be used or copy or diffused without
 * an explicit license of Artenum SARL, Paris-France
 */
package com.artenum.cassandra.pipeline;

import vtk.vtkActor;
import vtk.vtkActor2D;
import vtk.vtkMapper;
import vtk.vtkScalarBarActor;

import java.util.Iterator;

import javax.swing.JOptionPane;

/**
 * @author Sebastien
 */
public class CascadeRemoveManager {
    private PipeLineManager pipelineManager;

    public CascadeRemoveManager(PipeLineManager pipeLineManager) {
        this.pipelineManager = pipeLineManager;
    }

    public void removeScalarBar(VtkObject objToRemove) {
        if (JOptionPane.OK_OPTION == JOptionPane.showConfirmDialog(null, "Are you sure you want to delete the scalar bar ?")) {
            removeActorWithOutQuestion(objToRemove);
        }
    }

    public void removeActor(VtkObject objToRemove) {
        if (JOptionPane.OK_OPTION == JOptionPane.showConfirmDialog(null, "Are you sure you want to delete the 3D actor ?")) {
            removeActorWithOutQuestion(objToRemove);
        }
    }

    public void removeLookupTable(VtkObject objToRemove) {
        if (JOptionPane.OK_OPTION == JOptionPane.showConfirmDialog(null, "Are you sure you want to delete the lookup table ?")) {
            removeLookupTableWithOutQuestion(objToRemove);
        }
    }

    public void removeFilter(VtkObject objToRemove) {
        if (JOptionPane.OK_OPTION == JOptionPane.showConfirmDialog(null, "Are you sure you want to delete the Filter ?")) {
            removeFilterWithOutQuestion(objToRemove);
        }
    }

    public void removeMapper(VtkObject objToRemove) {
        if (JOptionPane.OK_OPTION == JOptionPane.showConfirmDialog(null, "Are you sure you want to delete the Mapper ?")) {
            removeMapperWithOutQuestion(objToRemove);
        }
    }

    public void removeDataSet(VtkObject objToRemove) {
        if (JOptionPane.OK_OPTION == JOptionPane.showConfirmDialog(null, "Are you sure you want to delete the Dataset ?")) {
            removeDataSetWithOutQuestion(objToRemove);
        }
    }

    // -------------------
    private void removeScalarBarWithOutQuestion(VtkObject objToRemove) {
        removeActorWithOutQuestion(objToRemove);
    }

    private void removeActorWithOutQuestion(VtkObject objToRemove) {
        pipelineManager.removeVtkObject(objToRemove);
    }

    private void removeLookupTableWithOutQuestion(VtkObject objToRemove) {
        Object[] objList = pipelineManager.getScalarBarList().getData().toArray();
        VtkObject vtkObject = null;
        for (int i = 0; i < objList.length; i++) {
            vtkObject = (VtkObject) objList[i];
            if (((vtkScalarBarActor) vtkObject.getVtkObject()).GetLookupTable().equals(objToRemove.getVtkObject())) {
                removeActorWithOutQuestion(vtkObject);
            }
        }

        //
        pipelineManager.removeVtkObject(objToRemove);
    }

    private void removeFilterWithOutQuestion(VtkObject objToRemove) {
        Filter filter = (Filter) objToRemove.getVtkObject();
        VtkObject vtkObject = null;

        // remove Output actors
        for (Iterator i = filter.getOutputActor().iterator(); i.hasNext();) {
            removeActorWithOutQuestion(pipelineManager.getActorList().getVtkObject(i.next()));
        }

        // remove Output datasets
        for (Iterator i = filter.getOutputDataSet().iterator(); i.hasNext();) {
            removeDataSetWithOutQuestion(pipelineManager.getDataSetList().getVtkObject(i.next()));
        }

        // remove Output mappers
        for (Iterator i = filter.getOutputMapper().iterator(); i.hasNext();) {
            removeMapperWithOutQuestion(pipelineManager.getMapperList().getVtkObject(i.next()));
        }

        // remove filter
        filter.remove();
        //
        pipelineManager.removeVtkObject(objToRemove);
    }

    private void removeMapperWithOutQuestion(VtkObject objToRemove) {
        // find filter
        Object[] objList = pipelineManager.getFilterList().getData().toArray();
        VtkObject vtkObject = null;
        for (int i = 0; i < objList.length; i++) {
            vtkObject = (VtkObject) objList[i];
            if (((Filter) vtkObject.getVtkObject()).getInputMapper().remove(objToRemove.getVtkObject())) {
                removeFilter(vtkObject);
            }
        }

        // Find actor
        objList = pipelineManager.getActorList().getData().toArray();
        for (int i = 0; i < objList.length; i++) {
            vtkObject = (VtkObject) objList[i];
            if (vtkObject.getVtkObject() instanceof vtkActor) {
                if ((((vtkActor) vtkObject.getVtkObject()).GetMapper() != null) &&
                        ((vtkActor) vtkObject.getVtkObject()).GetMapper().equals(objToRemove.getVtkObject())) {
                    removeActorWithOutQuestion(vtkObject);
                }
            } else if (vtkObject.getVtkObject() instanceof vtkActor2D) {
                if ((((vtkActor2D) vtkObject.getVtkObject()).GetMapper() != null) &&
                        ((vtkActor2D) vtkObject.getVtkObject()).GetMapper().equals(objToRemove.getVtkObject())) {
                    removeActorWithOutQuestion(vtkObject);
                }
            }
        }

        //
        pipelineManager.removeVtkObject(objToRemove);
    }

    private void removeDataSetWithOutQuestion(VtkObject objToRemove) {
        // find filter
        Object[] objList = pipelineManager.getFilterList().getData().toArray();
        VtkObject vtkObject = null;
        for (int i = 0; i < objList.length; i++) {
            vtkObject = (VtkObject) objList[i];
            if (((Filter) vtkObject.getVtkObject()).getInputDataSet().remove(objToRemove.getVtkObject())) {
                removeFilterWithOutQuestion(vtkObject);
            }
        }

        // find mapper
        objList = pipelineManager.getMapperList().getData().toArray();
        for (int i = 0; i < objList.length; i++) {
            vtkObject = (VtkObject) objList[i];
            if ((((vtkMapper) vtkObject.getVtkObject()).GetInputAsDataSet() != null) &&
                    ((vtkMapper) vtkObject.getVtkObject()).GetInputAsDataSet().equals(objToRemove.getVtkObject())) {
                removeMapperWithOutQuestion(vtkObject);
            }
        }

        //
        pipelineManager.removeVtkObject(objToRemove);
    }
}
