from pathlib import Path
import joblib

def test_model_load():

    model_path = Path(
        "../Backend/src/Models/Recomendation_chatbot_model.pkl"
    ).resolve()

    print(f"[DEBUG] model path: {model_path}")

    try:
        model = joblib.load(model_path)

    except Exception as e:
        print("Exception raised:", e)
        model = None

    assert model is not None