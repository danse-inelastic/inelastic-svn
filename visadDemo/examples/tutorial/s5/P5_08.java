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
  VisAD Tutorial example 5_08
  Like example 5_07, but with a VisADSlider and a Cell
  An animated surface with MathType
   ( time -> (( longitude, latitude )  -> ( altitude, temperature ) ) )
  Run program with java P5_08
 *
 */


public class P5_08{

  // Declare variables
  // The RealTypes

  private RealType time, longitude, latitude;
  private RealType altitude, temperature;


  // The function
  // (( longitude, latitude )  -> ( altitude, temperature ) )

  private FunctionType func_latlon_at;

  // The function
  // ( time -> ( ( longitude, latitude ) -> ( altitude, temperature ) ) )
  private FunctionType func_t_latlon;


  // Our Data values for longitude, latitude are represented by the set

  private Set latlonSet;

  // Time values are given by the set by the set

  private Set timeSet;


  // The FlatField

  private FlatField latlon_at_ff;

  // A FieldImpl

  private FieldImpl timeField;


  // The DataReference from the data to display

  private DataReferenceImpl data_ref;

  // The 2D display, and its the maps

  private DisplayImpl display;
  private ScalarMap timeAnimMap, timeZMap, selValMap;
  private ScalarMap lonXMap, latYMap, altiZMap, temperRGBMap;

  // The VisADSlider

  private VisADSlider vSlider;

  //private AnimationWidget animWid;

  public P5_08 (String[] args)
    throws RemoteException, VisADException {

    // Create the quantities

    altitude = RealType.getRealType("altitude", SI.meter, null);
    temperature = RealType.getRealType("temperature", SI.kelvin, null);

    // The RealTypes above form a tuple

    RealTupleType altitemp = new RealTupleType(altitude, temperature);

    // The RealTypes for the 2D domain

    longitude = RealType.getRealType("longitude", SI.meter, null);
    latitude = RealType.getRealType("latitude", SI.meter, null);

    // The RealTypes above form a tuple

    RealTupleType latlon = new RealTupleType(longitude, latitude);

    time = RealType.getRealTypeByName("Time");



    // Create the functions

    func_latlon_at = new FunctionType(latlon, altitemp);
    func_t_latlon = new FunctionType(time, func_latlon_at );


    // Create the sets: one for lat, lon and the other for time

    int NCOLS = 50;
    int NROWS = NCOLS;

    // the domain set is now 2D

    latlonSet = new Linear2DSet(latlon, -Math.PI, Math.PI, NROWS,
    					       -Math.PI, Math.PI, NCOLS);


    // Time set

    int tSamples = 12;
    double startValue = 10.0;
    timeSet = new Linear1DSet(time, startValue, startValue + tSamples, tSamples);

    // Values for altitude and temperature will go into:

    double[][] flat_samples = new double[2][NCOLS * NROWS];


    // Get the longitude and latitude values in the domain set to help with the calculations
    // "false" means we don't get a copy from the samples

    float[][] set_samples  = latlonSet.getSamples( false );


    // Create a FlatField
    latlon_at_ff = new FlatField( func_latlon_at, latlonSet);

    // ...and a FieldImpl
    timeField = new FieldImpl( func_t_latlon, timeSet);

    // loop for all samples arrays
    for(int t=0;t<tSamples;t++){


    // ...and then loop over columns and rows to calculate individual...

      for(int c = 0; c < NCOLS; c++)

        for(int r = 0; r < NROWS; r++){

          // ...altitude
          flat_samples[0][ c * NROWS + r ] =(float)( (Math.cos( t + 0.90*(double) set_samples[0][ c * NROWS + r ])  )  ) ;


          // ...temperature	values
          flat_samples[1][ c * NROWS + r ] = (float)( (Math.sin( t + 0.50*(double) set_samples[0][ c * NROWS + r ])  ) * Math.cos( (double) set_samples[1][ c * NROWS + r ] ) ) ;


      }

      // set those values in the FlatField
      latlon_at_ff.setSamples(flat_samples);

      // and the FlatField as the t-th Field value
      timeField.setSample( t, latlon_at_ff  );


    }


    // Create Display and its maps

    // The display

    display = new DisplayImplJ3D("display1");
    //display = new DisplayImplJ2D("display1");

    // Get display's graphics mode control draw scales

    GraphicsModeControl dispGMC = (GraphicsModeControl) display.getGraphicsModeControl();

    dispGMC.setScaleEnable(true);


    // Create the ScalarMaps

    lonXMap = new ScalarMap( longitude, Display.XAxis );
    latYMap = new ScalarMap( latitude, Display.YAxis );
    altiZMap = new ScalarMap( altitude, Display.RGB );
    temperRGBMap = new ScalarMap( temperature, Display.ZAxis );
    selValMap = new ScalarMap( time, Display.SelectValue );
    //timeAnimMap = new ScalarMap( time, Display.Animation );
    //timeZMap = new ScalarMap( time, Display.ZAxis );

    // Add maps to display

    display.addMap( lonXMap );
    display.addMap( latYMap );
    display.addMap( altiZMap );
    display.addMap( temperRGBMap );
    display.addMap( selValMap );
    //display.addMap( timeAnimMap );
    //display.addMap( timeZMap );

    temperRGBMap.setRange(-2,2);

    // Create a data reference and set the FieldImpl as our data

    data_ref = new DataReferenceImpl("amp_len_ref");

    data_ref.setData( timeField );

    // Add reference to display

    display.addReference( data_ref );


    // Get the ValueControl from the SelectValue map

    final ValueControl valControl = (ValueControl) selValMap.getControl();

    // Create the slider with the SelectValue map

    final DataReference value_ref = new DataReferenceImpl("value");

    vSlider = new VisADSlider(value_ref, 10, 22, 12,time, "Time (s)");

    CellImpl cell = new CellImpl() {
      public void doAction() throws RemoteException, VisADException {

        valControl.setValue(((Real) value_ref.getData()).getValue());
      }
    };
    cell.addReference(value_ref);



    // Get AnimationControl from the Animation ScalarMap
    //AnimationControl ac = (AnimationControl) timeAnimMap.getControl();

    // and start animation

    //ac.setOn( true );

    // Create the AnimationWidget
    //animWid = new AnimationWidget( timeAnimMap );

    // Create application window, put display into it

    JFrame jframe = new JFrame("VisAD Tutorial example 5_08");
    jframe.getContentPane().setLayout( new BorderLayout());
    jframe.getContentPane().add(display.getComponent(), BorderLayout.CENTER);
    jframe.getContentPane().add(vSlider, BorderLayout.SOUTH);

    // Set window size and make it visible

    jframe.setSize(300, 300);
    jframe.setVisible(true);


  }


  public static void main(String[] args)
    throws RemoteException, VisADException
  {
    new P5_08(args);
  }

} //end of Visad Tutorial Program 5_08
