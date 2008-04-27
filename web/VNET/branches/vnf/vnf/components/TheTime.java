import java.awt.*;
import javax.swing.*;
import java.io.*;
import java.net.*;

public class TheTime {
  public static void main(String args[]) {
    JFrame frame =  new JFrame("Time Check"); 
    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    JLabel label = new JLabel();
    Container content = frame.getContentPane();  
    content.add(label, BorderLayout.CENTER);
    String message = "missing";
    BufferedReader reader = null;
    try {
      Socket socket = new Socket("time.nist.gov", 13);
      InputStream is = socket.getInputStream();
      InputStreamReader isr = new InputStreamReader(is);
      reader = new BufferedReader(isr);
      reader.readLine(); // skip blank line
      message = reader.readLine();
    } catch (MalformedURLException e) {
      System.err.println("Malformed: " + e);
    } catch (IOException e) {
      System.err.println("I/O Exception: " + e);
    } finally {
      if (reader != null) {
        try {
          reader.close();
        } catch (IOException ignored) {
        }
      }
    }
    label.setText(message);
    frame.pack();
    frame.show();
  }
}