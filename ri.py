#!/usr/bin/env python
#	Tags: phoenix-port, py3-port

from six import BytesIO

import wx
import os, sys, math
from os.path import join 
import cv2, imutils
import numpy as np
from include.Base import Base
from include.FileCtrl import FileCtrlPanel
from pprint import pprint as pp

try:
	import cStringIO
except ImportError:
	import io as cStringIO
	
	
def opj(path):
	"""Convert paths to the platform-specific separator"""
	st = os.path.join(*tuple(path.split('/')))
	# HACK: on Linux, a leading / gets lost...
	if path.startswith('/'):
		st = '/' + st
	return st

#----------------------------------------------------------------------

########################################################################
class ViewerFrame(wx.Frame, Base):
	""""""

	#----------------------------------------------------------------------
	def __init__(self, title):
		Base.__init__(self) 
		wx.Frame.__init__(self, None, title="Image Viewer")
		self.pnl=pnl = ViewerPanel(self)
		self.folderPath = ""
		#pub.subscribe(self.resizeFrame, ("resize"))
		
		#self.initToolbar()
		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		cwd = os.getcwd()
		print(cwd)
		self.fc=FileCtrlPanel(parent=self, defaultDirectory= join(cwd, 'image'),pref=[])
		self.sizer.Add(self.fc,0)
		self.sizer.Add(pnl, 1, wx.EXPAND|wx.CENTER, 0,30)
		
		if 1:
			self.btn=btn = wx.Button(self, 1,'Rotate->')
			self.btn.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
			btn.Bind(wx.EVT_BUTTON, self.OnRotateF)
		if 1:
			self.btnb=btnb = wx.Button(self, 1,'<-Rotate')
			self.btnb.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
			btnb.Bind(wx.EVT_BUTTON, self.OnRotateB)
			
			self.ext=ext = wx.Button(self, 1,'Exit')
			self.ext.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
			ext.Bind(wx.EVT_BUTTON, self.OnExit)
		
		v_sizer = wx.BoxSizer(wx.VERTICAL)
		v_sizer.Add(btn)
		v_sizer.Add((-1,20))
		v_sizer.Add(btnb)
		v_sizer.Add((-1,-1),1, wx.EXPAND)
		v_sizer.Add(ext, 0, wx.EXPAND)
		self.sizer.Add(v_sizer,0, wx.EXPAND)
		self.SetSizer(self.sizer)
		#self.SetSize(pnl.getSize())
		
		self.Show()
		self.sizer.Fit(self)
		
		#self.SetSize((1000,1000))
		#self.Maximize(True)
		#self.ShowFullScreen(True)
		o_h, o_w = pnl.cvimg.shape
		_, height = wx.DisplaySize()
		self.SetSize((int(o_w*1.3), height-35))
		self.Center()
		self.sub('setFile')
	def setFile(self, message, arg2=None, **kwargs):		
		fn=message
		self.pnl.setFile(fn)
	def OnRotateF(self, evt):
		#print(132)
		self.pnl.Rotate(-15)
	def OnRotateB(self, evt):
		#print(132)
		self.pnl.Rotate(15)
		
		if 0:
			self.sizer.Clear()
			self.sizer.Add(self.pnl, 1, wx.EXPAND|wx.CENTER)
			self.sizer.Add(self.btn)
			self.SetSizerAndFit(self.sizer)
			#self.Update()	
			#self.SetSize((1000,1000))
			self.Center()
			self.Maximize(True)
			self.ShowFullScreen(True)
	def OnExit(self, evt):
		self.Close()
		evt.Skip()
		
		
		
		
class ViewerPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, -1)
		self.angle=0
		imgpath=r'C:\Users\alex_\mygit\dataworm\art.jpg'
		self.img = self.loadImage(imgpath)
		self.imgc = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(self.img))
		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer.Add(self.imgc, 1, wx.EXPAND|wx.CENTER)
		self.SetSizerAndFit(self.sizer)
	def setFile(self, fn):
		self.img = self.loadImage(fn)
		self.imgc.SetBitmap(wx.Bitmap(self.img))
	def loadImage(self,imgpath):
		data = open(opj(imgpath), "rb").read()



		stream = cStringIO.BytesIO(data)
		img= wx.Image( stream )
		if 1: #scale
			W = img.GetWidth()
			H = img.GetHeight()

		if 1:            
			self.cvimg = cv2.imdecode(np.frombuffer(data, np.uint8), 0 )
			o_h, o_w = self.cvimg.shape

		self.W, self.H = img.GetSize()
		return img


		
	def rotateImg(self, img, degree):
		self.angle +=degree
		
		ROI = self.rotate(img, self.angle)
		o_h, o_w = ROI.shape
		#print('ROI:',o_h, o_w )	
		retval, buffer = cv2.imencode('.jpg', ROI)
		img2= wx.Image(cStringIO.BytesIO(buffer.tobytes()))		
		
		return img2


	def rotate(self,image, angle, center=None, scale=1.0):
		# grab the dimensions of the image
		(h, w) = image.shape[:2]

		# if the center is None, initialize it as the center of
		# the image
		if center is None:
			center = (w // 2, h // 2)

		# perform the rotation
		M = cv2.getRotationMatrix2D(center, angle, scale)
		rotated = cv2.warpAffine(image, M, (w, h), borderValue=wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE))
		#rotated_image = cv2.warpAffine(img, M, (cols, rows), borderValue=(255,255,255))

		# return the rotated image
		return rotated

	
	def resizeRotated(self):
            
		stream.seek(0)            
		cv = cv2.imdecode(np.asarray( bytearray(stream.read() ) , dtype=np.uint8), 0 )
		o_h, o_w = cv.shape
		#print('cv2:',o_h, o_w )
		if 1:
			x,y,w,h = 0, 0, 500,500
			ROI = cv[y:y+h, x:x+w]
			o_h, o_w = ROI.shape
			#print('ROI:',o_h, o_w )					
		retval, buffer = cv2.imencode('.jpg', ROI)
		img2= wx.Image(cStringIO.BytesIO(buffer.tobytes()))
				
	def Rotate(self,degree):
		import base64
		img = self.rotateImg(self.cvimg, degree)
		#data=base64.b64encode(img.GetData())

		if 0:
			x,y,w,h = 0, 0, 500,500
			ROI = cv[y:y+h, x:x+w]
			o_h, o_w = ROI.shape
			#print('ROI:',o_h, o_w )					
			retval, buffer = cv2.imencode('.jpg', ROI)
			#print(type(buffer))
			#img2= wx.Image(cStringIO.BytesIO(buffer.tobytes()))
		
		#print(img.GetSize(), self.W, self.H)
		
		self.imgc.SetBitmap(wx.Bitmap(img))
		if 0:
			self.sizer.Clear()
			self.sizer.Add(self.imgc, 1, wx.EXPAND|wx.CENTER)
			self.SetSizerAndFit(self.sizer)
			self.Update()

	def getSize(self):
		return self.imgc.GetSize()
#----------------------------------------------------------------------



if __name__ == '__main__':
 
	app = wx.App()
	frame1 = ViewerFrame("An image on a panel")
	
	
	frame1.Show(1)
	app.MainLoop()
