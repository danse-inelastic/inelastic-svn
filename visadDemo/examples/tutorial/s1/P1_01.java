/*
VisAD Tutorial
Copyright (C) 2000 Ugo Taddei
*/

package tutorial.s1;

// Import needed classes

import visad.*;
import visad.java2d.DisplayImplJ2D;
import java.rmi.RemoteException;
import java.awt.*;
import javax.swing.*;

/**
  Java Tutorial Example 1_01
  The first tutorial example. A function height = f(time), represented by the
  MathType ( time -> height ), is plotted as a simple line.
  this function is actually the parabola height = 45 - 5 * time^2,
  We have the height values and time is the continuous independent variable, with
  data values given by a Set.
  Run program with "java P1_01"
 */


public class P1_01{

  // Declare variables
  // The quantities to be displayed in x- and y-axis

  private RealType time, height;


  // The function height = f(time), represented by ( time -> height )

  private FunctionType func_time_height;


  // Our Data values for time are represented by the set

  private Set time_set;


  // The Data class FlatField, which will hold time and height data.
  // time data are implicitly given by the Set time_set

  private FlatField vals_ff;


  // The DataReference from the data to display

  private DataReferenceImpl data_ref;


  // The 2D display, and its the maps

  private DisplayImpl display;
  private ScalarMap timeMap, heightMap;

  // The constructor for our example class

  public P1_01 (String []args)
    throws RemoteException, VisADException {

    // Create the quantities
    // Use RealType(String name)

    time = RealType.getRealType("time");
    height = RealType.getRealType("height");


    // Create a FunctionType, that is the class which represents our function
    // This is the MathType ( time -> height )
    // Use FunctionType(MathType domain, MathType range)

    func_time_height = new FunctionType(time, height);


    // Create the time_set, with 5 integer values, ranging from 0 to 4.
    // That means, that there should be 5 values for height.
    // Use Integer1DSet(MathType type, int length)

    time_set = new Integer1DSet(time, 5);


    // Those are our actual height values
    // Note the dimensions of the array:
    //   float[ number_of_range_components ][ number_of_range_samples]

    float[][] h_vals = new float[][]{{0.0f, 33.75f, 45.0f, 33.75f, 0.0f,} };


    // Create a FlatField, that is the class for the samples
    // Use FlatField(FunctionType type, Set domain_set)

    vals_ff = new FlatField( func_time_height, time_set);


    // and put the height values above in it

    vals_ff.setSamples( h_vals );


    // Create Display and its maps

    // A 2D display

    display = new DisplayImplJ2D("display1");


    // Create the ScalarMaps: quantity time is to be displayed along x-axis
    // and height along y-axis
    // Use ScalarMap(ScalarType scalar, DisplayRealType display_scalar)

    timeMap = new ScalarMap( time, Display.XAxis );
    heightMap = new ScalarMap( height, Display.YAxis );


    // Add maps to display

    display.addMap( timeMap );
    display.addMap( heightMap );


    // Create a data reference and set the FlatField as our data

    data_ref = new DataReferenceImpl("data_ref");

    data_ref.setData( vals_ff );


    // Add reference to display

    display.addReference( data_ref );


    // Create application window, put display into it

    JFrame jframe = new JFrame("My first VisAD application");
    jframe.getContentPane().add(display.getComponent());


    // Set window size and make it visible

    jframe.setSize(300, 300);
    jframe.setVisible(true);


  }


  public static void main(String[] args)
    throws RemoteException, VisADException
  {
    new P1_01(args);
  }

} //end of Visad Tutorial example 1_01
