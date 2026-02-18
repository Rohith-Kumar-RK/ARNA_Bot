import tensorflow as tf
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.applications import EfficientNetB3


# Load Disease Detection Model
disease_model = tf.keras.models.load_model("Models/best_model.keras")
identify_model = tf.keras.models.load_model("Models/identify_CNN.keras")
def load_and_preprocess_image(img_path, target_size=(300, 300)):
    img = load_img(img_path, target_size=target_size)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
    return img_array
def predict_disease(image_path):

    img_array = load_and_preprocess_image(image_path)
    potato=identify_model.predict(img_array)
    predict_potato = np.argmax(potato)
    if predict_potato==0:
      return "invalid"
    prediction = disease_model.predict(img_array)

    predicted_class = np.argmax(prediction)
    if predicted_class==0:
      return "Early blight disease"
    elif predicted_class==1:
      return "Late blight disease"
    elif predicted_class==2:
      return "Normal"