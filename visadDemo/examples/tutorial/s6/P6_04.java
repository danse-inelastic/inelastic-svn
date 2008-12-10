/*
VisAD Tutorial
Copyright (C) 2000-2001 Ugo Taddei
*/

package tutorial.s6;

// Import needed classes

import visad.*;
import visad.java2d.DisplayImplJ2D;
import visad.java2d.DirectManipulationRendererJ2D;
import java.rmi.RemoteException;
import java.awt.*;
import javax.swing.*;

/**
  VisAD Tutorial example 6_04
  Direct Manipulation
  Use Function.resample( line ) to sample a field
  Use a Cell to perform the necessary action

  Run program with java P6_04
 *
 */


public class P6_04{

  // Declare variables

  // The quantities to be displayed in x- and y-axes

  private RealType easting, latitude, temperature;


  // lat and lon form a domain

  private RealTupleType domain;

  // A Tuple of Reals (a subclass of VisAD Data)
  // which will hold cursor data.

  private Real cursorCoords;

  // and this FlatField will hold the surface
  private FlatField surfsField;


  // The white line
  private Set whiteLine;

  // The DataReferences from the data to display

  private DataReferenceImpl cursorDataRef, surfDataRef;
  private DataReferenceImpl wLineDataRef;


  // The 2D display, and its the maps

  private DisplayImpl display;
  private ScalarMap lonMap, latMap, rgbMap;


  public P6_04 (String[] args)
    throws RemoteException, VisADException {

    // Create the quantities

    easting = RealType.getRealType("easting", SI.meter, null);
    latitude = RealType.getRealType("latitude", SI.meter, null);
    temperature = RealType.getRealType("temperature", SI.kelvin, null);

    //...and the domain
    domain = new RealTupleType(easting, latitude);

    // Create the Data:

    // The cursor
    double initLatitude = 0.50;
    cursorCoords  = new Real(latitude, initLatitude);


    // Create the DataReference

    cursorDataRef = new DataReferenceImpl("cursorDataRef");


    // ...and initialize it with the RealTuple

    cursorDataRef.setData( cursorCoords );


    // More Data: create a Surface object and get its data
    // ...which we know from section 3.5 that is a FlatField
    // with MathType ( (easting, latitude) -> elevation )

    Surface surf = new Surface();
    surfsField = surf.getData();

    surfDataRef = new DataReferenceImpl("surfDataRef");
    surfDataRef.setData(surfsField);

    // Create the white line
    // with so many points

    int numberOfPoints = 100;
    whiteLine = (Set) makeLineSet(initLatitude, numberOfPoints);

    // Create the line's data ref and set data

    wLineDataRef = new DataReferenceImpl("wLineDataRef");
    wLineDataRef.setData(whiteLine);


    CellImpl cell = new CellImpl() {
      public void doAction() throws RemoteException, VisADException {

        // get the data object from the reference. We know it's a RealTuple
        Real lat = (Real) cursorDataRef.getData();

        double latValue = lat.getValue();

        // make a new line
        int nOfPoints = 100;
        whiteLine = (Set) makeLineSet(latValue, nOfPoints);

        // Re-set Data, will update display
        wLineDataRef.setData(whiteLine);


      }
    };

    // link cursor with cell
    // so that doAction gets called whenever cursor moves

    cell.addReference(cursorDataRef);


    // Create the Displays and their maps

    //  2D display

    display = new DisplayImplJ2D("display1");


    // Get display's graphics mode control draw scales

    GraphicsModeControl dispGMC = (GraphicsModeControl) display.getGraphicsModeControl();

    dispGMC.setScaleEnable(true);


    // Create the ScalarMaps

    lonMap = new ScalarMap( easting, Display.XAxis );
    latMap = new ScalarMap( latitude, Display.YAxis );
    rgbMap = new ScalarMap( temperature, Display.RGB );

    // Add maps to display

    display.addMap( lonMap );
    display.addMap( latMap );
    display.addMap( rgbMap );



    // Also create constant maps to define cursor size, color, etc...

    ConstantMap[] cMaps = { new ConstantMap( 0.0f, Display.Red ),
                           new ConstantMap( 1.0f, Display.Green ),
                           new ConstantMap( 0.0f, Display.Blue ),
                           new ConstantMap( 1.0f, Display.XAxis ),
                           new ConstantMap( 3.50f, Display.PointSize )  };


    // Now Add reference to display
    // But using a direct manipulation renderer

    display.addReferences( new DirectManipulationRendererJ2D(), cursorDataRef, cMaps );

    display.addReference(surfDataRef);

    display.addReference(wLineDataRef);




    // Create application window, put display into it

    JFrame jframe = new JFrame("VisAD Tutorial example 6_04");
    jframe.getContentPane().add(display.getComponent());

    // Set window size and make it visible

    jframe.setSize(300, 300);
    jframe.setVisible(true);


  }

  private Set makeLineSet( double latitudeValue, int pointsPerLine )
    throws VisADException, RemoteException
    {

      // arbitrary easting end values of the line

      double lowVal =  -4.0;
      double hiVal =  4.0;


      double[][] domainSamples = new double[2][pointsPerLine];

      double lonVal = lowVal;
      double increment = ( hiVal - lowVal )/ (double) pointsPerLine ;
      for(int i=0;i<pointsPerLine;i++){

        domainSamples[0][i] = lonVal;
        domainSamples[1][i] = latitudeValue;
        lonVal+=increment;
      }


      return new Gridded2DDoubleSet( domain, domainSamples, pointsPerLine);
  }

  public static void main(String[] args)
    throws RemoteException, VisADException
  {
    new P6_04(args);
  }

} //end of Visad Tutorial Program 6_04
