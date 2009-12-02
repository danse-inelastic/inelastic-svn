/*
  Automatically Converted from Java Source 
  
  by java2groovy v0.0.1   Copyright Jeremy Rayner 2007
  
  !! NOT FIT FOR ANY PURPOSE !! 
  'java2groovy' cannot be used to convert one working program into another  */

package cod

import java.awt.BorderLayout
import java.awt.Font
import java.awt.event.ActionEvent
import java.awt.event.WindowEvent
import java.io.File
import java.io.FileReader
import java.io.FileWriter
import java.io.IOException
import java.io.Serializable

import javax.swing.AbstractAction
import javax.swing.Action
import javax.swing.BorderFactory
import javax.swing.JDialog
import javax.swing.JFileChooser
import javax.swing.JMenu
import javax.swing.JMenuBar
import javax.swing.JPanel
import javax.swing.JScrollPane
import javax.swing.JTextArea
import javax.swing.WindowConstants

class Nutpad extends JDialog implements Serializable 
    {private static final long serialVersionUID = 7039308358105899711L

    JTextArea mEditArea
    private JFileChooser mFileChooser = new JFileChooser(".")

    private Action mOpenAction
    private Action mSaveAction
    private Action mExitAction

    private File file = null

    NutpadNutpad(File loadedFile) {
        super()
        file = loadedFile
        createActions()
        this.setContentPane(new contentPanel(loadedFile))
        this.setJMenuBar(createMenuBar())


        this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE)
        this.pack()
}











    NutpadNutpad(String contents) {
        super()
        createActions()
        this.setContentPane(new contentPanel(contents))
        this.setJMenuBar(createMenuBar())


        this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE)
        this.pack()
}










    private class contentPanel extends JPanel 
        {private static final long serialVersionUID = -6324322656704584756L

        contentPanelcontentPanel(File file) {
            initialize()

            try {
                FileReader reader = new FileReader(file)
                mEditArea.read(reader, """")
}


             catch (IOException ioex) {
                System.out.println(ioex)
}
}










        contentPanelcontentPanel(String contents) {
            initialize()
            mEditArea.setText(contents)
}




        private void initialize() {
            mEditArea = new JTextArea(50, 80)
            mEditArea.setBorder(BorderFactory.createEmptyBorder(2, 2, 2, 2))
            mEditArea.setFont(new Font("monospaced", Font.PLAIN, 14))
            JScrollPane scrollingText = new JScrollPane(mEditArea)

            this.setLayout(new BorderLayout())
            this.add(scrollingText, BorderLayout.CENTER)
}
}private JMenuBar createMenuBar() {
        JMenuBar menuBar = new JMenuBar()
        JMenu fileMenu = menuBar.add(new JMenu("File"))
        fileMenu.add(mOpenAction)
        fileMenu.add(mSaveAction)
        fileMenu.addSeparator()
        fileMenu.add(mExitAction)
        return menuBar
}










    private void createActions() {
        mOpenAction = new AbstractAction("Open..."
            {private static final long serialVersionUID = -1493840220632136728L

            void actionPerformed(ActionEvent e) {
                int retval = mFileChooser.showOpenDialog(Nutpad.this)
                if (retval == JFileChooser.APPROVE_OPTION) {
                    File f = mFileChooser.getSelectedFile()
                    try {
                        FileReader reader = new FileReader(f)
                        mEditArea.read(reader, """")
}


                     catch (IOException ioex) {
                        System.out.println(e)
}
}
}
})




















        mSaveAction = new AbstractAction("Save"
            {private static final long serialVersionUID = -3294324834199401502L

            void actionPerformed(ActionEvent e) {
                if (true) {
                    if (file == null) {
                        int retval = mFileChooser.showSaveDialog(Nutpad.this)
                        if (retval == JFileChooser.APPROVE_OPTION) {
                            File f = mFileChooser.getSelectedFile()
                            try {
                                FileWriter writer = new FileWriter(f)
                                mEditArea.write(writer)
}



                             catch (IOException ioex) {
                                System.out.println(e)
}
}
} else {
                        try {
                            FileWriter fw = new FileWriter(file)
                            fw.write(mEditArea.getText())
                            fw.close()
}



                         catch (IOException e1) {
                            e1.printStackTrace()
}
}
} else {}
}
})



































        mExitAction = new AbstractAction("Exit"
            {private static final long serialVersionUID = -6823728690923785461L

            void actionPerformed(ActionEvent e) {
                cancel()
}
})
}






































































    @Override 
    protected void
 
    processWindowEvent(WindowEvent e) {
        if (e.getID() == WindowEvent.WINDOW_CLOSING) {
            cancel()
}


        super.processWindowEvent(e)
}






    void cancel() {
        dispose()

        System.gc()
}
}
