/**
 * Copyright (c) Artenum SARL 2004-2005
 * @author Sebastien Jourdain
 *
 * All rights reserved. This software can
 * not be used or copy or diffused without
 * an explicit license of Artenum SARL, Paris-France
 */
package com.artenum.cassandra.pipeline.graph;

import com.artenum.cassandra.pipeline.VtkObject;

import com.artenum.graph.impl.DefaultConnection;
import com.artenum.graph.interfaces.Cell;
import com.artenum.graph.interfaces.Connection;
import com.artenum.graph.listener.DragListener;

import java.awt.Color;
import java.awt.Component;
import java.awt.Point;
import java.awt.Rectangle;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;

import java.util.ArrayList;
import java.util.List;

import javax.swing.BorderFactory;
import javax.swing.JComponent;

/**
 * @author Sebastien
 */
public class VtkObjectCellAdapter implements Cell {
    private VtkObject object;
    private boolean selected;
    private VtkObjectUI2 ui;
    protected Object oldGroupDragListener;
    protected ArrayList connectionList;
    protected Object userObject;
    protected Color selectedBorderColor = Color.BLACK;
    protected int selectedBorderSize = 2;

    public VtkObjectCellAdapter(VtkObject object) {
        this.object = object;
        ui = new VtkObjectUI2(object);
        new DragListener(this, ui, ui);
        connectionList = new ArrayList();
    }

    public Component getUI() {
        return ui;
    }

    public List getConnections() {
        return connectionList;
    }

    public Point getConnectionPoint(Connection connection) {
        Rectangle remoteBounds = connection.getOtherCell(this).getUI().getBounds();
        Rectangle localBounds = ui.getBounds();
        double rx = remoteBounds.getCenterX();
        double ry = remoteBounds.getCenterY();
        double lx = localBounds.getCenterX();
        double ly = localBounds.getCenterY();
        Point result = new Point((int) lx, (int) ly);

        //
        if ((localBounds.getMaxX() < rx) || (rx < localBounds.getMinX())) {
            result.x = (localBounds.getMinX() > rx) ? (int) localBounds.getMinX() : (int) localBounds.getMaxX();
        } else if ((localBounds.getMaxY() < ry) || (ry < localBounds.getMinY())) {
            result.y = (localBounds.getMinY() > ry) ? (int) localBounds.getMinY() : (int) localBounds.getMaxY();
        }

        //
        return result;
    }

    public void setSelected(boolean selected) {
        this.selected = selected;
        if ((ui != null) && ui instanceof JComponent) {
            if (selected) {
                ((JComponent) ui).setBorder(BorderFactory.createLineBorder(selectedBorderColor, selectedBorderSize));
            } else {
                ((JComponent) ui).setBorder(BorderFactory.createEmptyBorder());
            }
        }
    }

    public boolean isSelected() {
        return selected;
    }

    public void connectTo(Cell destCell) {
        DefaultConnection connnection = new DefaultConnection(this, destCell);
        this.addConnection(connnection);
        destCell.addConnection(connnection);
    }

    public void addConnection(Connection connection) {
        connectionList.add(connection);
    }

    public void addGroupDragListener(Object mouseListener) {
        if (oldGroupDragListener != null) {
            ui.removeMouseListener((MouseListener) oldGroupDragListener);
            ui.removeMouseMotionListener((MouseMotionListener) oldGroupDragListener);
        }

        ui.addMouseListener((MouseListener) mouseListener);
        ui.addMouseMotionListener((MouseMotionListener) mouseListener);
        oldGroupDragListener = mouseListener;
    }

    public void setSelectedBorderColor(Color selectedBorderColor) {
        this.selectedBorderColor = selectedBorderColor;
    }

    public void setSelectedBorderSize(int selectedBorderSize) {
        this.selectedBorderSize = selectedBorderSize;
    }

    public VtkObject getVtkObject() {
        return object;
    }

    public void savePosition() {
        ui.savePosition();
    }

    public Point getPosition() {
        return ui.getPosition();
    }
}
