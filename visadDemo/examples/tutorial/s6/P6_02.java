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
  VisAD Tutorial example 6_02
  Direct Manipulation of Reals
  represented by a cursor
  Use Function.evaluate() at cursor position
  Use a Cell to perform the necessary action

  Run program with java P6_02
 *
 */


public class P6_02{

  // Declare variables

  // The quantities to be displayed in x- and y-axes

  private RealType easting, northing, temperature;


  // A Tuple of Reals (a subclass of VisAD Data)
  // which will hold cursor data.

  private RealTuple cursorCoords;

  // and this FlatField will hold the surface
  private FlatField surfsField;

  // The DataReference from the data to display

  private DataReferenceImpl cursorDataRef, surfDataRef;


  // The 2D display, and its the maps

  private DisplayImpl display;
  private ScalarMap lonMap, latMap, rgbMap;


  public P6_02 (String[] args)
    throws RemoteException, VisADException {

    // Create the quantities

    easting = RealType.getRealType("easting", SI.meter, null);
    northing = RealType.getRealType("northing", SI.meter, null);
    temperature = RealType.getRealType("temperature", SI.meter, null);


    // Create the Data

    // first createa some "actual" data
    // that is, an array of Reals, quite like a pair of coordinates

    Real[] reals  = { new Real( easting, 0.50),
                      new Real( northing, 0.50) };

    // ...then pack this pair inside a RealTuple

    cursorCoords  = new RealTuple(reals);


    // Create the DataReference

    cursorDataRef = new DataReferenceImpl("cursorDataRef");


    // ...and initialize it with the RealTuple

    cursorDataRef.setData( cursorCoords );

    // More Data: create a Surface object and get its data
    // ...which we know from section 3.5 that is a FlatField
    // with MathType ( (northing, easting) -> elevation )

    Surface surf = new Surface();
    surfsField = surf.getData();

    surfDataRef = new DataReferenceImpl("surfDataRef");
    surfDataRef.setData(surfsField);

    CellImpl cell = new CellImpl() {
      public void doAction() throws RemoteException, VisADException {

        // get the data object from the reference. We know it's a RealTuple
        RealTuple coords = (RealTuple) cursorDataRef.getData();

        // then break the tuple down its components
        Real lon = (Real) coords.getComponent(0);
        Real lat = (Real) coords.getComponent(1);

        // print the value of each component
        System.out.println("Cursor at: (" + lon.getValue() + ", " +
                                            lat.getValue()+ ")");

        // Evaluate the value of the function
        // temperature = f( easting, northing)
        // at the cursor position
        Real tem = (Real) surfsField.evaluate(coords);

        System.out.println("Temperature = "+ tem.getValue() );
      }
    };

    cell.addReference(cursorDataRef);




    // Create Display and its maps

    // A 2D display

    display = new DisplayImplJ2D("display1");

    // Get display's graphics mode control draw scales

    GraphicsModeControl dispGMC = (GraphicsModeControl) display.getGraphicsModeControl();

    dispGMC.setScaleEnable(true);


    // Create the ScalarMaps

    lonMap = new ScalarMap( easting, Display.XAxis );
    latMap = new ScalarMap( northing, Display.YAxis );
    rgbMap = new ScalarMap( temperature, Display.RGB );

    // Add maps to display

    display.addMap( lonMap );
    display.addMap( latMap );
    display.addMap( rgbMap );

    // Also create constant maps to define cursor size, color, etc...

    ConstantMap[] cMaps = { new ConstantMap( 1.0f, Display.Red ),
                           new ConstantMap( 1.0f, Display.Green ),
                           new ConstantMap( 1.0f, Display.Blue ),
                           new ConstantMap( 3.50f, Display.PointSize )  };


    // Now Add reference to display
    // But using a direct manipulation renderer

    display.addReferences( new DirectManipulationRendererJ2D(), cursorDataRef, cMaps );

    display.addReference(surfDataRef);


    // Create application window, put display into it

    JFrame jframe = new JFrame("VisAD Tutorial example 6_02");
    jframe.getContentPane().add(display.getComponent());

    // Set window size and make it visible

    jframe.setSize(300, 300);
    jframe.setVisible(true);


  }


  public static void main(String[] args)
    throws RemoteException, VisADException
  {
    new P6_02(args);
  }

} //end of Visad Tutorial Program 6_02
