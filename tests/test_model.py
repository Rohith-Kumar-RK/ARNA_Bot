import joblib
import os
def test_model_load():
    try:
        data_path=os.path("../Backend/src/Models/Recomendation_chatbot_model.pkl").resolve()
        print(f"[DEBUG] model path: {data_path}")
        model = joblib.load("../Backend/src/Models/Recomendation_chatbot_model.pkl")
    except Exception as e:
        print("exception raised",e) 
    
    # model = joblib.load("")
    # model2 = joblib.load("../backend/src/Models/.pkl")
    # model3 = joblib.load("../backend/src/Models/Recomendation_chatbot_model.pkl")
    # model4 = joblib.load("../backend/src/Models/Recomendation_chatbot_model.pkl")

    assert model is not None