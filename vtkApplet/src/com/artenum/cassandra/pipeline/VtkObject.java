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

import com.artenum.graph.interfaces.Cell;

import java.util.Hashtable;

/**
 * <pre>
 * <b>Project ref           :</b> CASSANDRA project
 * <b>Copyright and license :</b> See relevant sections
 * <b>Status                :</b> under development
 * <b>Creation              :</b> 04/03/2005
 * <b>Modification          :</b>
 *
 * <b>Description  :</b> Meta VTK Component.
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
public interface VtkObject extends Cell {
    public final static int ACTOR = 1;
    public final static int MAPPER = 2;
    public final static int DATASET = 3;
    public final static int FILTER = 4;
    public final static int LOOKUP_TABLE = 5;
    public final static int SCALAR_BAR = 6;
    public final static int TXT_ACTOR = 7;
    public final static String ACTOR_VISIBLE = "ACTOR_VISIBLE";
    public final static String CELL = "CELL";
    public final static String POPUP_MENU = "POPUP_MENU";

    public Integer getId();

    public Integer getLocalTypeId();

    public String getName();

    public void setName(String newName);

    public int getType();

    public Object getVtkObject();

    public Hashtable getMetaData();

    public boolean isValide();

    public void setValide(boolean valide);
}
