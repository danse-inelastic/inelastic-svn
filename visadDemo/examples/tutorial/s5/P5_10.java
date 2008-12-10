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
import visad.jmet.*;

/**
  VisAD Tutorial example 5_10
  Animating a GIF/JPEG image
   ( time -> (( longitude, latitude )  -> ( redType, greenType, blueType ) ) )
  Run program with java P5_10
 *
 */


public class P5_10{

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


  public P5_10 (String[] args)
    throws RemoteException, VisADException {

    if(args.length <= 1){
      System.out.println("run with \"java P5_10 image_1.gif image_2.gif ...\"");
      return;
    }

    // The following will hold the number of images
    int nImages = args.length;

    // Create GIFForm object
    GIFForm image = new GIFForm();

    // Get the image data
    DataImpl imageData = image.open(args[0]);

    // Print out the MathType
    System.out.println(imageData.getType().prettyString());


    // Get the image type. Oh, well, we know it's a FunctionType
    FunctionType functionType = (FunctionType) imageData.getType();


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


    // Define Time and its set

    time = RealType.getRealTypeByName("Time");

    // make set as big enaough to hold all nImages
    timeSet = new Integer1DSet(time, nImages);

    // Make Function ( time -> ( Image-MathType) )

    func_t_latlon = new FunctionType(time, functionType);

    // Make Field

    timeField = new FieldImpl( func_t_latlon, timeSet);

    // Set Field with data from the images

    // set the first on, because it's already open

    timeField.setSample(0, imageData);

    // ...then set the rest
    for(int i=1;i<nImages;i++){

      imageData = image.open(args[i]);
      timeField.setSample(i, imageData);

    }

    // Dump info about data or data type

    DumpType.dumpMathType( func_t_latlon, System.out);
    //DumpType.dumpDataType( timeField, System.out);


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

    timeAnimMap =  new ScalarMap( time, Display.Animation );

    // Add maps to display

    display.addMap( lonXMap );
    display.addMap( latYMap );
    display.addMap( redMap );
    display.addMap( greenMap );
    display.addMap( blueMap );
    display.addMap( timeAnimMap );

    // Create a data reference and set the FieldImpl as our data

    data_ref = new DataReferenceImpl("image_ref");

    data_ref.setData( timeField );

    // Add reference to display

    display.addReference( data_ref );



    // Get AnimationControl from the Animation ScalarMap
    AnimationControl ac = (AnimationControl) timeAnimMap.getControl();

    // and start animation

    ac.setOn( true );

    // Create application window, put display into it

    JFrame jframe = new JFrame("VisAD Tutorial example 5_10");
    jframe.getContentPane().setLayout( new BorderLayout());
    jframe.getContentPane().add(display.getComponent(), BorderLayout.CENTER);

    // Set window size and make it visible

    jframe.setSize(300, 300);
    jframe.setVisible(true);


  }


  public static void main(String[] args)
    throws RemoteException, VisADException
  {
    new P5_10(args);
  }

} //end of Visad Tutorial Program 5_10
