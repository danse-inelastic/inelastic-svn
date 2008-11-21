/*
VisAD Tutorial
Copyright (C) 2000 Ugo Taddei
*/

package tutorial.s5;

// Import needed classes

import visad.*;
import visad.util.*;
import visad.java2d.DisplayImplJ2D;
import visad.java3d.DisplayImplJ3D;
import java.rmi.RemoteException;
import java.awt.*;
import javax.swing.*;
import java.util.Calendar;
import java.util.GregorianCalendar;

/**
  VisAD Tutorial example 5_05
  A simple sine curve, like P5_04
  Introduce DateTime
  Run program with java P5_05
 *
 */


public class P5_05{

  // Declare variables
  // The quantities to be displayed in x- and y-axes

  private RealType time, length, amplitude;


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

  private AnimationWidget animWid;

  public P5_05 (String[] args)
    throws RemoteException, VisADException {

    // Create the quantities

    length = RealType.getRealType("length", SI.meter, null);
    amplitude = RealType.getRealType("amplitude", SI.meter, null);

    time = RealType.getRealTypeByName("Time");

    // Create the functions

    func_len_amp = new FunctionType(length,amplitude);
    func_t_range = new FunctionType(time, func_len_amp );


    // Create the sets: one for length and the other for time

    int nSamples = 32;
    lengthSet = new Linear1DSet(length, -3.0, 3.0, nSamples);

    int tSamples = 12;

    // Use java.util.GregorianCalendar to define dates
    // the start date, and end date, tSamples days later
    // See the javadoc of java.util.calendar
    GregorianCalendar startDate = new GregorianCalendar( 1997, Calendar.MAY,  Calendar.DATE);
    GregorianCalendar endDate = new GregorianCalendar( 1997, Calendar.MAY, Calendar.DATE + tSamples -1 );

    // Set the date format pattern, optional
    // See the javadoc of java.text.SimpleDateFormat
    String myDateFormat = "yyyy/MMMM/dd  ";


    // Create a DateTime object and set its date format
    DateTime dt = new DateTime();
    dt.setFormatPattern( myDateFormat );

    // initialize the DateTime object with the start/end dates
    // ...and get the double values from it
    dt = new DateTime( startDate.getTime() );
    double startValue = dt.getValue();

    dt = new DateTime( endDate.getTime() );
    double endValue = dt.getValue();



    // Time set


    timeSet = new Linear1DSet(time, startValue, endValue, tSamples);

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

    // The display

    //display = new DisplayImplJ3D("display1");
    display = new DisplayImplJ2D("display1");

    // Get display's graphics mode control draw scales

    GraphicsModeControl dispGMC = (GraphicsModeControl) display.getGraphicsModeControl();

    dispGMC.setScaleEnable(true);


    // Create the ScalarMaps

    lenXMap = new ScalarMap( length, Display.XAxis );
    ampYMap = new ScalarMap( amplitude, Display.YAxis );
    ampRGBMap = new ScalarMap( amplitude, Display.RGB );
    timeAnimMap = new ScalarMap( time, Display.Animation );
    //timeZMap = new ScalarMap( time, Display.ZAxis );

    // Add maps to display

    display.addMap( lenXMap );
    display.addMap( ampYMap );
    display.addMap( ampRGBMap );
    display.addMap( timeAnimMap );
    //display.addMap( timeZMap );

    // Create a data reference and set the FieldImpl as our data

    data_ref = new DataReferenceImpl("amp_len_ref");

    data_ref.setData( timeField );

    // Add reference to display

    display.addReference( data_ref );

    // Get AnimationControl from the Animation ScalarMap
    AnimationControl ac = (AnimationControl) timeAnimMap.getControl();

    // and start animation

    ac.setOn( true );

    // Create the AnimationWidget
    //animWid = new AnimationWidget( timeAnimMap );

    // Create application window, put display into it

    JFrame jframe = new JFrame("VisAD Tutorial example 5_05");
    //jframe.getContentPane().setLayout( new FlowLayout() );
    jframe.getContentPane().add(display.getComponent());
    //jframe.getContentPane().add(animWid);
    // Set window size and make it visible

    jframe.setSize(300, 300);
    jframe.setVisible(true);



  }


  public static void main(String[] args)
    throws RemoteException, VisADException
  {
    new P5_05(args);
  }

} //end of Visad Tutorial Program 5_05
