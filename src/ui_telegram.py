import asyncio
import nest_asyncio
from src.disease_identification import predict_disease
from src.fertilizer_recomendation import recommend_fertilizer
from src.LLM import gemini_response
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os

nest_asyncio.apply()

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(" Welcome to ARNA Bot! Send text for AI assistance or an image for disease prediction.")
async def handle_text(update: Update, context: CallbackContext):
    user_input = update.message.text
    response = gemini_response(user_input)
    await update.message.reply_text(response)
async def handle_image(update: Update, context: CallbackContext):
    photo = await update.message.photo[-1].get_file()
    photo_path = "input.jpg"


    with open(photo_path, "wb") as f:
        f.write(await photo.download_as_bytearray())

    # Predict disease
    predicted_disease = predict_disease(photo_path)


    # Recommend fertilizer
    recommended_fertilizer = recommend_fertilizer(predicted_disease)
    if predicted_disease=="invalid":
      response_text= "Uploaded image is not a Potato Leaf image. So, Please Upload Potato Leaf image"
    else:
      response_text = f"🌾 Disease Detected: {predicted_disease} \n🧴 Recommended Fertilizer: {recommended_fertilizer}"
    await update.message.reply_text(response_text)
def create_app():

    BOT_TOKEN = os.getenv("BOT_TOKEN")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))

    return app
def main():
    app = create_app()
    app.run_polling()
    print("Bot is running...")

# Run the bot in the background
