import wx
import os
from pprint import pprint as pp
from include.Base import Base


class FileCtrl(wx.FileCtrl, Base):
		 
	def __init__(self, **kwargs):
		Base.__init__(self) 
		if 1:
			defaultDirectory = kwargs.get('defaultDirectory', '')		
			defaultFilename  = kwargs.get('defaultFilename', '')
			wildCard = kwargs.get('wildCard', "Image files (*.jpg)|*.jpg") 
			parent 	 = kwargs.get('parent')
			style	 = kwargs.get('style', wx.FC_DEFAULT_STYLE)
			pos 	 = kwargs.get('pos', wx.DefaultPosition)
			size	 = kwargs.get('size', wx.DefaultSize)
			id 		 = kwargs.get('id', wx.ID_ANY)
			name	 = kwargs.get('name', "filectrl")
				 
		print('8'*50,defaultDirectory)

		
		wx.FileCtrl.__init__(self, parent, id, defaultDirectory, defaultFilename,
							 wildCard, style, pos, size, name)

		

		self.Bind(wx.EVT_FILECTRL_FILEACTIVATED, self.OnFileActivated)
		self.Bind(wx.EVT_FILECTRL_SELECTIONCHANGED, self.OnSelectionChanged)
		self.Bind(wx.EVT_FILECTRL_FOLDERCHANGED, self.OnFolderChanged)
		self.Bind(wx.EVT_FILECTRL_FILTERCHANGED, self.OnFilterChanged)
		self.Bind(wx.EVT_LEFT_DOWN, self.OnMouse)
		self.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)

	def onKeyPress(self, event):
		keycode = event.GetKeyCode()
		print (keycode)
		if keycode == wx.WXK_SPACE:
			print ("you pressed the spacebar!")
		event.Skip()		
	def OnMouse(self, evt):
		self.last_was_mouse = True
		print('OnMouse')
		evt.Skip()


	def OnFileActivated(self, event):
		import os
		fn=self.GetFilename()
		dn=self.Directory
		print('File Activated: %s\n' % os.path.join(dn, fn))
		self.send('setFile', os.path.join(dn, fn))

		

	def OnSelectionChanged(self, event):
		print('Selection Changed: %s\n' % self.GetPath())
		ms = wx.MouseState()
		#pp(dir(ms))
		#print(ms.x, ms.y)
		print(self.GetPositionTuple())
		

	def OnFolderChanged(self, event):
		print('Directory Changed: %s\n' % self.GetDirectory())

	def OnFilterChanged(self, event):
		print('Filter Changed: %s\n' % self.GetFilterIndex())

	def on_open_folder(self, event):
		title = "Choose a directory:"
		dlg = wx.DirDialog(self, title, style=wx.DD_DEFAULT_STYLE)
		if dlg.ShowModal() == wx.ID_OK:
			self.panel.update_mp3_listing(dlg.GetPath())
		dlg.Destroy()

#---------------------------------------------------------------------------


class FileCtrlPanel(wx.Panel):
	def __init__(self,  **kwargs):
		wx.Panel.__init__(self, kwargs['parent'])
		self.pref= kwargs['pref']
		kwargs['parent']=self
		fc = FileCtrl(**kwargs)
		fc.SetSize((350,650))
		fc.BackgroundColour = 'sky blue'
