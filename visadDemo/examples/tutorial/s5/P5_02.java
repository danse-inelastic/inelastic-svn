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
  VisAD Tutorial example 5_02
  A simple sine curve, but this time animated and with a different MathType.
  Use a FieldImpl and Display.Animation
  Run program with java P5_02
 *
 */


public class P5_02{

  // Declare variables
  // The quantities to be displayed in x- and y-axes

  private RealType minute, length, amplitude;


  // The function amplitude = f(length)
  // as ( length -> amplitude )

  private FunctionType func_len_amp;

  // The ( time -> range )
  private FunctionType func_t_range;


  // Our Data values for length are represented by the set

  private Set lengthSet;

  // Time values are given by the set by the set

  private Set timeSet;


  // The Data class FlatField, which will hold data.

  private FlatField amp_len_ff;

  // A FieldImpl, which will hold all data.

  private FieldImpl timeField;


  // The DataReference from the data to display

  private DataReferenceImpl data_ref;

  // The 2D display, and its the maps

  private DisplayImpl display;
  private ScalarMap timeAnimMap, timeZMap, lenXMap, ampYMap, ampRGBMap;


  public P5_02 (String[] args)
    throws RemoteException, VisADException {

    // Create the quantities

    length = RealType.getRealType("length", SI.meter, null);
    amplitude = RealType.getRealType("amplitude", SI.meter, null);

    minute = RealType.getRealType("minute", SI.second, null);

    // Create the functions

    func_len_amp = new FunctionType(length,amplitude);
    func_t_range = new FunctionType(minute, func_len_amp );


    // Create the sets: one for length and the other for time

    int nSamples = 32;
    lengthSet = new Linear1DSet(length, -3.0, 3.0, nSamples);

    // Time set

    int tSamples = 12;
    timeSet = new Integer1DSet(minute,  tSamples);

    // Values for amplitude are in an array like float[ rangeDim ][ nSamples]

    float[][] ampVals = new float[1][nSamples];


    // Get the lengthtime values in the domain set to help with the calculations
    // "flase" means we don't get a copy from the samples

    float[][] lenVals  = lengthSet.getSamples( false );

    // Create some amplitude values:

    // Create a FlatField
    amp_len_ff = new FlatField( func_len_amp, lengthSet);

    // ...and a FieldImpl
    timeField = new FieldImpl( func_t_range, timeSet);

    // loop once for all time steps
    for(int t=0;t<tSamples;t++){

      // and twice to create some "amplitude" values
      for(int i=0;i<nSamples;i++){

        ampVals[0][i] = (float) Math.sin( (float) lenVals[0][i] + t);
      }

       // and initialize it with the samples array
      amp_len_ff.setSamples( ampVals );

      // set amp_len_ff as the t-th component of the Field
      timeField.setSample( t, amp_len_ff  );

    }



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
    timeAnimMap = new ScalarMap( minute, Display.Animation );

    // Add maps to display

    display.addMap( lenXMap );
    display.addMap( ampYMap );
    display.addMap( ampRGBMap );
    display.addMap( timeAnimMap );

    // Create a data reference and set the FieldImpl as our data

    data_ref = new DataReferenceImpl("amp_len_ref");

    data_ref.setData( timeField );

    // Add reference to display

    display.addReference( data_ref );

    // Get AnimationControl from the Animation ScalarMap
    AnimationControl ac = (AnimationControl) timeAnimMap.getControl();

    // and start animation

    ac.setOn( true );

    // Create application window, put display into it

    JFrame jframe = new JFrame("VisAD Tutorial example 5_02");
    jframe.getContentPane().add(display.getComponent());

    // Set window size and make it visible

    jframe.setSize(300, 300);
    jframe.setVisible(true);


  }


  public static void main(String[] args)
    throws RemoteException, VisADException
  {
    new P5_02(args);
  }

} //end of Visad Tutorial Program 5_02
