import cv2
import numpy as np
import matplotlib.pyplot as plt


def Get_biggest_contour(img1,thresh_img , contours):
	'''
	find contours sort and find the biggest contour
	inputs: image and contrours 
	output: the biggest contour which corresponds to the plate
	'''
	cv2.drawContours(thresh_img, contours, -1, (0, 255, 0), 3)
	all_areas =[]   #contains area of all contours
	contours_list  = []
	for i in range(len(contours)):
		area= cv2.contourArea(contours[i])
		all_areas.append(area)
		contours_list.append(contours[i])


	max_area_index = np.argmax(all_areas)
	largest_contour_area = contours_list[max_area_index]
	mask = np.zeros(thresh_img.shape, np.uint8)
	cv2.drawContours(mask,[largest_contour_area],-1, (255,255,255), -1)
	biggest_Contour = cv2.bitwise_and(img1,img1,mask = mask)   # we think (plate)
	return biggest_Contour

def Get_Fruit_and_Finger(biggest_Contour):
	'''
	remove the plate and only save the contours of the fruit and the finger
	'''
	hsv_img = cv2.cvtColor(biggest_Contour, cv2.COLOR_BGR2HSV)
	lower_white = np.array([0,0,100]) 
	upper_white = np.array([255,90,255])
	mask_plate = cv2.inRange(hsv_img, lower_white, upper_white)
	mask_not_plate = cv2.bitwise_not(mask_plate)
	fruit_and_finger = cv2.bitwise_and(biggest_Contour,biggest_Contour,mask = mask_not_plate)
	return fruit_and_finger

def Get_Fruit(img1 ,fruit):
	'''
	remove finger pixels from the image to get the image with only the fruit
	'''
	fruit_gray = cv2.cvtColor(fruit, cv2.COLOR_BGR2GRAY)
    #plt.hist(fruit_gray.ravel(),256,[0,256]);  #to find the place of fruit
    #from histogarm we found that the fruit place in range(10,255)
	place_of_fruit_in_hist = 10
	fruit_black_and_white = cv2.inRange(fruit_gray,place_of_fruit_in_hist, 255) #black and white of fruit to apply morphological operations

	#erode
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
	erode_fruit = cv2.erode(fruit_black_and_white,kernel,iterations = 1)

	thresh_img2 = cv2.adaptiveThreshold(erode_fruit,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
	contours2, hierarchy = cv2.findContours(thresh_img2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	#cv2.drawContours(thresh_img2, contours2, -1, (0, 255, 0), 3)
	all_areas2 =[]   #contains area of all contours
	contours_list2  = []
	for i in range(len(contours2)):
		area= cv2.contourArea(contours2[i])
		all_areas2.append(area)
		contours_list2.append(contours2[i])

	max_area_index2 = np.argmax(all_areas2)
	contours_list2  = np.delete(contours_list2,max_area_index2)
	all_areas2      = np.delete(all_areas2,max_area_index2)
	max_area_index2 = np.argmax(all_areas2)
	largest_contour_area2 = contours_list2[max_area_index2]
	mask_fruit = np.zeros(fruit_black_and_white.shape, np.uint8)
	cv2.drawContours(mask_fruit,[largest_contour_area2],0, (255,255,255), -1)

	#dilate now
	kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(13,13))
	Binary_image_fruit = cv2.dilate(mask_fruit,kernel2,iterations = 1)

	Colored_fruit_image = cv2.bitwise_and(img1,img1,mask = Binary_image_fruit)
	return Colored_fruit_image , Binary_image_fruit

def Get_Fruit_Area(Binary_image_fruit):
	'''
	find the area of the food
	'''
	img_th = cv2.adaptiveThreshold(Binary_image_fruit,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
	contours3, hierarchy = cv2.findContours(img_th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	all_areas3 =[]   #contains area of all contours
	contours_list3  = []
	for i in range(len(contours3)):
		area= cv2.contourArea(contours3[i])
		all_areas3.append(area)
		contours_list3.append(contours3[i])
	max_area_index3 = np.argmax(all_areas3)
	contours_list3  = np.delete(contours_list3,max_area_index3)
	all_areas3      = np.delete(all_areas3,max_area_index3)
	max_area_index3 = np.argmax(all_areas3)
	fruit_contour = contours_list3[max_area_index3]
	fruit_area = cv2.contourArea(fruit_contour)
	return fruit_area , fruit_contour

def Get_finger(mask_finger, Binary_image_fruit):
	'''
	find the area of the finger
	'''
	skin2 =abs(mask_finger - Binary_image_fruit)    #el soba3 bntra7 el soba3 na2s el tofa7a fbytl3 el goz2 bta3 el soba3
	#erode before finding contours
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
	skin_eroded = cv2.erode(skin2,kernel,iterations = 1)
	img_th = cv2.adaptiveThreshold(skin_eroded,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
	contours4, hierarchy = cv2.findContours(img_th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	mask_finger_new = np.zeros(mask_finger.shape, np.uint8)
	all_areas4 =[]   #contains area of all contours
	contours_list4  = []
	for i in range(len(contours4)):
		area= cv2.contourArea(contours4[i])
		all_areas4.append(area)
		contours_list4.append(contours4[i])
	max_area_index4 = np.argmax(all_areas4)
	contours_list4  = np.delete(contours_list4,max_area_index4)
	all_areas4      = np.delete(all_areas4,max_area_index4)
	max_area_index4 = np.argmax(all_areas4)
	largest_area_2 = contours_list4[max_area_index4]
	cv2.drawContours(mask_finger_new, [largest_area_2], 0, (255,255,255), -1)
	return largest_area_2
	
def Get_Food_Area(img1):
	'''
	Estimate the area of the fruit, it returns its binary image , color image, area of the finger,
	fruit contour, pix_to_cm_ratio of the contour
	'''

	#convert the image to gray scale and remove the noise then convert to black and white image
	img_grey = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
	img_filt = cv2.medianBlur(img_grey, 5)
	thresh_img = cv2.adaptiveThreshold(img_filt,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
	contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

	#the biggest contour corresponds to the plate and fruit.
	biggest_Contour = Get_biggest_contour(img1 ,thresh_img , contours)

	#now we want to remove the plate and only save the contours of the fruit and the finger
	fruit_and_finger = Get_Fruit_and_Finger(biggest_Contour)

	# now convert to hsv to remove finger pixels from the image to get the image with only the fruit
	hsv_img = cv2.cvtColor(fruit_and_finger, cv2.COLOR_BGR2HSV)
	lower_finger = np.array([0,10,60]) 
	upper_finger = np.array([10,160,255])
	mask_finger = cv2.inRange(hsv_img, lower_finger,upper_finger) 
	not_finger = cv2.bitwise_not(mask_finger); #invert skin and black
	fruit = cv2.bitwise_and(fruit_and_finger,fruit_and_finger,mask = not_finger)

	Colored_fruit_image , Binary_image_fruit = Get_Fruit(img1, fruit)

	#find area of fruit
	fruit_area , fruit_contour = Get_Fruit_Area(Binary_image_fruit)


	#finding the area of finger. find area of biggest contour from image that only contains the finger
	largest_area_2 = Get_finger(mask_finger, Binary_image_fruit)

	finger_rect = cv2.minAreaRect(largest_area_2)
	box = cv2.boxPoints(finger_rect)
	box = np.int0(box)
	mask_finger_2 = np.zeros(mask_finger.shape, np.uint8)
	cv2.drawContours(mask_finger_2,[box],0,(255,255,255), -1)

	pix_height = max(finger_rect[1])
	pix_to_cm_multiplier = 5.0/pix_height
	finger_area = cv2.contourArea(box)


	return fruit_area, Binary_image_fruit, Colored_fruit_image, finger_area, fruit_contour, pix_to_cm_multiplier


