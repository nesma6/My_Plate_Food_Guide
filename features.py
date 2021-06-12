import cv2
import numpy as np

def Get_Color_Features(img):
	'''
	Computes the color feature vector of the image
	based on HSV histogram
    input : image contains the colored food
    output : color feature vector
	'''
	img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	h,s,v = cv2.split(img_hsv)

	h_bins = 6
	s_bins = 2
	v_bins = 2
	histSize = [h_bins, s_bins, v_bins]

	h_ranges = [0, 180]
	s_ranges = [0, 256]
	v_ranges = [0, 256]

	channels = [0, 1, 2]

	ranges = []
	for i in range(len(h_ranges)):
		ranges.append(h_ranges[i])
	for i in range(len(s_ranges)):
		ranges.append(s_ranges[i])
	for i in range(len(v_ranges)):
		ranges.append(v_ranges[i])

	hist = cv2.calcHist([img_hsv], channels , None, histSize, ranges)
	new_hist = hist.reshape(1,24)
	new_hist = new_hist[0]
	#remove the background feature
	feature = new_hist[1:]
	
	return feature


def Get_Shape_Features(img):
	'''
	The shape features of an image are calculated
	based on the contour of the food item using Hu moments.
    input : binary image of the food
    output : shape feature vector
	'''
	contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	moments = cv2.moments(contours[0])
	hu = cv2.HuMoments(moments)
	feature = []
	for i in hu:
		feature.append(i[0])	
	return feature

def Get_texture_features(img):
    '''
	The texture features of an image are calculated
	using gabor filter
    input : colored image of the food
    output : texture feature vector
	'''
    img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ksize=31  
    phi = 0  
    sigma = 5
    num = 1  #To count numbers up in order to give Gabor features a lable in the data frame
    kernels = []  #Create empty list to hold all kernels that we will generate in a loop
    feature = []
    for theta in np.arange(0, np.pi, np.pi / 8):   
        for lamda in [8.0, 13.0]:   #Range of wavelengths
            for gamma in [0.8, 2.0]:   #Gamma values of 0.8 and 2.0
                kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lamda, gamma, phi, ktype=cv2.CV_32F)    
                kernels.append(kernel)
                fimg = cv2.filter2D(img1, cv2.CV_8UC3, kernel)
                
                mean, dev = cv2.meanStdDev(fimg)
                a, b =  mean[0][0], dev[0][0]
                feature.append(a)
                feature.append(b)
               
    return feature


