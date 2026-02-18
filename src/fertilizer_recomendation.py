import pickle
import joblib
import json
import random
# Load Fertilizer Recommendation Model
fertilizer_model = joblib.load("../Models/Recomendation_chatbot_model.pkl")
with open('../Dataset/Fartillizer_recom.json', 'r') as f:
    intents = json.load(f)
# Load Tokenizer
with open("../Models/recomendation_vectorizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

def recommend_fertilizer(disease):
    # Tokenize the disease index or name (modify based on tokenizer format)
    if disease=="Normal":
      return "Your Crop is Healthy No Need Fertilizers"

    promt="Recommend the Fertilizer for"+disease
    tokenized_input = tokenizer.transform([promt])
    predicted_intent = fertilizer_model.predict(tokenized_input)[0]
    for intent in intents['intents']:
        if intent['tag'] == predicted_intent:
            response = random.choice(intent['responses'])
            if ':' in response:
              return response.split(':')[1].strip()
            break

    # return predicted_intent
    return response