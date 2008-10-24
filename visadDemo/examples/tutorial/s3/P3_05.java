/*
VisAD Tutorial
Copyright (C) 2000 Ugo Taddei
*/

package tutorial.s3;

// Import needed classes

import visad.*;
import visad.java2d.DisplayImplJ2D;
import java.rmi.RemoteException;
import java.awt.*;
import javax.swing.*;
import java.awt.event.*;

  /**
  VisAD Tutorial example 3_05
  We have the function temperature = f(latitude, longitude)
  represented by the MathType
  ( (latitude, longitude) -> elevation )
  Map the elevation  and temperature  to IsoContour (and to RGB)
  Run program with "java P3_05"
 */



public class P3_05{

// Declare variables
  // The domain quantities longitude and latitude
  // and the dependent quantity temperature

  private RealType longitude, latitude;
  private RealType temperature;

  // Tuple to pack longitude and latitude together, as the domain

  private RealTupleType domain_tuple;


  // The function (domain_tuple -> temperature )
  // Remeber, range is only "temperature"

  private FunctionType func_domain_range;


   // Our Data values for the domain are represented by the Set

  private Set domain_set;


  // The Data class FlatField

  private FlatField vals_ff;

  // The DataReference from data to display

  private DataReferenceImpl data_ref;

  // The 2D display, and its the maps

  private DisplayImpl display;
  private ScalarMap latMap, lonMap;
  private ScalarMap tempIsoMap, tempRGBMap;


  public P3_05(String []args)
    throws RemoteException, VisADException {

    // Create the quantities
    // Use RealType(String name);

    latitude = RealType.getRealType("latitude");
    longitude = RealType.getRealType("longitude");

    domain_tuple = new RealTupleType(latitude, longitude);

    temperature = RealType.getRealType("temperature");

    // Create a FunctionType (domain_tuple -> range_tuple )
    // Use FunctionType(MathType domain, MathType range)

    func_domain_range = new FunctionType( domain_tuple, temperature);

    // Create the domain Set
    // Use LinearDSet(MathType type, double first1, double last1, int lengthX,
    //				     double first2, double last2, int lengthY)

    int NCOLS = 50;
    int NROWS = NCOLS;

    domain_set = new Linear2DSet(domain_tuple, -Math.PI, Math.PI, NROWS,
    					       -Math.PI, Math.PI, NCOLS);



    // Get the Set samples to facilitate the calculations

    float[][] set_samples = domain_set.getSamples( true );


    // The actual temperature values are stored in this array
    // float[1][ number_of_samples ]

    float[][] flat_samples = new float[1][NCOLS * NROWS];

    // We fill our 'flat' array with the generated values
    // by looping over NCOLS and NROWS

    for(int c = 0; c < NCOLS; c++)

      for(int r = 0; r < NROWS; r++){

	// ...temperature
	flat_samples[0][ c * NROWS + r ] = (float)( (Math.sin( 0.50*(double) set_samples[0][ c * NROWS + r ])  ) * Math.cos( (double) set_samples[1][ c * NROWS + r ] ) ) ;


    }


    // Create a FlatField
    // Use FlatField(FunctionType type, Set domain_set)

    vals_ff = new FlatField( func_domain_range, domain_set);

    // ...and put the values above into it

    // Note the argument false, meaning that the array won't be copied

    vals_ff.setSamples( flat_samples , false );

    // Create Display and its maps

    // A 2D display

    display = new DisplayImplJ2D("display1");

    // Get display's graphics mode control and draw scales

    GraphicsModeControl dispGMC = (GraphicsModeControl)  display.getGraphicsModeControl();
    dispGMC.setScaleEnable(true);


    // Create the ScalarMaps: latitude to YAxis, longitude to XAxis and
    // temperature to IsoContour and eventualy to RGB
    // Use ScalarMap(ScalarType scalar, DisplayRealType display_scalar)

    latMap = new ScalarMap( latitude,    Display.YAxis );
    lonMap = new ScalarMap( longitude, Display.XAxis );

    // This is new!

    tempIsoMap = new ScalarMap( temperature,  Display.IsoContour );

    // this ScalarMap will color the isolines
    // don't foget to add it to the display

    tempRGBMap = new ScalarMap( temperature,  Display.RGB );


    // Add maps to display

    display.addMap( latMap );
    display.addMap( lonMap );

    display.addMap( tempIsoMap );
    //display.addMap( tempRGBMap );


    // Create a data reference and set the FlatField as our data

    data_ref = new DataReferenceImpl("data_ref");

    data_ref.setData( vals_ff );

    // Add reference to display

    display.addReference( data_ref );


    // Create application window and add display to window

    JFrame jframe = new JFrame("VisAD Tutorial example 3_05");
    jframe.getContentPane().add(display.getComponent());


    // Set window size and make it visible

    jframe.setSize(300, 300);
    jframe.setVisible(true);


  }


  public static void main(String[] args)
    throws RemoteException, VisADException
  {
    new P3_05(args);
  }

} //end of Visad Tutorial Program 3_05
