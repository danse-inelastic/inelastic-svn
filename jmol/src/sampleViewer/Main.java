package sampleViewer;

import java.io.File;

import javax.swing.JFrame;

import org.openscience.jmol.app.Jmol;

public class Main {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		Jmol jmol = Jmol.getJmol(new JFrame(), 640, 480, "");
		//File temp = new File(System.getProperty("user.home") + "/" + System.nanoTime() + ".xyz");
		File temp = new File(System.getProperty("user.dir") + "/"+args[0]);
		jmol.viewer.openFile(temp.getPath());

	}

}
