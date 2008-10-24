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
  VisAD Tutorial example 3_09
  We have the functions altitude = h(latitude, longitude)
  			temperature = f(latitude, longitude)

  represented by the MathType
  ( (latitude, longitude) -> (altitude, temperature ) )
  Map the altitude to IsoContour and temperature to RGB
  Run program with "java P3_09"
 */



public class P3_09{

// Declare variables
  // The domain quantities longitude and latitude
  // and the dependent quantities altitude, temperature

  private RealType longitude, latitude;
  private RealType altitude, temperature,  precipitation;

  // Two Tuples: one to pack longitude and latitude together, as the domain
  // and the other for the range (altitude, temperature)

  private RealTupleType domain_tuple, range_tuple;


  // The function (domain_tuple -> range_tuple )

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
  private ScalarMap altIsoMap, tempRGBMap;
  private ScalarMap altRGBMap, tempIsoMap;


  public P3_09(String []args)
    throws RemoteException, VisADException {

    // Create the quantities
    // Use RealType(String name);

    latitude = RealType.getRealType("latitude");
    longitude = RealType.getRealType("longitude");

    domain_tuple = new RealTupleType(latitude, longitude);

    temperature = RealType.getRealType("temperature");
    altitude = RealType.getRealType("altitude");

    // Create the range tuple ( altitude, temperature )
    // Use RealTupleType( RealType[] )

    range_tuple = new RealTupleType( altitude, temperature  );


    // Create a FunctionType (domain_tuple -> range_tuple )
    // Use FunctionType(MathType domain, MathType range)

    func_domain_range = new FunctionType( domain_tuple, range_tuple);

    // Create the domain Set
    // Use LinearDSet(MathType type, double first1, double last1, int lengthX,
    //				     double first2, double last2, int lengthY)

    int NCOLS = 50;
    int NROWS = NCOLS;

    domain_set = new Linear2DSet(domain_tuple, -Math.PI, Math.PI, NROWS,
    					       -Math.PI, Math.PI, NCOLS);




    // Get the Set samples to facilitate the calculations

    float[][] set_samples = domain_set.getSamples( true );


    // We create another array, with the same number of elements of
    // altitude and temperature, but organized as
    // float[2][ number_of_samples ]

    float[][] flat_samples = new float[2][NCOLS * NROWS];

    // ...and then we fill our 'flat' array with the generated values
    // by looping over NCOLS and NROWS

    for(int c = 0; c < NCOLS; c++)

      for(int r = 0; r < NROWS; r++){

	// ...altitude
	flat_samples[0][ c * NROWS + r ] = 01.0f / (float)( (set_samples[0][ c * NROWS + r ] *
						     set_samples[0][ c * NROWS + r ]) +
						     (set_samples[1][ c * NROWS + r ] *
						     set_samples[1][ c * NROWS + r ]) + 1.0f );

	// ...temperature
	flat_samples[1][ c * NROWS + r ] = (float)( (Math.sin( 0.50*(double) set_samples[0][ c * NROWS + r ])  ) * Math.cos( (double) set_samples[1][ c * NROWS + r ] ) ) ;


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


    // Create the ScalarMaps: latitude to XAxis, longitude to YAxis and
    // altitude to RGB and temperature to IsoContour
    // Use ScalarMap(ScalarType scalar, DisplayRealType display_scalar)

    latMap = new ScalarMap( latitude,    Display.YAxis );
    lonMap = new ScalarMap( longitude, Display.XAxis );


    altIsoMap = new ScalarMap( altitude,  Display.IsoContour );
    tempRGBMap = new ScalarMap( temperature,  Display.RGB );


    // Add maps to display

    display.addMap( latMap );
    display.addMap( lonMap );

    display.addMap( altIsoMap );
    display.addMap( tempRGBMap );

    // The ContourControl
    // Note that we get the control from the IsoContour map

    ContourControl isoControl = (ContourControl) altIsoMap.getControl();

    // Define some parameters for contour lines

    float interval = 0.1250f;  // interval between lines

    float lowValue = -2.0f;  // lowest value

    float highValue = 1.0f;   // highest value

    float base = -1.0f;       //  starting at this base value

    // ...and set the lines with the method

    isoControl.setContourInterval(interval, lowValue, highValue, base);
    isoControl.enableLabels(true);

    // Create a data reference and set the FlatField as our data

    data_ref = new DataReferenceImpl("data_ref");

    data_ref.setData( vals_ff );

    // Add reference to display

    display.addReference( data_ref );


    // Create application window and add display to window

    JFrame jframe = new JFrame("VisAD Tutorial example 3_09");
    jframe.getContentPane().add(display.getComponent());


    // Set window size and make it visible

    jframe.setSize(300, 300);
    jframe.setVisible(true);


  }


  public static void main(String[] args)
    throws RemoteException, VisADException
  {
    new P3_09(args);
  }

} //end of Visad Tutorial Program 3_09
