from src.ui_telegram import create_app
def test_model_loading():
    app = create_app()

    assert app is not None 