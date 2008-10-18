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
  VisAD Tutorial example 3_03
  A function with MathType ( (latitude, longitude) -> temperature ) is plotted
  Like previous example, but with different range values for Linear2DSet
  and temperature mapped to Display.Red
  Run program with "java P3_03"
 */



public class P3_03{

// Declare variables
  // The quantities to be displayed in x- and y-axes: longitude and latitude
  // The quantity temperature will be mapped to RGB color

  private RealType longitude, latitude, temperature;

  // A Tuple, to pack longitude and latitude together, as the domain

  private RealTupleType domain_tuple;


  // The function ( (latitude, longitude) -> temperature )
  // That is, (domain_tuple -> temperature )

  private FunctionType func_dom_temp;


   // Our Data values for the domain are represented by the Set

  private Set domain_set;


  // The Data class FlatField

  private FlatField vals_ff;

  // The DataReference from data to display

  private DataReferenceImpl data_ref;

  // The 2D display, and its the maps
  // note the red, green and blue CostantMaps

  private DisplayImpl display;
  private ScalarMap latMap, lonMap, tempMap;
  private ConstantMap redCMap, greenCMap, blueCMap;


  public P3_03(String []args)
    throws RemoteException, VisADException {

    // Create the quantities
    // Use RealType(String name);

    latitude = RealType.getRealType("latitude");
    longitude = RealType.getRealType("longitude");

    domain_tuple = new RealTupleType(latitude, longitude);

    temperature = RealType.getRealType("temperature");


   // Create a FunctionType (domain_tuple -> temperature )
   // Use FunctionType(MathType domain, MathType range)

    func_dom_temp = new FunctionType( domain_tuple, temperature);

    // Create the domain Set, with 5 columns and 6 rows, using an
    // LinearDSet(MathType type, double first1, double last1, int lengthX,
    //				 double first2, double last2, lengthY)

    int NCOLS = 5;
    int NROWS = 6;

    domain_set = new Linear2DSet(domain_tuple, 0.0, 12.0, NROWS,
    					       0.0, 5.0, NCOLS);



    // Our temperature values, given as a float[6][5] array

    float[][] temp_vals = new float[][]{{0, 6, 12, 18, 24},
    					 {1, 7, 12, 19, 25},
					 {2, 8, 14, 20, 26},
					 {3, 9, 15, 21, 27},
					 {4, 10, 16, 22, 28},
					 {5, 11, 17, 23, 29}  };

    // We create another array, with the same number of elements of
    // temperature_vals[][], but organized as float[1][ number_of_samples ]

    float[][] flat_samples = new float[1][NCOLS * NROWS];

    // ...and then we fill our 'flat' array with the original values
    // Note that the temperature values indicate the order in which these values
    // are stored in flat_samples

    for(int c = 0; c < NCOLS; c++)
      for(int r = 0; r < NROWS; r++)

	flat_samples[0][ c * NROWS + r ] = temp_vals[r][c];


    // Create a FlatField
    // Use FlatField(FunctionType type, Set domain_set)

    vals_ff = new FlatField( func_dom_temp, domain_set);

     // ...and put the temperature values above into it

    vals_ff.setSamples( flat_samples );

    // Create Display and its maps

    // A 2D display

    display = new DisplayImplJ2D("display1");

    // Get display's graphics mode control and draw scales

    GraphicsModeControl dispGMC = (GraphicsModeControl) display.getGraphicsModeControl();
    dispGMC.setScaleEnable(true);


    // Create the ScalarMaps: latitude to YAxis, longitude to XAxis and
    // temperature to  to Red
    // Use ScalarMap(ScalarType scalar, DisplayRealType display_scalar)

    latMap = new ScalarMap( latitude,    Display.YAxis );
    lonMap = new ScalarMap( longitude, Display.XAxis );
    tempMap = new ScalarMap( temperature,  Display.Red );

    // uncomment the following line (and comment the prevous line) to get...

      // ...temperature to Green
  //  tempMap = new ScalarMap( temperature,  Display.Green );

      // ...temperature to blue
  //  tempMap = new ScalarMap( temperature,  Display.Blue );

      // ...temperature to Cyan, Magenta, Yellow
   //tempMap = new ScalarMap( temperature,  Display.Cyan );
   //tempMap = new ScalarMap( temperature,  Display.Magenta );
   //tempMap = new ScalarMap( temperature,  Display.Yellow );

      // ...temperature to CMY (Cyan, Magenta, Yellow)
  //  tempMap = new ScalarMap( temperature,  Display.CMY );

      // ...temperature to Value, also known as Brightness
  //  tempMap = new ScalarMap( temperature,  Display.Value );


    // Also create three ConstantMaps for red, green and blue

    double red = 0.0;
    double green = 0.0;
    double blue = 0.0;

    redCMap = new ConstantMap( red, Display.Red );
    greenCMap = new ConstantMap( green, Display.Green );
    blueCMap  = new ConstantMap( blue, Display.Blue );


    // Add maps to display

    display.addMap( latMap );
    display.addMap( lonMap );
    display.addMap( tempMap );

      // constant maps

    //display.addMap( redCMap );
    display.addMap( greenCMap );
    display.addMap( blueCMap );

    // Create a data reference and set the FlatField as our data

    data_ref = new DataReferenceImpl("data_ref");

    data_ref.setData( vals_ff );

    // Add reference to display

    display.addReference( data_ref );


    // Create application window and add display to window

    JFrame jframe = new JFrame("VisAD Tutorial example 3_03");
    jframe.getContentPane().add(display.getComponent());


    // Set window size and make it visible

    jframe.setSize(300, 300);
    jframe.setVisible(true);


  }


  public static void main(String[] args)
    throws RemoteException, VisADException
  {
    new P3_03(args);
  }

} //end of Visad Tutorial Program 3_03
