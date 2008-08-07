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

import vtk.vtkLookupTable;

import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Point;
import java.awt.geom.Rectangle2D;

import java.net.URL;

import javax.swing.ImageIcon;
import javax.swing.JLabel;

/**
 * @author Sebastien
 */
public class VtkObjectUI2 extends JLabel implements VtkObjectUI {
    private VtkObject object;
    protected final Dimension size = new Dimension(59, 66);
    protected Point position;
    protected String txt;
    protected ImageIcon glassIcon;
    protected ImageIcon glassIcon2;
    protected ImageIcon icon;
    private final int deltaX = 100;
    private final int deltaY = 80;

    public VtkObjectUI2(VtkObject object) {
        this.object = object;
        position = new Point(10, 10);
        //
        txt = object.getName();
        setToolTipText(txt);
        if (txt.length() > 6) {
            txt = txt.substring(0, 6);
            txt += "...";
        }

        switch (object.getType()) {
        case VtkObject.ACTOR:
            icon = createImageIcon("icon/actor.png", "Actor");
            glassIcon = createImageIcon("icon/actorEye.png", "Visible");
            position.x = deltaX * 4;
            position.y += ((object.getLocalTypeId().intValue() - 1) * deltaY);
            break;
        case VtkObject.MAPPER:
            icon = createImageIcon("icon/mapper.png", "Mapper");
            txt = "";
            position.x = deltaX * 3;
            position.y += ((object.getLocalTypeId().intValue() - 1) * deltaY);
            break;
        case VtkObject.DATASET:
            icon = createImageIcon("icon/dataset.png", "DataSet");
            position.x = deltaX * 2;
            position.y += ((object.getLocalTypeId().intValue() - 1) * deltaY);
            break;
        case VtkObject.FILTER:
            icon = createImageIcon("icon/filter.png", "Filter");
            position.x = deltaX * 1;
            position.y += ((object.getLocalTypeId().intValue() - 1) * deltaY);
            break;
        case VtkObject.LOOKUP_TABLE:
            icon = createImageIcon("icon/lookuptable.png", "Lookup Table");
            glassIcon = createImageIcon("icon/linearLT.png", "Lookup Table");
            glassIcon2 = createImageIcon("icon/logLT.png", "Lookup Table");
            position.x = deltaX * 5;
            position.y += ((object.getLocalTypeId().intValue() - 1) * deltaY);
            break;
        case VtkObject.SCALAR_BAR:
            icon = createImageIcon("icon/scalarBar.png", "ScalarBar");
            glassIcon = createImageIcon("icon/actorEye.png", "Visible");
            position.x = deltaX * 6;
            position.y += ((object.getLocalTypeId().intValue() - 1) * deltaY);
            break;
        case VtkObject.TXT_ACTOR:
            icon = createImageIcon("icon/txtActor.png", "Text actor");
            glassIcon = createImageIcon("icon/txtActorEye.png", "Visible");
            position.x = deltaX * 7;
            position.y += ((object.getLocalTypeId().intValue() - 1) * deltaY);
            break;
        }

        setIcon(icon);
    }

    public void setName(String newName) {
        txt = newName;
        repaint();
    }

    protected static ImageIcon createImageIcon(String path, String description) {
        URL imgURL = VtkObjectCellAdapter.class.getResource(path);
        if (imgURL != null) {
            return new ImageIcon(imgURL, description);
        } else {
            System.err.println("Couldn't find file: " + imgURL);
            return null;
        }
    }

    public void savePosition() {
        position = getLocation();
        if (position.x < 0) {
            position.x = 0;
        }

        if (position.y < 0) {
            position.y = 0;
        }

        setLocation(position);
    }

    public void setPosition(Point p) {
        position = p;
        if (position.x < 0) {
            position.x = 0;
        }

        if (position.y < 0) {
            position.y = 0;
        }

        setLocation(position);
    }

    public Point getPosition() {
        return position;
    }

    public Dimension getSize() {
        return size;
    }

    public void paint(Graphics g) {
        super.paint(g);
        //g.drawImage(icon.getImage(), 0, 0, icon.getImageObserver());
        if (((object.getType() == VtkObject.ACTOR) || (object.getType() == VtkObject.SCALAR_BAR) || (object.getType() == VtkObject.TXT_ACTOR)) &&
                (object.getMetaData().get(VtkObject.ACTOR_VISIBLE) != null)) {
            if (((String) object.getMetaData().get(VtkObject.ACTOR_VISIBLE)).equals("true")) {
                g.drawImage(glassIcon.getImage(), 0, 0, glassIcon.getImageObserver());
            }
        } else if (object.getType() == VtkObject.LOOKUP_TABLE) {
            if (((vtkLookupTable) object.getVtkObject()).GetScale() == 0) {
                g.drawImage(glassIcon.getImage(), 0, 0, glassIcon.getImageObserver());
            } else {
                g.drawImage(glassIcon2.getImage(), 0, 0, glassIcon2.getImageObserver());
            }
        }

        // write txt
        Rectangle2D txtR = g.getFontMetrics().getStringBounds(txt, g);

        // 59 * 66
        int dx = (int) (59 - txtR.getWidth()) / 2;
        g.drawString(txt, dx, 66);
    }
}
