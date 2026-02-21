from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from telegram import Update

# =========================
# YOUR DETAILS
# =========================

TOKEN = "8298919629:AAHA2kT14ukNYoROHrlXkXXH-qiP514Z4W4"
OWNER_ID = 821747442  # your user id


# =========================
# START COMMAND
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 Welcome To CSEC ASTU PODCAST BOT!\n\n"
         "Got a burning question for our next guest?🔥\n"
    "Send it here and your question will be answered on the podcast! 🎙️"
    )


# =========================
# USER SENDS QUESTION
# =========================

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    question = update.message.text

    # forward to you
    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=f"📩 Question from {user.id}:\n\n{question}"
    )

    # confirm to user
    await update.message.reply_text(
         "✅ Awesome! Your question is safely in our collection box 📬\n"
    "Stay Tuned!It will be answered on the podcast! 🎧"
    )


# =========================
# YOU REPLY
# =========================

async def handle_owner_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.reply_to_message:

        replied_text = update.message.reply_to_message.text

        if "Question from" in replied_text:

            user_id = int(replied_text.split()[2].replace(":", ""))

            await context.bot.send_message(
                chat_id=user_id,
                text=f"💬 Answer:\n\n{update.message.text}"
            )


# =========================
# MAIN
# =========================

def main():

    app = ApplicationBuilder().token(TOKEN).build()

    # start command
    app.add_handler(CommandHandler("start", start))

    # user questions (ignore commands)
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND & ~filters.User(OWNER_ID),
            handle_user_message
        )
    )

    # your replies
    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.User(OWNER_ID),
            handle_owner_reply
        )
    )

    print("✅ Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
