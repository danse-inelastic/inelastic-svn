/*
VisAD Tutorial
Copyright (C) 2000 Ugo Taddei
*/

package tutorial.s2;

// Import needed classes

import visad.*;
import visad.java2d.DisplayImplJ2D;
import java.rmi.RemoteException;
import java.awt.*;
import javax.swing.*;

/**
  VisAD Tutorial example 2_09
  Using a Gridded1DSet to demonstrate a irregular
  sampling of points. These are denser near the peak of the curve
  y = exp( -x^2 ), a gaussian distribution curve
  Run program with java P2_09
 */


public class P2_09{

  // Declare variables
  // The quantities to be displayed in x- and y-axes

  private RealType x, y;


  // The function y = f(x)
  // as ( x -> y )

  private FunctionType func_x_y;


  // Our Data values for x are represented by the set

  private Set x_set;


  // The Data class FlatField, which will hold data.

  private FlatField vals_ff;

  // The DataReference from the data to display

  private DataReferenceImpl data_ref;

  // The 2D display, and its the maps

  private DisplayImpl display;
  private ScalarMap xMap, yMap, yRGBMap;


  public P2_09 (String []args)
    throws RemoteException, VisADException {

    // Create the quantities
    // x and y are measured in SI meters
    // Use RealType(String name, Unit u,  Set set), set is null

    x = RealType.getRealType("X", SI.meter, null);
    y = RealType.getRealType("Y", SI.meter, null);


    // Create the x_set, with the following x samples
    // Gridded1DSet(MathType type, float[][] samples int length)

    int LENGTH = 23;
    float[][] x_vals  = new float[][]{{ -4.0f, -1.7142857f, -1.0285715f, -0.9142857f,
			    -0.8f, -0.6857143f, -0.5714286f, -0.45714286f, -0.34285715f, -0.22857143f,
			    -0.114285715f, 0.0f, 0.114285715f, 0.22857143f,0.34285715f, 0.45714286f,
			    0.5714286f, 0.6857143f, 0.8f, 0.9142857f, 1.0285715f, 1.7142857f, 4.0f}};

    x_set = new Gridded1DSet(x, x_vals, LENGTH);


   // Create a FunctionType, that is the class which represents the function y = f(x)
   // Use FunctionType(MathType domain, MathType range)


    func_x_y = new FunctionType(x, y);

    // These are our actual y values
    // Note that these are y values for the curve y = exp( -x^2 )

    float[][] y_vals = new float[][]{{1.12535176E-7f, 0.0529305f, 0.34716353f, 0.4334762f, 0.5272924f,
			    0.6248747f, 0.72142226f, 0.8114118f, 0.8890951f, 0.9490964f, 0.9870237f,
			    1.0f, 0.9870237f, 0.9490964f, 0.8890951f, 0.8114118f, 0.72142226f, 0.6248747f,
			    0.5272924f, 0.4334762f, 0.34716353f, 0.0529305f, 1.12535176E-7f }};


    // Create a FlatField
    // Use FlatField(FunctionType type, Set domain_set)


     vals_ff = new FlatField( func_x_y, x_set);


     // and put the y values above in it

     vals_ff.setSamples( y_vals );


    // Create Display and its maps

    // A 2D display

    display = new DisplayImplJ2D("display1");

    // Get display's graphics mode control draw scales
    // and change line thickness

    GraphicsModeControl dispGMC = (GraphicsModeControl) display.getGraphicsModeControl();

    dispGMC.setScaleEnable(true);


    // Create the ScalarMaps: quantity x is to be displayed along XAxis and y along YAxis
    // Use ScalarMap(ScalarType scalar, DisplayRealType display_scalar)

    xMap = new ScalarMap( x, Display.XAxis );
    yMap = new ScalarMap( y, Display.YAxis );
    yRGBMap = new ScalarMap( y, Display.RGB );

    // Add maps to display, note that w have a RGB ScalarMap for y

    display.addMap( xMap );
    display.addMap( yMap );
    display.addMap( yRGBMap );

    // Create a data reference and set the FlatField as our data

    data_ref = new DataReferenceImpl("data_ref");

    data_ref.setData( vals_ff );

    // Add reference to display

    display.addReference( data_ref );


    // Create application window, put display into it

    JFrame jframe = new JFrame("VisAD Tutorial example 2_09");
    jframe.getContentPane().add(display.getComponent());

    // Set window size and make it visible

    jframe.setSize(300, 300);
    jframe.setVisible(true);


  }


  public static void main(String[] args)
    throws RemoteException, VisADException
  {
    new P2_09(args);
  }

} //end of Visad Tutorial Program 2_09
