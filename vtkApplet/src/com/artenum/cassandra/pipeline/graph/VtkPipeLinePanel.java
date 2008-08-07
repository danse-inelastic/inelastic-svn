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
import com.artenum.cassandra.ui.VtkObjectPopupMenuDipatcher;

import com.artenum.graph.SimpleGraphPanel;
import com.artenum.graph.interfaces.Cell;
import com.artenum.graph.interfaces.Connection;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Component;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Point;
import java.awt.Rectangle;
import java.awt.Stroke;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;

import java.util.Hashtable;
import java.util.Observable;
import java.util.Observer;

/**
 * @author Sebastien
 */
public class VtkPipeLinePanel extends SimpleGraphPanel implements Observer {
    private VtkObjectPopupMenuDipatcher vtkPopupMenu;
    private PopupListener popupListener;
    private Hashtable cellIndex;
    private Stroke lineStroke;

    public VtkPipeLinePanel(VtkPipeLineGraphModel graphModel) {
        super(graphModel);
        ((Observable) graphModel.getPipelineManager()).addObserver(this);
        vtkPopupMenu = new VtkObjectPopupMenuDipatcher(graphModel.getPipelineManager(), graphModel.getPluginManager());
        popupListener = new PopupListener();
        cellIndex = new Hashtable();
        setBackground(Color.WHITE);
        lineStroke = new BasicStroke(2F);
        enableGroupSelection(true);
        enableGroupDragging(true);
    }

    public void addCell(Cell cell) {
        cellIndex.put(cell.getUI(), cell);
        Component c = cell.getUI();
        Point location = ((VtkObjectCellAdapter) cell).getPosition();
        cell.addGroupDragListener(groupDragListener);
        add(c);
        c.addMouseListener(popupListener);
        c.setBounds(new Rectangle(c.getPreferredSize()));
        c.setLocation(location.x, location.y);
        validate();
        repaint();
    }

    protected void drawConnection(Graphics g, Connection connection) {
        Point sourcePoint = connection.getSource().getConnectionPoint(connection);
        Point targetPoint = connection.getTarget().getConnectionPoint(connection);
        Graphics2D g2 = (Graphics2D) g;
        g2.setColor(Color.BLACK);
        g2.setStroke(lineStroke);
        g2.drawLine(sourcePoint.x, sourcePoint.y, targetPoint.x, targetPoint.y);
    }

    public void update(Observable o, Object arg) {
        repaint();
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
                VtkObject obj = ((VtkObjectCellAdapter) cellIndex.get(e.getSource())).getVtkObject();
                vtkPopupMenu.showPopupMenu(e.getComponent(), e.getX(), e.getY(), obj);
            }
        }
    }
}
