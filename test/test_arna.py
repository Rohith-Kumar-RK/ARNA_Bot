from ui_telegram import main
import threading
threading.Thread(target=main).start()
main()