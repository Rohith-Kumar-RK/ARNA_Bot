import tensorflow as tf
from pathlib import Path

import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
# import osg
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
  BASE_DIR = Path(__file__).resolve().parent

  MODEL_DIR = BASE_DIR / "Models"

  DISEASE_MODEL_PATH = MODEL_DIR / "best_model.keras"
  IDENTIFY_MODEL_PATH = MODEL_DIR / "identify_CNN.keras"


  # Load once globally
  disease_model = tf.keras.models.load_model(
      DISEASE_MODEL_PATH
  )

  identify_model = tf.keras.models.load_model(
      IDENTIFY_MODEL_PATH
  )
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