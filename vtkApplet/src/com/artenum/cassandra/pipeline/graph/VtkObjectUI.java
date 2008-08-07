/**
 * Copyright (c) Artenum SARL 2004-2005
 * @author Sebastien Jourdain
 *
 * All rights reserved. This software can
 * not be used or copy or diffused without
 * an explicit license of Artenum SARL, Paris-France
 */
package com.artenum.cassandra.pipeline.graph;

import java.awt.Point;

/**
 * @author Sebastien
 */
public interface VtkObjectUI {
    public Point getPosition();

    public void setName(String newName);
}
