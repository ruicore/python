# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-08-10 10:10:26
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-11 09:17:08

import wx
import wxgui


def load(event):
    _file = open(filename.GetValue())
    contents.SetValue(_file.read())
    _file.close()


def save(event):
    _file = open(filename.GetValue(), 'w')
    _file.write(contents.GetValue())
    _file.close()


app = wx.App()
win = wx.Frame(None, title='Simple Editor', size=(410, 335))

bkg = wx.Panel(win)

loadButton = wx.Button(bkg, label="Open")
loadButton.Bind(wx.EVT_BUTTON,load)

saveButton = wx.Button(bkg, label="Save")
saveButton.Bind(wx.EVT_BUTTON,save)


filename = wx.TextCtrl(bkg)
contents = wx.TextCtrl(bkg, style=wx.TE_MULTILINE | wx.HSCROLL)

hbox = wx.BoxSizer()
hbox.Add(filename, proportion=1, flag=wx.EXPAND)
hbox.Add(loadButton, proportion=0, flag=wx.LEFT, border=5)
hbox.Add(saveButton, proportion=0, flag=wx.LEFT, border=5)

vbox = wx.BoxSizer(wx.VERTICAL)
vbox.Add(hbox, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
vbox.Add(contents, proportion=1, flag=wx.EXPAND |
         wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)

bkg.SetSizer(vbox)
win.Show()

app.MainLoop()
