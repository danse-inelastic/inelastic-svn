package diagrams;

import java.awt.Color;
import java.awt.Font;
import java.awt.Image;

import javax.swing.SwingConstants;

import de.jreality.backends.label.LabelUtility;
import de.jreality.geometry.IndexedLineSetFactory;
import de.jreality.geometry.PointSetFactory;
import de.jreality.geometry.Primitives;
import de.jreality.math.MatrixBuilder;
import de.jreality.scene.Appearance;
import de.jreality.scene.IndexedLineSet;
import de.jreality.scene.SceneGraphComponent;
import de.jreality.shader.ImageData;
import de.jreality.shader.Texture2D;
import de.jreality.shader.TextureUtility;
import de.jreality.ui.viewerapp.ViewerApp;

public class NeutronCoordinates {

	public static void main(String[] args) {

		IndexedLineSetFactory ilsf = new IndexedLineSetFactory();

		double [][] vertices = new double[][] {
				{0, 0, 0}, {1, 0, 0}, {0, 1, 0}, {0, 0, 1}, {0,0,-1}, {1,1,1}
		};

		int[][] edgeIndices = new int[][]{
				{0, 1}, {0, 2}, {0, 3}, {0, 4}, {0,5}  
		};

		ilsf.setVertexCount( vertices.length );
		ilsf.setVertexCoordinates( vertices );
		ilsf.setLineCount(edgeIndices.length);
		ilsf.setEdgeIndices(edgeIndices);

		ilsf.update();
		
	    PointSetFactory psf = new PointSetFactory();
	    psf.setVertexCount(1);
	    psf.setVertexCoordinates(new double[]{0,0,0});
	    psf.setVertexColors(new double[]{0,0,0,0});
	    psf.setVertexLabels(new String[]{"my label"});
	    psf.update();
	    SceneGraphComponent cmp = new SceneGraphComponent();
	    cmp.setGeometry(psf.getPointSet());
	    
	    Appearance app = new Appearance();
	    app.setAttribute("pointShader.textShader.alignment", SwingConstants.CENTER);
	    double offx= -1.0;	
	    double offy = 1.0;
	    double offz=1.0;
	    app.setAttribute("pointShader.textShader.offset", new double[]{offx, offy, offz});
		
		
//	    // create the image
//	    Font f = new Font("Sans Serif", Font.PLAIN, 24);
//	    Image img = LabelUtility.createImageFromString("label text", f, Color.blue);
//
//	    Appearance app = new Appearance();
//	    app.setAttribute("showPoints", false);
//	   
//	    // otherwise there is a black border around the letters
//	    app.setAttribute("transparencyEnabled", true);
//
//	    // create the texture
//	    Texture2D tex = TextureUtility.createTexture(app, "polygonShader", new ImageData(img));
//
//	    // display it on a quad
//	    SceneGraphComponent cmp = new SceneGraphComponent();
//	    MatrixBuilder.euclidean().rotateX(Math.PI).assignTo(cmp);
//	    IndexedLineSet quad = Primitives.plainQuadMesh(0.01*img.getWidth(null), 0.01*img.getHeight(null),1,1);
//	    cmp.setAppearance(app);
//	    cmp.setGeometry(quad);
//
//	    ViewerApp.display(cmp); 


		ViewerApp.display(ilsf.getIndexedLineSet());
	}

}
