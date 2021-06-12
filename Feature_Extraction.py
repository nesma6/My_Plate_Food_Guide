from features import Get_Color_Features , Get_Shape_Features ,Get_texture_features
from img_segmentation import *

def Get_image_Features(filename):
	'''
	creates the feature vector using color , texture, shape features
	input is : the path of the image
	outputs are : feature vector , area of food item , area of the finger , frout contour and pixels to cm ratio
	'''
	img = cv2.imread(filename)
	feature = []
	Fruit_area, Binary_Image, Coloured_image, Finger_area, Fruit_contour, pix_to_cm_ratio = Get_Food_Area(img)  
	color = Get_Color_Features(Coloured_image)
	color = Feature_Normalization(color)
	texture = Get_texture_features(Coloured_image)
	texture = Feature_Normalization(texture)
	shape = Get_Shape_Features(Binary_Image)
	shape = Feature_Normalization(shape)
	for i in color:
		feature.append(i)
	for i in texture:
		feature.append(i)
	for i in shape:
		feature.append(i)

	feature = Feature_Normalization(feature)
	return feature, Fruit_area, Finger_area, Fruit_contour, pix_to_cm_ratio

def Feature_Normalization(feature):
    '''
    Normalizes the feature vector 
    input is : feature vector
    output : normalized feature vector
    '''
    mean=np.mean(feature)
    dev=np.std(feature)
    feature = (feature - mean)/dev
    return feature

