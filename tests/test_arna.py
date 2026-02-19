from src.ui_telegram import main
import threading
def test_main():
    threading.Thread(target=main).start()
    assert main() 