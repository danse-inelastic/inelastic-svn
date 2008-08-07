/**
 * Copyright (c) Artenum SARL 2004-2005
 * @author Sebastien Jourdain
 *
 * All rights reserved. This software can
 * not be used or copy or diffused without
 * an explicit license of Artenum SARL, Paris-France
 */
package com.artenum.cassandra.vtk;

import com.artenum.cassandra.pipeline.SimplePipeLineManager;

import vtk.vtkActor;
import vtk.vtkAssembly;
import vtk.vtkAxes;
import vtk.vtkConeSource;
import vtk.vtkPolyDataMapper;
import vtk.vtkTextActor;
import vtk.vtkTubeFilter;

/**
 * @author seb
 */
public class DefaultAxes {
    private double axisLength = 0.8;
    private double axisTextLength = 1.2;
    private SimplePipeLineManager pipelineManager;
    private vtkTextActor xactor;
    private vtkTextActor yactor;
    private vtkTextActor zactor;
    private vtkConeSource xcone;
    private vtkConeSource ycone;
    private vtkConeSource zcone;
    private vtkAssembly assembly;

    public DefaultAxes(SimplePipeLineManager pipelineManager) {
        this.pipelineManager = pipelineManager;
        vtkAxes axes = new vtkAxes();
        axes.SetOrigin(0, 0, 0);
        axes.SetScaleFactor(axisLength);

        xactor = new vtkTextActor();
        yactor = new vtkTextActor();
        zactor = new vtkTextActor();

        xactor.SetInput("X");
        yactor.SetInput("Y");
        zactor.SetInput("Z");

        xactor.ScaledTextOn();
        yactor.ScaledTextOn();
        zactor.ScaledTextOn();

        xactor.GetPositionCoordinate().SetCoordinateSystemToWorld();
        yactor.GetPositionCoordinate().SetCoordinateSystemToWorld();
        zactor.GetPositionCoordinate().SetCoordinateSystemToWorld();

        xactor.GetPositionCoordinate().SetValue(axisLength, 0.0, 0.0);
        yactor.GetPositionCoordinate().SetValue(0.0, axisLength, 0.0);
        zactor.GetPositionCoordinate().SetValue(0.0, 0.0, axisLength);

        xactor.GetTextProperty().SetColor(1.0, 1.0, 1.0);
        xactor.GetTextProperty().ShadowOn();
        xactor.GetTextProperty().ItalicOn();
        xactor.GetTextProperty().BoldOff();

        yactor.GetTextProperty().SetColor(1.0, 1.0, 1.0);
        yactor.GetTextProperty().ShadowOn();
        yactor.GetTextProperty().ItalicOn();
        yactor.GetTextProperty().BoldOff();

        zactor.GetTextProperty().SetColor(1.0, 1.0, 1.0);
        zactor.GetTextProperty().ShadowOn();
        zactor.GetTextProperty().ItalicOn();
        zactor.GetTextProperty().BoldOff();

        xactor.SetMaximumLineHeight(0.25);
        yactor.SetMaximumLineHeight(0.25);
        zactor.SetMaximumLineHeight(0.25);

        vtkTubeFilter tube = new vtkTubeFilter();
        tube.SetInput(axes.GetOutput());
        tube.SetRadius(0.05);
        tube.SetNumberOfSides(8);

        vtkPolyDataMapper tubeMapper = new vtkPolyDataMapper();
        tubeMapper.SetInput(tube.GetOutput());

        vtkActor tubeActor = new vtkActor();
        tubeActor.SetMapper(tubeMapper);
        tubeActor.PickableOff();

        int coneRes = 12;
        double coneScale = 0.3;

        //--- x-Cone
        xcone = new vtkConeSource();
        xcone.SetResolution(coneRes);
        vtkPolyDataMapper xconeMapper = new vtkPolyDataMapper();
        xconeMapper.SetInput(xcone.GetOutput());
        vtkActor xconeActor = new vtkActor();
        xconeActor.SetMapper(xconeMapper);
        xconeActor.GetProperty().SetColor(1, 0, 0);
        xconeActor.SetScale(coneScale, coneScale, coneScale);
        xconeActor.SetPosition(axisLength, 0.0, 0.0);

        //--- y-Cone
        ycone = new vtkConeSource();
        ycone.SetResolution(coneRes);
        vtkPolyDataMapper yconeMapper = new vtkPolyDataMapper();
        yconeMapper.SetInput(ycone.GetOutput());
        vtkActor yconeActor = new vtkActor();
        yconeActor.SetMapper(yconeMapper);
        yconeActor.GetProperty().SetColor(1, 1, 0);
        yconeActor.RotateZ(90);
        yconeActor.SetScale(coneScale, coneScale, coneScale);
        yconeActor.SetPosition(0.0, axisLength, 0.0);

        //--- z-Cone
        zcone = new vtkConeSource();
        zcone.SetResolution(coneRes);
        vtkPolyDataMapper zconeMapper = new vtkPolyDataMapper();
        zconeMapper.SetInput(zcone.GetOutput());
        vtkActor zconeActor = new vtkActor();
        zconeActor.SetMapper(zconeMapper);
        zconeActor.GetProperty().SetColor(0, 1, 0);
        zconeActor.RotateY(-90);
        zconeActor.SetScale(coneScale, coneScale, coneScale);
        zconeActor.SetPosition(0.0, 0.0, axisLength);

        //
        assembly = new vtkAssembly();
        assembly.AddPart(tubeActor);
        assembly.AddPart(xconeActor);
        assembly.AddPart(yconeActor);
        assembly.AddPart(zconeActor);
    }

    public void setVisible(boolean view) {
        if (view) {
            pipelineManager.getCassandraView().GetRenderer().AddActor2D(xactor);
            pipelineManager.getCassandraView().GetRenderer().AddActor2D(yactor);
            pipelineManager.getCassandraView().GetRenderer().AddActor2D(zactor);
            pipelineManager.getCassandraView().GetRenderer().AddActor(assembly);
        } else {
            pipelineManager.getCassandraView().GetRenderer().RemoveActor2D(xactor);
            pipelineManager.getCassandraView().GetRenderer().RemoveActor2D(yactor);
            pipelineManager.getCassandraView().GetRenderer().RemoveActor2D(zactor);
            pipelineManager.getCassandraView().GetRenderer().RemoveActor(assembly);
        }
    }
}
