from src.ui_telegram import main
import threading
def test_arna_1():
    threading.Thread(target=main).start()
    main() 