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

import java.awt.Graphics;
import java.awt.Point;

import java.net.URL;

import javax.swing.ImageIcon;
import javax.swing.JLabel;

/**
 * @author Sebastien
 */
public class VtkObjectUI1 extends JLabel implements VtkObjectUI {
    private VtkObject object;
    protected Point position;
    protected ImageIcon glassIcon;
    protected int dx;
    protected int dy;

    public VtkObjectUI1(VtkObject object) {
        this.object = object;
        position = new Point(10, 10);
        //
        ImageIcon icon = null;
        String toolTip = object.getName();
        String txt = toolTip;
        if (txt.length() > 6) {
            txt = txt.substring(0, 6);
            txt += "...";
        }

        setText(txt);
        setToolTipText(toolTip);
        switch (object.getType()) {
        case VtkObject.ACTOR:
            icon = createImageIcon("image/actor.png", "Actor");
            glassIcon = createImageIcon("image/eye.png", "Visible");
            setIcon(icon);
            setVerticalTextPosition(JLabel.BOTTOM);
            setHorizontalTextPosition(JLabel.CENTER);
            setHorizontalAlignment(JLabel.CENTER);
            position.x = 370;
            position.y += ((object.getLocalTypeId().intValue() - 1) * 120);

            dx = (getPreferredSize().width / 2) - 12;
            dy = 25;
            break;
        case VtkObject.MAPPER:
            icon = createImageIcon("image/mapper.png", "Mapper");
            setIcon(icon);
            setText(" ");
            setVerticalTextPosition(JLabel.BOTTOM);
            setHorizontalTextPosition(JLabel.CENTER);
            setHorizontalAlignment(JLabel.CENTER);
            position.x = 250;
            position.y += ((object.getLocalTypeId().intValue() - 1) * 120);
            break;
        case VtkObject.DATASET:
            icon = createImageIcon("image/dataset.png", "DataSet");
            setIcon(icon);
            setVerticalTextPosition(JLabel.BOTTOM);
            setHorizontalTextPosition(JLabel.CENTER);
            setHorizontalAlignment(JLabel.CENTER);
            position.x = 130;
            position.y += ((object.getLocalTypeId().intValue() - 1) * 120);
            break;
        case VtkObject.FILTER:
            icon = createImageIcon("image/filter.png", "Filter");
            setIcon(icon);
            setVerticalTextPosition(JLabel.BOTTOM);
            setHorizontalTextPosition(JLabel.CENTER);
            setHorizontalAlignment(JLabel.CENTER);
            position.x = 10;
            position.y += ((object.getLocalTypeId().intValue() - 1) * 120);
            break;
        case VtkObject.LOOKUP_TABLE:
            icon = createImageIcon("image/lookupTableLinear.png", "Lookup Table");
            setIcon(icon);
            setVerticalTextPosition(JLabel.BOTTOM);
            setHorizontalTextPosition(JLabel.CENTER);
            setHorizontalAlignment(JLabel.CENTER);
            position.x = 490;
            position.y += ((object.getLocalTypeId().intValue() - 1) * 120);
            break;
        case VtkObject.SCALAR_BAR:
            icon = createImageIcon("image/scalarBar.png", "ScalarBar");
            glassIcon = createImageIcon("image/eye.png", "Visible");
            setIcon(icon);
            setVerticalTextPosition(JLabel.BOTTOM);
            setHorizontalTextPosition(JLabel.CENTER);
            setHorizontalAlignment(JLabel.CENTER);
            position.x = 600;
            position.y += ((object.getLocalTypeId().intValue() - 1) * 120);
            dx = (getPreferredSize().width / 2) - 15;
            dy = 25;
            break;
        case VtkObject.TXT_ACTOR:
            icon = createImageIcon("image/txtActor.png", "Text actor");
            glassIcon = createImageIcon("image/eye.png", "Visible");
            setIcon(icon);
            setVerticalTextPosition(JLabel.BOTTOM);
            setHorizontalTextPosition(JLabel.CENTER);
            setHorizontalAlignment(JLabel.CENTER);
            position.x = 440;
            position.y += ((object.getLocalTypeId().intValue() - 1) * 120);
            dx = (getPreferredSize().width / 2) - 12;
            dy = 25;
            break;
        }
    }

    public void setName(String newName) {
        setText(newName);
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

    public void paint(Graphics g) {
        super.paint(g);
        if (((object.getType() == VtkObject.ACTOR) || (object.getType() == VtkObject.SCALAR_BAR) || (object.getType() == VtkObject.TXT_ACTOR)) &&
                (object.getMetaData().get(VtkObject.ACTOR_VISIBLE) != null)) {
            if (((String) object.getMetaData().get(VtkObject.ACTOR_VISIBLE)).equals("true")) {
                g.drawImage(glassIcon.getImage(), dx, dy, glassIcon.getImageObserver());
            }
        }
    }
}
