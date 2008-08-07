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

import java.util.ArrayList;
import java.util.Collection;
import java.util.Iterator;

/**
 * <pre>
 * <b>Project ref           :</b> CASSANDRA project
 * <b>Copyright and license :</b> See relevant sections
 * <b>Status                :</b> under development
 * <b>Creation              :</b> 04/03/2005
 * <b>Modification          :</b>
 *
 * <b>Description  :</b> Concrete class of the Filter
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
public class FilterImpl implements Filter {
    private ArrayList inputDataSet;
    private ArrayList inputMapper;
    private ArrayList inputActor;
    private ArrayList outputDataSet;
    private ArrayList outputMapper;
    private ArrayList outputActor;
    private ArrayList removeListenerList;

    public FilterImpl() {
        inputDataSet = new ArrayList();
        inputMapper = new ArrayList();
        inputActor = new ArrayList();
        outputDataSet = new ArrayList();
        outputMapper = new ArrayList();
        outputActor = new ArrayList();
        removeListenerList = new ArrayList();
    }

    public Collection getInputDataSet() {
        return inputDataSet;
    }

    public Collection getInputMapper() {
        return inputMapper;
    }

    public Collection getInputActor() {
        return inputActor;
    }

    public Collection getOutputDataSet() {
        return outputDataSet;
    }

    public Collection getOutputMapper() {
        return outputMapper;
    }

    public Collection getOutputActor() {
        return outputActor;
    }

    public void addRemoveListener(RemoveListener rl) {
        removeListenerList.add(rl);
    }

    public void remove() {
        for (Iterator i = removeListenerList.iterator(); i.hasNext();) {
            ((RemoveListener) i.next()).remove();
        }
    }

    public void removeRemoveListener(RemoveListener rl) {
        removeListenerList.remove(rl);
    }
}
