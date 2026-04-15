import random
from groq import Groq
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# 🔑 KEYS
client = Groq(api_key="YOUR_GROQ_API_KEY")
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
# 🎬 START MENU
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("😂 Get Joke", callback_data="joke")]
    ]

    await update.message.reply_text(
        "👋 Welcome!\nPress the button to get a joke 😂",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# 🎯 GENERATE JOKE FUNCTION
def generate_joke():

    topics = ["animals", "school", "food", "technology", "work", "money", "sports", "europe" , "africa" , "facebook" , "cats"]
    topic = random.choice(topics)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": f"Write a very short funny joke about {topic}"
        }]
    )

    return response.choices[0].message.content

# ⚡ BUTTON HANDLER (100% SAFE FLOW)
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    # 🚨 MUST ALWAYS BE FIRST
    try:
        await query.answer()
    except:
        pass

    data = query.data

    # 😂 JOKE OR ANOTHER ONE
    if data in ["joke", "another"]:

        await query.edit_message_text("😂 Thinking of a joke...")

        try:
            joke = generate_joke()

            keyboard = [
                [InlineKeyboardButton("😂 Another one", callback_data="another")],
                [InlineKeyboardButton("🏠 Menu", callback_data="menu")]
            ]

            await query.message.reply_text(
                joke,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        except:
            await query.message.reply_text("⚠️ Failed to generate joke. Try again.")

    # 🏠 MENU
    elif data == "menu":

        keyboard = [
            [InlineKeyboardButton("😂 Get Joke", callback_data="joke")]
        ]

        await query.edit_message_text(
            "👋 Main Menu",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# 🚀 MAIN APP
def main():

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
