/*
VisAD Tutorial
Copyright (C) 2000 Ugo Taddei
*/

package tutorial.s5;

// Import needed classes

import visad.*;
import visad.java2d.DisplayImplJ2D;
import java.rmi.RemoteException;
import java.awt.*;
import javax.swing.*;

/**
  VisAD Tutorial example 5_01
  A simple sine curve, but this time animated.
  Run program with java P5_01
 *
 */


public class P5_01{

  // Declare variables
  // The quantities to be displayed in x- and y-axes

  private RealType length, amplitude;


  // The function amplitude = f(length)
  // as ( length -> amplitude )

  private FunctionType func_len_amp;


  // Our Data values for length are represented by the set

  private Set lengthSet;


  // The Data class FlatField, which will hold data.

  private FlatField amp_len_ff;

  // The DataReference from the data to display

  private DataReferenceImpl amp_len_ref;

  // The 2D display, and its the maps

  private DisplayImpl display;
  private ScalarMap lenXMap, ampYMap, ampRGBMap;


  public P5_01 (String[] args)
    throws RemoteException, VisADException {

    // Create the quantities

    length = RealType.getRealType("length", SI.meter, null);
    amplitude = RealType.getRealType("amplitude", SI.meter, null);


    // Create the function

    func_len_amp = new FunctionType(length,amplitude);


    // Create the domain (length) set
    int nSamples = 32;
    lengthSet = new Linear1DSet(length, -3.0, 3.0, nSamples);


    // Values for amplitude are in an array like float[ rangeDim ][ nSamples]

    float[][] ampVals = new float[1][nSamples];


    // Get the lengthtime values in the domain set to help with the calculations
    // "flase" means we don't get a copy from the samples

    float[][] lenVals  = lengthSet.getSamples( false );

    // Create some amplitude values:


    for(int i=0;i<nSamples;i++){

      ampVals[0][i] = (float) Math.sin( (float) lenVals[0][i] );
    }

    // Create a FlatField
    // Use FlatField(FunctionType type, Set domain_set)


     amp_len_ff = new FlatField( func_len_amp, lengthSet);


     // and initialize it with the first samples array

     amp_len_ff.setSamples( ampVals );


    // Create Display and its maps

    // A 2D display

    display = new DisplayImplJ2D("display1");

    // Get display's graphics mode control draw scales

    GraphicsModeControl dispGMC = (GraphicsModeControl) display.getGraphicsModeControl();

    dispGMC.setScaleEnable(true);


    // Create the ScalarMaps

    lenXMap = new ScalarMap( length, Display.XAxis );
    ampYMap = new ScalarMap( amplitude, Display.YAxis );
    ampRGBMap = new ScalarMap( amplitude, Display.RGB );


    // Add maps to display

    display.addMap( lenXMap );
    display.addMap( ampYMap );
    display.addMap( ampRGBMap );


    // Create a data reference and set the FlatField as our data

    amp_len_ref = new DataReferenceImpl("amp_len_ref");

    amp_len_ref.setData( amp_len_ff );

    // Add reference to display

    display.addReference( amp_len_ref );


    // Create application window, put display into it

    JFrame jframe = new JFrame("VisAD Tutorial example 5_01");
    jframe.getContentPane().add(display.getComponent());

    // Set window size and make it visible

    jframe.setSize(300, 300);
    jframe.setVisible(true);



    // index to count time step
    int index=0;
    // Loop forever, changing the samples array every time
    while(true){
      try{

        // recalculate the values
        for(int i=0;i<nSamples;i++){

          ampVals[0][i] = (float) Math.sin( lenVals[0][i] + (float) index);
        }

        // Update samples
        amp_len_ff.setSamples( ampVals );

        index++;
        Thread.sleep(500);
      }
      catch (InterruptedException ie){
       ie.printStackTrace();
      }

    }

  }


  public static void main(String[] args)
    throws RemoteException, VisADException
  {
    new P5_01(args);
  }

} //end of Visad Tutorial Program 5_01
