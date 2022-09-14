#***************************** Car Damage Detection ***************************
#******************************************************************************
#*********************************** Start ************************************

#******************************* Import essentials ****************************
import os
import json

import h5py
import numpy as np
import pickle as pk
from PIL import Image


# openvino 
from openvino.runtime import Core

# keras imports
from keras.models import  load_model
from keras.preprocessing.image import img_to_array, load_img
from keras.applications.vgg19 import VGG19, preprocess_input
from keras.preprocessing import image
from keras.models import Model
from keras import backend as K
import tensorflow as tf

#************************* Prepare Image for processing ***********************

def prepare_img_224(img_path):
    img = load_img(img_path, target_size=(224, 224))
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x


# Loading  valid categories for identifying cars using VGG16
with open('static/cat_counter.pk', 'rb') as f:
    cat_counter = pk.load(f)

# shortlisting top 27 Categories that VGG16 stores for cars (Can be altered for less or more)
cat_list  = [k for k, v in cat_counter.most_common()[:27]]

global graph
graph = tf.compat.v1.get_default_graph()
# #******************************************************************************

# #******************************************************************************
# #~~~~~~~~~~~~~~~ Prapare the flat image~~~~~~~~~~~~~
# #******************************************************************************
# def prepare_flat(img_224):
#     base_model = load_model('static/vgg19.h5')
#     model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)
#     feature = model.predict(img_224)
#     flat = feature.flatten()
#     flat = np.expand_dims(flat, axis=0)
#     return flat

#******************* Loading Models, Weights and Categories Done **************

#******************************************************************************
#~~~~~~~~~~~~~~~~~~~~~~~~~ FIRST Check- CAR OR NOT~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#******************************************************************************

CLASS_INDEX_PATH = 'static/imagenet_class_index.json'

def get_predictions(preds, top=5):

    global CLASS_INDEX
    CLASS_INDEX = json.load(open(CLASS_INDEX_PATH))

    results = []
    for pred in preds:
        top_indices = pred.argsort()[-top:][::-1]
        result = [tuple(CLASS_INDEX[str(i)]) + (pred[i],) for i in top_indices]
        result.sort(key=lambda x: x[2], reverse=True)
        results.append(result)
    return results

def car_categories_check(img_224):
    first_check = load_model('static/vgg19.h5')
    print ("Validating that this is a picture of your car...")
    out = first_check.predict(img_224)
    top = get_predictions(out, top=5)
    for j in top[0]:
        if j[0:2] in cat_list:
            print ("Car Check Passed!!!")
            print ("\n")
            return True
    return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FIRST check ENDS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#******************************************************************************

#******************************************************************************
#~~~~~~~~~~~~~~~~~~~~~~~~~ SECOND CHECK - DAMAGED OR NOT~~~~~~~~~~~~~~~~~~~~~~~~
#******************************************************************************
# function for openvino model loading 
def OPvino_model_load(path):
    """ 
    Return model IR representation and it's output key
    """
    ie = Core()
    model = ie.read_model(model=path  + "/saved_model.xml", weights=path + "/saved_model.bin")
    compiled_model = ie.compile_model(model=model, device_name="CPU")
    output_key = compiled_model.output(0)
    return compiled_model, output_key


# models ' paths
second_model_path = "static/carORnot"
third_model_path = "static/FRS_vgg"
fourth_model_path = "static/MMS_vgg"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ SECOND CHECK ENDS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#*******************************************************************************
def car_damage_check(image):
    print ("Validating that damage exists...")

    second_check, second_output_key  =  OPvino_model_load(second_model_path)
    result = second_check([image])[second_output_key]

    prediction = int(result[0])
    
    if prediction == 1:
        print ("Validation complete - proceeding to location and severity determination")
        print ("\n")
        return True 
    else:
        return False
#******************************************************************************
#~~~~~~~~~~~~~~~~~~~~ THIRD CHECK - Location and Severity Assesment~~~~~~~~~~~~~
#******************************************************************************



def location_assessment(image):
    print ("Validating the damage area - Front, Rear or Side")

    third_check , third_output_key = OPvino_model_load(third_model_path)
    
    labels = ["Front","Rear","Side"]
    
    result = third_check ([image])[third_output_key]
    
    result_index = np.argmax(result)

    prediction = labels[result_index]
    
    print ("Your Car is damaged at - " + prediction)
    print ("Location assesment complete")
    print("\n")

    return prediction



def severity_assessment(image):
    print ("Validating the Severity...")
    
    fourth_check, fourth_output_key = OPvino_model_load(fourth_model_path)

    labels = ["Minor","Moderate","Severe"]
    
    result = fourth_check([image])[fourth_output_key]
    
    result_index = np.argmax(result)

    prediction = labels[result_index]
    
    
    print ("Your Car damage impact is - " + prediction)
    print ("Severity assesment complete")
    print ("\n")
    print ("Thank you for using the assesment kit from Ashar Siddiqui!!!")
    print ("More such kits in pipeline")
    return prediction
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ THIRD CHECK ENDS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#******************************************************************************


#******************************************************************************
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  ENGINE  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#******************************************************************************

# load models

def engine(car):

    img = car.image
    print(img)
    img_path = os.path.join("media",str(img))
    
    
    with graph.as_default():

        img_224 = prepare_img_224(img_path)
        # img_flat = prepare_flat(img_224)
        iscar = car_categories_check(img_224)
        

        while True:
            try:

                if iscar is False:
                    # g1_pic = "Are you sure its a car?Make sure you click a clear picture of your car and resubmit"
                    # g2_pic = 'N/A'
                    # g3='N/A'
                    # g4='N/A'
                    # ns='N/A'
                    car.iscar = False
                    car.isdamaged = False
                    car.location = 'N/A'
                    car.severity = 'N/A'
                    break
                else:
                    car.iscar = True
                    isdamaged = car_damage_check(img_224)

                if isdamaged is False:
                    # g2_pic = "Are you sure your car is damaged?. Make sure you click a clear picture of the damaged portion.Please resubmit the pic"
                    # g3='N/A'
                    # g4='N/A'
                    # ns='N/A'
                    car.isdamaged = False
                    car.location = 'N/A'
                    car.severity = 'N/A'
                    break
                else:
                    car.isdamaged = True     
                    car.location = location_assessment(img_224)
                    car.severity =severity_assessment(img_224)
                    # ns='a). Create a report and send to Vendor \n b). Proceed to cost estimation \n c). Estimate TAT'
                    break

            except:
                break
        
        # suppression de l'image après traitement
        # src= 'media/'
    
        # for image_file_name in os.listdir(src):
        #     os.remove(src + image_file_name)

        # K.clear_session()

        return car


    

    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ENGINE ENDS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#******************************************************************************

