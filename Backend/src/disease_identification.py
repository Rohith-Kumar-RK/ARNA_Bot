import tensorflow as tf
# import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
import os
import io
from PIL import Image


# Load Disease Detection Model

def load_and_preprocess_image(image_bytes, target_size=(300, 300)):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    
    # Resize
    image = image.resize(target_size)
    
    # Convert to array
    img_array = img_to_array(image)
    
    # Expand dims (for model input)
    img_array = np.expand_dims(img_array, axis=0)
    
    # EfficientNet preprocessing
    img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
    
    return img_array
def predict_disease(image_path):
  try:
    if os.path.exists(r"Models/best_model.keras"):
      print("folder findout")
      disease_model = tf.keras.models.load_model("Models/best_model.keras")
    else:
      print("Keras model not found")
    if os.path.exists(r"Models/identify_CNN.keras"):
      identify_model = tf.keras.models.load_model("Models/identify_CNN.keras")
    else:
      print("keras model not found","*"*10)
  except Exception as e:
    print("model not found",e)
  img_array = load_and_preprocess_image(image_path)
  potato=identify_model.predict(img_array)
  confidence1 = float(np.max(potato)) 
  predict_potato = np.argmax(potato)
  if predict_potato==0:
    return "invalid",confidence1*100
  prediction = disease_model.predict(img_array)
  confidence = float(np.max(prediction)) 
  predicted_class = np.argmax(prediction)
  if predicted_class==0:
    return "Early blight disease" ,confidence*100
  elif predicted_class==1:
    return "Late blight disease" , confidence*100
  elif predicted_class==2:
    return "Normal" ,confidence*100