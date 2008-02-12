import wx

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "List Boxes")
        panel = wx.Panel(self, -1)

        choices1 = ["red", "green", "blue"]
        choices2 = ["10", "20", "30"]

        self.lb1 = wx.ListBox(panel, -1, (10, 10),
                  (100, 200), choices1, wx.LB_SINGLE)
        self.lb1.Bind(wx.EVT_LISTBOX, self.on_select)


        lb2 = wx.ListBox(panel, -1, (120, 10),
                  (100, 200), choices2, wx.LB_SINGLE)
        target = MyTextTarget(lb2)  #MyTextTarget defined below
        lb2.SetDropTarget(target)

    def on_select(self, event):
        selection = self.lb1.GetSelection()

        text = self.lb1.GetStringSelection()
        text_obj = wx.TextDataObject(text)

        source = wx.DropSource(self.lb1)
        source.SetData(text_obj)

        drop_result = source.DoDragDrop(wx.Drag_DefaultMove)
        if drop_result == wx.DragMove:  #the selection was moved-not copied
            self.lb1.Delete(selection)


class MyTextTarget(wx.TextDropTarget):
    def __init__(self, target_widget):
        wx.TextDropTarget.__init__(self)
        self.target_widget = target_widget

        self.text_obj = wx.TextDataObject()
        self.SetDataObject(self.text_obj)

    def OnData(self, x, y, default):  #called automatically on drop
        self.GetData()
        text = self.text_obj.GetText()

        end_of_list = self.target_widget.GetCount()
        self.target_widget.InsertItems([text], end_of_list)

        return default


app = wx.PySimpleApp(redirect=False)

win = MyFrame()
win.Show()

app.MainLoop()