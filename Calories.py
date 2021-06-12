import cv2
import numpy as np


#density - gram / cm^3
density_dictionary = { 1:0.609, 2:0.94, 3:0.577, 4:0.641, 5:1.151, 6:0.482, 7:0.513, 8:0.641, 9:0.481, 10:0.641, 11:0.521, 12:0.881, 13:0.228, 14:0.650 }
#kcal
calorie_dictionary = { 1:52, 2:89, 3:92, 4:41, 5:360, 6:47, 7:40, 8:158, 9:18, 10:16, 11:50, 12:61, 13:31, 14:30 }
#skin of photo to real multiplier
finger_to_area_ratio = 5*2.3

def Get_Calories(label, volume): #volume in cm^3
	'''
	Inputs: the volume of the food item and the label of the food item
	The calorie content in the given volume of the food item is calculated.
	output:  the estimation of the mass of the food item, calorie of the food item and calories per 100 grams
	'''
	#calorie per 100 grams is standard
	calorie_per_100_grams = calorie_dictionary[label]
	density = density_dictionary[label]
	mass = volume*density*1.0
	total_calories = (calorie_per_100_grams/100.0)*mass
	return mass, total_calories, calorie_per_100_grams 

def Get_Volume(label, Frout_area, Finger_area, pix_to_cm_multiplier, fruit_contour):
	'''
	the volume of the food item is calculated using the callibration techniques, from the area
	and the contour of the food item,compare this area to the most fitted geometric shape
    input : class image , area of the food , area of the finger , pixel to cm factor and fruit contour
    output : the estimate volume of the food
	'''
	#area in cm^2
	area_fruit = (Frout_area/Finger_area)*finger_to_area_ratio 
	volume = 100

	#sphere-apple,tomato,orange,kiwi,onion,pepper
	if label == 1 or label == 9 or label == 7 or label == 6 or label==12 or label==13: 
		radius = np.sqrt(area_fruit/np.pi)
		volume = (4/3)*np.pi*pow(radius,3)

	#cylinder like banana, cucumber, carrot
	if label == 2 or label == 10 or (label == 4 and area_fruit > 30):
		fruit_rect = cv2.minAreaRect(fruit_contour)
		height = max(fruit_rect[1])*pix_to_cm_multiplier
		radius = area_fruit/(2.0*height)
		volume = np.pi*pow(radius,2)*height
	
	#cheese, carrot, sauce
	if (label==4 and area_fruit < 30) or (label==5) or (label==11):
		volume = area_fruit*0.5 #assuming width = 0.5 cm

	#beans , pasta , watermelon
	if label== 3 or label==8 or label==14:
		volume = area_fruit*1.5 #assuming width = 1.5 cm
	
	return volume
