/*
  Automatically Converted from Java Source 
  
  by java2groovy v0.0.1   Copyright Jeremy Rayner 2007
  
  !! NOT FIT FOR ANY PURPOSE !! 
  'java2groovy' cannot be used to convert one working program into another  */

package cod

import java.awt.Dimension
import java.awt.Toolkit
import java.awt.event.KeyAdapter
import java.awt.event.KeyEvent
import java.awt.event.MouseAdapter
import java.awt.event.MouseEvent
import java.io.BufferedReader
import java.io.FileNotFoundException
import java.io.IOException
import java.io.InputStreamReader
import java.net.MalformedURLException
import java.net.URL

import javax.swing.JFrame
import javax.swing.JOptionPane
import javax.swing.JTabbedPane

class Main 
    {static JTabbedPane tabs = new JTabbedPane()

    MainMain() {


        tabs.addKeyListener(new KeyAdapter(
                {@Override 
                void
 
                keyReleased(KeyEvent e) {
                    if (e.getKeyCode() == KeyEvent.VK_DELETE) {
                        if (JOptionPane.showConfirmDialog(null, 
                                "Are you sure you want to delete this node?"
)
                             == JOptionPane.YES_OPTION
) {
                            tabs.remove(tabs.getSelectedIndex())
}
}
}
}))










        tabs.addMouseListener(new MouseAdapter(
                {@Override 
                void
 
                mouseClicked(MouseEvent e) {
                    if (e.getClickCount() == 2) {
                        addTab()
}
}
}))







        addTab()

        JFrame jFrame = new JFrame("Crystallography Search")
        jFrame.setSize(new Dimension(800, 600))
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize()
        Dimension frameSize = jFrame.getSize()
        if (frameSize.height > screenSize.height) {
            frameSize.height = screenSize.height
}


        if (frameSize.width > screenSize.width) {
            frameSize.width = screenSize.width
}


        jFrame.setLocation(screenSize.width - frameSize.width / 2, 
            screenSize.height - frameSize.height / 2
)

        jFrame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
        jFrame.add(tabs)
        jFrame.setVisible(true)
}








































    private void addTab() {
        tabs.add("""" + tabs.getTabCount() + 1, new Search())
}



    static void main(String[] args) {
        new Main()
}



    static StringBuffer getFileContents(String fileName) throws FileNotFoundException{
        StringBuffer contents = new StringBuffer()
        String newLine = System.getProperty("line.separator")
        try {
            URL url = new URL(fileName)
            BufferedReader input = new BufferedReader(new InputStreamReader(url.openConnection().getInputStream()))
            String line = null
            while (line = input.readLine() != null) {
                contents.append(line)
                contents.append(newLine)
}



            input.close()
}








         catch (MalformedURLException e) {
            e.printStackTrace()
}

         catch (FileNotFoundException fnfe) {
            throw fnfe
}

         catch (IOException e) {
            e.printStackTrace()
}


        return contents
}
}
