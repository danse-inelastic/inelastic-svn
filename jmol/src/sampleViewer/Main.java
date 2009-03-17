package sampleViewer;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;

import javax.swing.JFrame;

import org.openscience.jmol.app.Jmol;

public class Main {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		if(args.length==0)
			args = new String[]{"headDynamics1.xyz"};
		Jmol jmol = Jmol.getJmol(new JFrame(), 640, 480, "");
		//File temp = new File(System.getProperty("user.home") + "/" + System.nanoTime() + ".xyz");
		String base = "http://trueblue.caltech.edu/java";//System.getProperty("user.dir");
		String sampleFile = getURLContentAsString(base + File.separatorChar + args[0]);
		//write to sample File to disk, open Jmol, and delete temporary file
		File temp = new File(System.getProperty("user.home") + File.separatorChar + System.nanoTime() + ".cif");
		FileWriter fw = null;
		try {
			fw = new FileWriter(temp);
			fw.write(sampleFile);
			fw.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
		jmol.viewer.openFile(temp.getPath());
		temp.deleteOnExit();		
		
		
//		File temp = new File(System.getProperty("user.dir") + "/"+args[0]);
//		jmol.viewer.openFile(temp.getPath());

	}
	
	public static String getURLContentAsString(String urlString) {
		String content = "";
	    try {
	        // Create a URL for the desired page
	        URL url = new URL(urlString);
	        // Read all the text returned by the server
	        BufferedReader in = new BufferedReader(new InputStreamReader(url.openStream()));
	        String str;
	        while ((str = in.readLine()) != null) {
	            // str is one line of text; readLine() strips the newline character(s)
	        	content+=str;
	        	content+=System.getProperty("line.separator");
	        }
	        in.close();
	    } catch (MalformedURLException e) {
	    } catch (IOException e) {
	    }
		return content;
	}

}
