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

import com.artenum.cassandra.vtk.CassandraView;

import vtk.vtkLookupTable;
import vtk.vtkScalarBarActor;
import vtk.vtkTextActor;

import java.io.File;

/**
 * <pre>
 * <b>Project ref           :</b> CASSANDRA project
 * <b>Copyright and license :</b> See relevant sections
 * <b>Status                :</b> under development
 * <b>Creation              :</b> 04/03/2005
 * <b>Modification          :</b>
 *
 * <b>Description  :</b> Core part of Cassandra which take care of the VTK components
 *                that will be shown in the Pipeline editor.
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
public interface PipeLineManager {
    public void addVtkFile(File vtkFile);

    public void setActorVisible(Integer vtkObjectId, boolean viewActor);

    public void setActorVisible(VtkObject vtkObjectActor, boolean viewActor);

    public VtkObject getVtkObject(Integer vtkObjectId);

    public VtkObjectListModel getActorList();

    public VtkObjectListModel getMapperList();

    public VtkObjectListModel getDataSetList();

    public VtkObjectListModel getFilterList();

    public VtkObjectListModel getLookupTableList();

    public VtkObjectListModel getScalarBarList();

    public VtkObjectListModel getTextActorList();

    public VtkObject addActor(Object actor, String name);

    public VtkObject addMapper(Object mapper, String name);

    public VtkObject addDataSet(Object dataset, String name);

    public VtkObject addFilter(Filter filter, String name);

    public VtkObject addScalarBar(vtkScalarBarActor scalarBar, String name);

    public VtkObject addLookupTable(vtkLookupTable lookupTable, String name);

    public VtkObject addTxtActor(vtkTextActor txtActor, String name);

    public void removeVtkObject(Integer vtkObjectId);

    public void removeVtkObject(VtkObject vtkObject);

    public CassandraView getCassandraView();

    public void setAxisVisible(boolean viewAxis);

    public void validateViewAndGo();

    public void validateViewAndWait();

    public void deepValidateView();

    public void notifyConnectivityChange(VtkObject obj);

    public void addConnectivityListener(ConnectivityListener l);

    public void removeConnectivityListener(ConnectivityListener l);
}
