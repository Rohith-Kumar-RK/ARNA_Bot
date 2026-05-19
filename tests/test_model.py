import joblib

def test_model_load():

    model = joblib.load("../Backend/src/Models/Recomendation_chatbot_model.pkl")
    # model2 = joblib.load("../backend/src/Models/.pkl")
    # model3 = joblib.load("../backend/src/Models/Recomendation_chatbot_model.pkl")
    # model4 = joblib.load("../backend/src/Models/Recomendation_chatbot_model.pkl")

    assert model is not None