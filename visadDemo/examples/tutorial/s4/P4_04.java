/*
VisAD Tutorial
Copyright (C) 2000 Ugo Taddei
*/

package tutorial.s4;

// Import needed classes

import visad.*;
import visad.util.*;
import visad.java3d.DisplayImplJ3D;
import java.rmi.RemoteException;
import java.awt.*;
import javax.swing.*;
import java.awt.event.*;

  /**
  VisAD Tutorial example 4_04
  Define a color table
  We have the function altitude = h(latitude, longitude)

  represented by the MathType
  ( (latitude, longitude) -> altitude )
  altitude values in the code
  Use a LabeledColorWidget
  Run program with "java P4_04"
 */



public class P4_04{

// Declare variables
  // The domain quantities longitude and latitude
  // and the dependent quantity altitude

  private RealType longitude, latitude;
  private RealType altitude;

  // Tuple to pack longitude and latitude together

  private RealTupleType domain_tuple;


  // The function (domain_tuple -> altitude )

  private FunctionType func_domain_alt;


   // Our Data values for the domain are represented by the Set

  private Set domain_set;


  // The Data class FlatField

  private FlatField vals_ff;

  // The DataReference from data to display

  private DataReferenceImpl data_ref;

  // The 2D display, and its the maps

  private DisplayImpl display;
  private ScalarMap latMap, lonMap;
  private ScalarMap altMap, altRGBMap;

  private LabeledColorWidget labelCW;

  // Our color table

  private float[][] myColorTable;

  public P4_04(String []args)
    throws RemoteException, VisADException {

    // Create the quantities
    // Use RealType(String name, Unit unit, Set set);

    latitude = RealType.getRealType("latitude", SI.meter, null);
    longitude = RealType.getRealType("longitude", SI.meter, null);

    domain_tuple = new RealTupleType(latitude, longitude);

    altitude = RealType.getRealType("altitude", SI.meter, null);

    // Create a FunctionType (domain_tuple -> range_tuple )
    // Use FunctionType(MathType domain, MathType range)

    func_domain_alt = new FunctionType( domain_tuple, altitude);

    // Create the domain Set, with 12 columns and 6 rows, using an
    // LinearDSet(MathType type, double first1, double last1, int lengthX,
    //				 double first2, double last2, int lengthY)

    // note the "inverted" first and last values of latitude

    int NCOLS = 12;
    int NROWS = 6;

    domain_set = new Linear2DSet(domain_tuple, 6000.0,     0.0, NROWS,
    					          0.0,  10000.0, NCOLS);



    // The actal altitudes values
    // ordered as float[ NROWS ][ NCOLS ]

    double[][] alt_samples = new double[][]{
     {3000.0,   3000.0,   6500.0,   4000.0,   3500.0,   4000.0,   5500.0,   4000.0,   4000.0,   4000.0,   5000.0,   1000 },
     {1000.0,   1500.0,   4000.0,   3500.0,   6300.0,   4500.0,   4000.0,   3800.0,   3800.0,   3800.0,   5000.0,   6400 },
     {  0.0,      0.0,       0.0,   1500.0,   3000.0,   6500.0,   4500.0,   5000.0,   4000.0,   3800.0,   3800.0,   6200 },
     {-3000.0,   -2000.0,   -1000.0,    0.0,   1500.0,   1000.0,   4000.0,   5800.0,   4000.0,   4000.0,   3900.0,   3900 },
     {-3000.0,   -4000.0,   -2000.0,   -1000.0,  0.0,   1000.0,   1500.0,   4000.0,   5700.0,   4500.0,   4000.0,   4000.0 },
     {-6500.0,   -6000.0,   -4000.0,   -3000.0,   0.0,   100.0,   1500.0,   4500.0,   6000.0,   4000.0,   4000.0,   4000.0 }};


    // Our 'flat' array

    double[][] flat_samples = new double[1][NCOLS * NROWS];

    // Fill our 'flat' array with the altitude values
    // by looping over NCOLS and NROWS

    // Note the use of an index variable, indicating the order of the samples

    int index = 0;

    for(int c = 0; c < NCOLS; c++)

      for(int r = 0; r < NROWS; r++){

	      // set altitude
	      flat_samples[0][ index ] = alt_samples[r][c];

	      // increment index
	      index++;
      }

    // Create a FlatField
    // Use FlatField(FunctionType type, Set domain_set)

    vals_ff = new FlatField( func_domain_alt, domain_set);


    FlatField der_vals_ff ;//= new FlatField( func_domain_alt, domain_set);


    // ...and put the altitude values above into it

    // Note the argument false, meaning that the array won't be copied

    vals_ff.setSamples( flat_samples , false );


    der_vals_ff = (FlatField) vals_ff.derivative( longitude, Data.NO_ERRORS );//.setSamples( flat_samples , false );


    // Create Display and its maps

    // This is new: a 3D display

    display = new DisplayImplJ3D("display1");

    // Get display's graphics mode control and draw scales

    GraphicsModeControl dispGMC = (GraphicsModeControl)  display.getGraphicsModeControl();
    dispGMC.setScaleEnable(true);


    // Create the ScalarMaps: latitude to XAxis, longitude to YAxis and
    // altitude to ZAxis and to RGB
    // Use ScalarMap(ScalarType scalar, DisplayRealType display_scalar)

    latMap = new ScalarMap( latitude,    Display.YAxis );
    lonMap = new ScalarMap( longitude, Display.XAxis );


    altRGBMap = new ScalarMap( altitude,  Display.RGB );

    altMap = new ScalarMap( altitude,  Display.ZAxis );

    // Add maps to display

    display.addMap( latMap );
    display.addMap( lonMap );

    display.addMap( altMap );
    display.addMap( altRGBMap );

    // Create a color table
    // Note: table has red, green and blue components
    // and is 8 units long, i.e float[3][8]

    myColorTable = new float[][]{{0.0f, 1.0f, 0.0f, 0.0f, 0.0f, 1.0f, 1.0f, 1.0f},  // red component
                                 {0.0f, 0.0f, 1.0f, 0.0f, 1.0f, 0.0f, 1.0f, 1.0f},  // green component
                                 {0.0f, 0.0f, 0.0f, 1.0f, 1.0f, 1.0f, 0.0f, 1.0f}}; // blue component



    // Create a LabeledColorWidget with an
    // RGB ScalarMap and a user-defined color table

    labelCW = new LabeledColorWidget( altRGBMap, myColorTable );


    // Create a data reference and set the FlatField as our data

    data_ref = new DataReferenceImpl("data_ref");
    data_ref.setData( vals_ff );


    display.addReference( data_ref);


    // Create application window and add display to window

    JFrame jframe = new JFrame("VisAD Tutorial example 4_04");
    jframe.getContentPane().setLayout(new FlowLayout());
    jframe.getContentPane().add(display.getComponent());

    // Add the LabeledColorWidget to the frame


    jframe.getContentPane().add(labelCW);

    // Set window size and make it visible

    jframe.setSize(550, 300);
    jframe.setVisible(true);


  }


  public static void main(String[] args)
    throws RemoteException, VisADException
  {
    new P4_04(args);
  }

} //end of Visad Tutorial Program 4_04
