import onnxruntime as ort
import numpy as np
import cv2
# import tensorflow as tf
# from tensorflow.keras.preprocessing.image import img_to_array, load_img
# import os
# from io import BytesIO
# from PIL import Image
import tensorflow as tf

# from tensorflow.keras.preprocessing.image import (
#     load_img,
#     img_to_array
# )

session = ort.InferenceSession(
    "Backend/src/Models/best_model.onnx"
)

input_name = session.get_inputs()[0].name

# Class Labels

classes = [
    "Early blight disease",
    "Late blight disease",
    "Normal"
]

# -----------------------------
# Preprocessing Function
# -----------------------------
def preprocess_image(image_bytes):

    # Convert bytes -> numpy array
    np_arr = np.frombuffer(
        image_bytes,
        np.uint8
    )

    # Decode image
    image = cv2.imdecode(
        np_arr,
        cv2.IMREAD_COLOR
    )

    if image is None:
        raise ValueError(
            "Invalid image data"
        )

    # BGR -> RGB
    image = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    # Resize
    image = cv2.resize(
        image,
        (300, 300)
    )

    # float32
    image = image.astype(np.float32)

    # Batch dimension
    image = np.expand_dims(
        image,
        axis=0
    )

    # EfficientNet preprocessing
    image = image.astype("float32")
    image = image / 127.5 - 1

    return image
# -----------------------------
# Inference Function
# -----------------------------
def predict_disease(image_bytes):

    input_image = preprocess_image(
        image_bytes
    )

    prediction = session.run(
        None,
        {
            input_name: input_image
        }
    )[0]

    predicted_class = np.argmax(
        prediction
    )

    confidence = float(
        np.max(prediction)
    )

    disease = classes[predicted_class]

    return disease, confidence