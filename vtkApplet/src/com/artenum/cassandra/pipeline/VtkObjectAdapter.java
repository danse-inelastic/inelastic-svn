/**
 * Copyright (c) Artenum SARL 2004-2005
 * @author Sebastien Jourdain
 *
 * All rights reserved. This software can
 * not be used or copy or diffused without
 * an explicit license of Artenum SARL, Paris-France
 */
package com.artenum.cassandra.pipeline;

import com.artenum.graph.impl.DefaultCell;
import com.artenum.graph.listener.DragListener;

import java.util.Hashtable;

import javax.swing.JLabel;

/**
 * @author seb
 */
public class VtkObjectAdapter extends DefaultCell implements VtkObject {
    private Object vtkObject;
    private int type = -1;
    private Integer id;
    private Integer localId;
    private String name;
    private Hashtable metadata;
    private boolean valide;

    public VtkObjectAdapter(Object vtkObject, int type, String name, Integer id) {
        super(vtkObject, new JLabel(name));
        new DragListener(this, getUI(), getUI());
        this.vtkObject = vtkObject;
        this.type = type;
        this.name = name;
        this.id = id;
        this.metadata = new Hashtable();
        valide = true;
    }

    public Integer getId() {
        return id;
    }

    public int getType() {
        return type;
    }

    public Object getVtkObject() {
        return vtkObject;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public void setType(int i) {
        type = i;
    }

    public void setVtkObject(Object object) {
        vtkObject = object;
    }

    public String toString() {
        return getName();
    }

    public Hashtable getMetaData() {
        return metadata;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public boolean isValide() {
        return valide;
    }

    public void setValide(boolean valide) {
        this.valide = valide;
    }

    public Integer getLocalTypeId() {
        return localId;
    }

    public void setLocalTypeId(int localId) {
        this.localId = new Integer(localId);
    }
}
