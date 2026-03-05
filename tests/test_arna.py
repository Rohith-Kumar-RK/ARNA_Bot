from src.ui_telegram import main
import threading


def test_model_loading():
    threading.Thread(target=main).start()
    assert main() 