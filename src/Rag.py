import google.generativeai as genai

# Set up Gemini AI
genai.configure(api_key="AIzaSyBcsDn9QIuBZCUgoc5KslegvSEJLftAb2M")


def gemini_response(text):
    model_id = 'tunedModels/farmerqa-m3phv20xubea'

    model = genai.GenerativeModel(model_id)

    response = model.generate_content(text)
    return response.text if response else "❌ No response from Gemini AI."