# from src.ui_telegram import main
# import threading
# def test_main():
#     threading.Thread(target=main).start()
#     assert main() f
import tensorflow as tf

disease_model = tf.keras.models.load_model("Models/best_model.keras")
