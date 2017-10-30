from cv2 import * # initialize the camera
from Tkinter import *
import numpy as np
import cv2
from matplotlib import pyplot as plt

master = Tk() #just create the window using Tk- (tk is a object of tkinter package)

master.minsize(width=300, height=300) # setup the window size

#function called on button click (show)
def opencam():
   cam = VideoCapture(0)   # 0 -> index of camera
   s, img = cam.read()
   if s:    # frame captured without any errors
        namedWindow("cam-test",CV_WINDOW_AUTOSIZE)
        imshow("cam-test",img)
        waitKey(0)
        destroyWindow("cam-test")
        imwrite("filename.jpg",img) #save image
	
#def checkangle():
	im = cv2.imread("filename.jpg");
	#imm = cv2.imread("filename.jpg",0);
	size = im.shape
	print size;
	height, width = im.shape[:2]
	print width;
	print height;

	#ball = im[280:340, 330:390]
	#im[273:333, 100:160] = ball

	#2D image points. If you change the image, you need to change vector

	image_points = np.array([   (213, 85),     
		                    (590, 80),     
		                    (245, 93),     
		                    (213, 81),     
		                    (200, 95),     
		                    (253, 94)  
		                ], dtype="double")
	 # 3D model points.

	model_points = np.array([   (0.1, 0.1, 0.1),             
		                    (0.0, -330.0, -65.0),       
		                    (-225.0, 170.0, -135.0),     
		                    (225.0, 170.0, -135.0),     
		                    (-150.0, -150.0, -125.0),    
		                    (150.0, -150.0, -125.0)     
		                 
		                ])
	 
	# initialize the HOG descriptor/person detector
	hog = cv2.HOGDescriptor()
	hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

	# detect people in the image
	(rects, weights) = hog.detectMultiScale(im, winStride=(4, 4),padding=(8, 8), scale=1.05)

	print rects
	print weights
	# Camera internals
	
	focal_length = size[1]
	center = (size[1]/2, size[0]/2)
	camera_matrix = np.array(
		                 [[focal_length, 0, center[0]],
		                 [0, focal_length, center[1]],
		                 [0, 0, 1]], dtype = "double"
		                 )
	 
	print "Camera Matrix :\n {0}".format(camera_matrix)
	 
	dist_coeffs = np.zeros((4,1)) # Assuming no lens distortion
	(success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.CV_ITERATIVE)
	 


	(nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)
	 



	print "Rotation Vector:\n {0}".format(rotation_vector)
	print "Translation Vector:\n {0}".format(translation_vector)
	 
	p1 = ( int(image_points[0][0]), int(image_points[0][1]))
	p2 = ( int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))
	 
	cv2.line(im, p1, p2, (255,0,0), 2)
	 
	# Display image
	cv2.imshow("Output", im)
	cv2.waitKey(0)

Button(master, text='Cam', command=opencam).grid(row=3, column=0, sticky=W, pady=4)
#Button(master, text='Check Angle', command=checkangle).grid(row=3, column=1, sticky=W, pady=4) #buttons
Button(master, text='Quit', command=master.quit).grid(row=3, column=2, sticky=W, pady=4) #buttons

mainloop()


