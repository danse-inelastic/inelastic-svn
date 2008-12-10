/*
VisAD Tutorial
Copyright (C) 2000 Ugo Taddei
*/

package tutorial.s5;

// Import needed classes

import visad.*;
import visad.util.*;
import visad.data.gif.*;
import visad.java2d.DisplayImplJ2D;
import visad.java3d.DisplayImplJ3D;
import java.rmi.RemoteException;
import java.awt.*;
import javax.swing.*;
import java.util.Calendar;
import java.util.GregorianCalendar;

/**
  VisAD Tutorial example 5_09
  Analyse the MathType of a GIF/JPEG image
    (( longitude, latitude )  -> ( redType, greenType, blueType ) )
  Run program with java P5_09 image_name
 *
 */


public class P5_09{

  // Declare variables
  // The RealTypes

  private RealType time, longitude, latitude;
  private RealType redType, greenType, blueType;


  // The function
  // ( time -> ( ( longitude, latitude ) -> ( redType, greenType,blueType ) ) )
  private FunctionType func_t_latlon;


  // Our Data values for longitude, latitude are represented by the set

  private Set latlonSet;

  // Time values are given by the set by the set

  private Set timeSet;


  // A FieldImpl

  private FieldImpl timeField;


  // The DataReference from the data to display

  private DataReferenceImpl data_ref;

  // The 2D display, and its the maps

  private DisplayImpl display;
  private ScalarMap timeAnimMap, timeZMap;
  private ScalarMap lonXMap, latYMap, altiZMap;
  private ScalarMap redMap, greenMap, blueMap;

  // The VisADSlider

  private VisADSlider vSlider;

  //private AnimationWidget animWid;

  public P5_09 (String[] args)
    throws RemoteException, VisADException {

    if(args.length != 1){
      System.out.println("run with \"java P5_09 image_nam.gif\"");
      return;
    }

    // Create GIFForm object
    GIFForm image = new GIFForm();

    // Get the image data
    DataImpl imageData = image.open(args[0]);

    // Print out the MathType
    System.out.println(imageData.getType().prettyString());


    // Get the image type. Oh, well, we know it's a FunctionType
    FunctionType functionType = (FunctionType) imageData.getType();

    //MathType imageType = imageData.getType();


    // Get the domain...

    RealTupleType domain = (RealTupleType) functionType.getDomain();

    // ...and the range

    RealTupleType range = (RealTupleType)functionType.getRange();


    // Create the quantities

    longitude = (RealType) domain.getComponent(0);
    latitude = (RealType) domain.getComponent(1);


    redType = (RealType) range.getComponent(0);
    greenType = (RealType) range.getComponent(1);
    blueType = (RealType) range.getComponent(2);



    // Create Display and its maps

    // The display

    //display = new DisplayImplJ3D("display1");
    display = new DisplayImplJ2D("display1");

    // Get display's graphics mode control draw scales

    GraphicsModeControl dispGMC = (GraphicsModeControl) display.getGraphicsModeControl();

    dispGMC.setScaleEnable(true);


    // Create the ScalarMaps

    lonXMap = new ScalarMap( longitude, Display.XAxis );
    latYMap = new ScalarMap( latitude, Display.YAxis );

    redMap =  new ScalarMap( redType, Display.Red );
    greenMap =  new ScalarMap( greenType, Display.Green );
    blueMap =  new ScalarMap( blueType, Display.Blue );

    // Add maps to display

    display.addMap( lonXMap );
    display.addMap( latYMap );
    display.addMap( redMap );
    display.addMap( greenMap );
    display.addMap( blueMap );


    // Create a data reference and set the FieldImpl as our data

    data_ref = new DataReferenceImpl("image_ref");

    data_ref.setData( imageData );

    // Add reference to display

    display.addReference( data_ref );



    // Get AnimationControl from the Animation ScalarMap
    //AnimationControl ac = (AnimationControl) timeAnimMap.getControl();

    // and start animation

    //ac.setOn( true );

    // Create the AnimationWidget
    //animWid = new AnimationWidget( timeAnimMap );

    // Create application window, put display into it

    JFrame jframe = new JFrame("VisAD Tutorial example 5_09");
    jframe.getContentPane().setLayout( new BorderLayout());
    jframe.getContentPane().add(display.getComponent(), BorderLayout.CENTER);

    // Set window size and make it visible

    jframe.setSize(300, 300);
    jframe.setVisible(true);


  }


  public static void main(String[] args)
    throws RemoteException, VisADException
  {
    new P5_09(args);
  }

} //end of Visad Tutorial Program 5_09
