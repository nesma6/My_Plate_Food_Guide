import numpy as np
import cv2
from Feature_Extraction import *
from Calories import *


foods = {
	1 : "Apple",
	2 : "Banana",
	3 : "Bean", 
	4 : "Carrot",
	5 : "Cheese",
	6 : "Orange",
	7 : "Onion",
	8 : "Pasta",
	9 : "Tomato",
	10: "Cucumber",
	11: "Souce",
	12: "Kiwi",
	13: "Pepper",
	14: "Watermelon"
}

def training():
    '''
    using the SVM model and the features of the input images, a ML model is created and saved in a file 
    so that it's easily later to classify an image using this model
    '''
    feature_mat = []
    response = []
    for j in [1,2,3,4,5,6,7,8,9,10,11,12,13,14]:
        for i in range(1,21):
            print ("images/All_Images/"+str(j)+"_"+str(i)+".jpg")
            feature, food_area, finger_area, fruit_contour, pix_to_cm_factor = Get_image_Features("images/All_Images/"+str(j)+"_"+str(i)+".jpg")
            feature_mat.append(feature)
            response.append(j)

    trainData = np.float32(feature_mat).reshape(-1,94)
    responses = np.array(response)
    svm = cv2.ml.SVM_create()
    svm.setType(cv2.ml.SVM_C_SVC)
    svm.setKernel(cv2.ml.SVM_LINEAR)
    svm.setTermCriteria((cv2.TERM_CRITERIA_MAX_ITER, 100, 1e-6))
    svm.train(trainData, cv2.ml.ROW_SAMPLE, responses)
    svm.save('svm_data.dat')


def classify_image(img_path):
    '''
    clssify the input image to one of the classes from 1 to 14 based on the features of the image
    input : image path 
    output : image class , food area , finger area , fruit contour and pixels to cm factor
    '''
    svm = cv2.ml.SVM_create()
    svm = cv2.ml.SVM_load('svm_data.dat')
    feature, food_area, finger_area, fruit_contour, pix_to_cm_factor = Get_image_Features(img_path)
    feature_mat = feature
    testData = np.float32(feature_mat).reshape(-1,94)
    result_prediction = svm.predict(testData)
    result_pre = result_prediction[1].tolist()
    label = int(result_pre[0][0])
    return label, food_area, finger_area, fruit_contour, pix_to_cm_factor

def get_food_Name(label):
    '''
	based on the class image return the name of the food
    input : image class
    output : name of the food
	'''
    return foods[label]



