import wx
import numpy as np
import cv2
import glob
import math
import os
import wx.lib.filebrowsebutton

ix,iy,jx,jy=-1,-1,-1,-1
list=[]
def mouseclick1(event,x,y,flags,param):
    global ix,iy,jx,jy
    global list
    if event == cv2.EVENT_LBUTTONDBLCLK:
        list.append([x,y])
  
class Mywin(wx.Frame): 
   dist=0

   def OnRadiogroup(self, e): 
       global dist
       dist=float(self.t2.GetValue()) 
       rb = e.GetEventObject()
       unit = rb.GetLabel()
       if unit=='mm':
          dist=dist
       if unit=='cm':
          dist=dist*10
       if unit=='m':
          dist=dist*1000
		
   def OnTimeToClose(self, evt):
        """Event handler for the exit button click."""
	exit()
       

   def OnGoButton(self, evt):
        """Event handler for the continue button click."""
	global dist
        # termination criteria
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

	# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)

	pattern_size = (7,5)
	objp = np.zeros( (np.prod(pattern_size), 3), np.float32 )
	objp[:,:2] = np.indices(pattern_size).T.reshape(-1, 2)

	# Arrays to store object points and image points from all the images.
	objpoints = [] # 3d point in real world space
	imgpoints = [] # 2d points in image plane.

	images = glob.glob('sample*.jpg')
	for fname in images:
    		img = cv2.imread(fname)
    		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	
    		# Find the chess board corners
    		ret, corners = cv2.findChessboardCorners(gray, (7,5),None)
    		h, w = img.shape[:2]
    		# If found, add object points, image points (after refining them)
    		if ret == True:
    	  	     objpoints.append(objp)
    	             corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
    	    	     imgpoints.append(corners2)
      
	rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, (w, h), None, None)
	
	fx,fy=camera_matrix[0][0],camera_matrix[1][1]
	fxy=(fx+fy)/2
	f=3.6
	m=fxy/f
	
	path=self.fbb.GetValue()
	img = cv2.imread(path)
	cv2.imshow('image',img)
	cv2.setMouseCallback('image',mouseclick1)
	
	while(1):
	    k = cv2.waitKey(20) & 0xFF 
	    if k==27:
	        break
	    if k == ord('a'):
		ix,iy=list[0][0],list[0][1]
		jx,jy=list[1][0],list[1][1]
		d=math.sqrt(math.pow((jx-ix),2)+math.pow((jy-iy),2))
		mid=(((ix+jx)/2),((iy+jy)/2)-10)
		h1, w1 = img.shape[:2]
		x=(w1*m)/w
		sizeimgsen=d/x
		realsize=(dist*sizeimgsen)/(f)
		strval=str(realsize)
		img1 = cv2.line(img,(ix,iy),(jx,jy),(0,0,255),3)
		font = cv2.FONT_HERSHEY_SIMPLEX
        	cv2.putText(img1,strval,mid, font, .5, (0,255,0), 2, cv2.LINE_AA)
		cv2.imshow('image',img1)
		del list[:]
	

	cv2.waitKey(0)
	cv2.destroyAllWindows()
        
   

   def __init__(self, parent, title):
      wx.Frame.__init__(self, parent, -1, title,pos=(150, 150), size=(1000, 500))
	
      panel = wx.Panel(self) 
      vbox = wx.BoxSizer(wx.VERTICAL) 
         
      hbox1 = wx.BoxSizer(wx.HORIZONTAL) 
      
    
      self.fbb = wx.lib.filebrowsebutton.FileBrowseButton(panel,labelText="Select a jpg file:", fileMask="*.jpg")	
      
     
      hbox1.Add(self.fbb, 1, wx.ALIGN_LEFT)
     
      vbox.Add(hbox1) 
		
      hbox2 = wx.BoxSizer(wx.HORIZONTAL) 
      l2 = wx.StaticText(panel, -1, "Enter the distance from object to camera:") 
		
      hbox2.Add(l2, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
      self.t2 = wx.TextCtrl(panel) 
		
      hbox2.Add(self.t2,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
      self.t2.Bind(wx.EVT_TEXT,None) 
      vbox.Add(hbox2)
      hbox5 = wx.BoxSizer(wx.HORIZONTAL)

      #three RadioButtons, grouped by specifying wx.RB_GROUP style are placed on the panel
      self.rb1 = wx.RadioButton(panel,11, label = 'mm',style = wx.RB_GROUP) 
      self.rb2 = wx.RadioButton(panel,22, label = 'cm') 
      self.rb3 = wx.RadioButton(panel,33, label = 'm')      

      hbox5.Add(self.rb1,1)
      hbox5.Add(self.rb2,1)
      hbox5.Add(self.rb3,1)

      
      self.Bind(wx.EVT_RADIOBUTTON,self.OnRadiogroup) 
      vbox.Add(hbox5)
   
      hbox4 = wx.BoxSizer(wx.HORIZONTAL) 
      l3 = wx.StaticText(panel, -1, "INSTRUCTION:Select the line and press 'a'") 
      l3.SetForegroundColour((255,0,0)) # set text color	
      hbox4.Add(l3, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
      vbox.Add(hbox4)

      hbox3 = wx.BoxSizer(wx.HORIZONTAL)
      exitbtn = wx.Button(panel, -1, "Exit",pos=(20,120))
      hbox3.Add(exitbtn,1)
      gobtn = wx.Button(panel, -1, "Continue",pos=(60,120))
      hbox3.Add(gobtn,1)
      vbox.Add(hbox3)

      # bind the button events to handlers
      
      self.Bind(wx.EVT_BUTTON, self.OnTimeToClose, exitbtn)
      self.Bind(wx.EVT_BUTTON, self.OnGoButton, gobtn)

      panel.SetSizer(vbox) 
        
      self.Centre() 
      self.Show() 
      self.Fit()  

app = wx.App()
Mywin(None,  'OBJECT MEASUREMENT FROM IMAGES')
app.MainLoop()
