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
import java.util.Vector;

/**
  VisAD Tutorial example 6_05
  Direct Manipulation
  Use Function.resample( line ) to sampe a field
  Show  sampled line with another display
  Use a Cell to perform the necessary action

  Run program with java P6_05
 *
 */


public class P6_05{

  // Declare variables

  // The quantities to be displayed in x- and y-axes

  private RealType easting, northing, temperature;


  // lat and lon form a domain

  private RealTupleType domain;

  // A Tuple of Reals (a subclass of VisAD Data)
  // which will hold cursor data.

  private Real cursorCoords;

  // and this FlatField will hold the surface
  private FlatField surfsField;

  // The temperature line
  private FlatField temperLine;

  // The white line
  private Set whiteLine;

  // The DataReferences from the data to display

  private DataReferenceImpl cursorDataRef, surfDataRef;
  private DataReferenceImpl wLineDataRef, tLineDataRef;


  // The 2D display, and its the maps

  private DisplayImpl[] displays;
  private ScalarMap lonMap, latMap, rgbMap;


  public P6_05 (String[] args)
    throws RemoteException, VisADException {

    // Create the quantities

    easting = RealType.getRealType("easting", SI.meter, null);
    northing = RealType.getRealType("northing", SI.meter, null);
    temperature = RealType.getRealType("temperature", SI.kelvin, null);

    //...and the domain
    domain = new RealTupleType(easting, northing);

    // Create the Data:

    // The cursor
    double initLatitude = 0.50;
    cursorCoords  = new Real(northing, initLatitude);


    // Create the DataReference

    cursorDataRef = new DataReferenceImpl("cursorDataRef");


    // ...and initialize it with the RealTuple

    cursorDataRef.setData( cursorCoords );


    // More Data: create a Surface object and get its data
    // ...which we know from section 3.5 that is a FlatField
    // with MathType ( (easting, northing) -> elevation )

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

    // Create the temperature line to be shown on display

    temperLine = (FlatField) surfsField.resample( whiteLine);
    tLineDataRef = new DataReferenceImpl("tLineDataRef");
    tLineDataRef.setData(temperLine);


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


        // Re-create the temperature line
        temperLine = (FlatField) surfsField.resample( whiteLine);

        // and update ist data reference -> will update display
        tLineDataRef.setData(temperLine);

      }
    };

    // link cursor with cell
    // so that doAction gets called whenever cursor moves

    cell.addReference(cursorDataRef);


    // Create the Displays and their maps

    // Two 2D displays

    displays = new DisplayImpl[2];

    for( int i = 0; i<2;i++){
      displays[i] = new DisplayImplJ2D("display" + i);
    }


    // Get display's graphics mode control draw scales

    for( int i = 0; i<2;i++){
      GraphicsModeControl dispGMC = (GraphicsModeControl) displays[i].getGraphicsModeControl();

    dispGMC.setScaleEnable(true);
    }



    // Create the ScalarMaps

    lonMap = new ScalarMap( easting, Display.XAxis );
    latMap = new ScalarMap( northing, Display.YAxis );
    rgbMap = new ScalarMap( temperature, Display.RGB );

    // Add maps to display

    displays[0].addMap( lonMap );
    displays[0].addMap( latMap );
    displays[0].addMap( rgbMap );


   // Copy those maps and add to second display

   // could get all of display 1 maps with
   //Vector mapsVec =  displays[0].getMapVector();
   /*
   for( int i = 0; i<mapsVec.size();i++){

      ScalarMap sm = (ScalarMap) mapsVec.get(i);
      displays[1].addMap( sm.clone() );
    }
    */

    // but choose only two of the maps

    displays[1].addMap( (ScalarMap) lonMap.clone() );
    displays[1].addMap( (ScalarMap) rgbMap.clone() );



    // Also create constant maps to define cursor size, color, etc...

    ConstantMap[] cMaps = { new ConstantMap( 0.0f, Display.Red ),
                           new ConstantMap( 1.0f, Display.Green ),
                           new ConstantMap( 0.0f, Display.Blue ),
                           new ConstantMap( 1.0f, Display.XAxis ),
                           new ConstantMap( 3.50f, Display.PointSize )  };

    // ...and constant maps to make temperature line slightly thicker

    ConstantMap[] tLineMaps = { new ConstantMap( 2.0f, Display.PointSize )  };


    // Now Add reference to display
    // But using a direct manipulation renderer


    // display 1
    displays[0].addReferences( new DirectManipulationRendererJ2D(), cursorDataRef, cMaps );

    displays[0].addReference(surfDataRef);

    displays[0].addReference(wLineDataRef);


    // display 2

    displays[1].addReference(tLineDataRef, tLineMaps);



    // Create application window, put display into it

    JFrame jframe = new JFrame("VisAD Tutorial example 6_05");
    jframe.getContentPane().setLayout(new GridLayout(1,2) );
    jframe.getContentPane().add(displays[0].getComponent());
    jframe.getContentPane().add(displays[1].getComponent());

    // Set window size and make it visible

    jframe.setSize(600, 300);
    jframe.setVisible(true);


  }

  private Set makeLineSet( double northingValue, int pointsPerLine )
    throws VisADException, RemoteException
    {

      // arbitrary easting end values of the line

      double lowVal =  -4.0;
      double hiVal =  4.0;


      double[][] domainSamples = new double[2][pointsPerLine];

      double lonVal = lowVal;
      double increment = ( hiVal - lowVal )/ (double) (pointsPerLine-1) ;
      for(int i=0;i<pointsPerLine;i++){

        domainSamples[0][i] = lonVal;
        domainSamples[1][i] = northingValue;
        lonVal+=increment;
      }


      return new Gridded2DDoubleSet( domain, domainSamples, pointsPerLine);
  }

  public static void main(String[] args)
    throws RemoteException, VisADException
  {
    new P6_05(args);
  }

} //end of Visad Tutorial Program 6_05
