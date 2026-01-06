import os
import fitz  # PyMuPDF
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)

app = Flask(__name__)
dispatcher = Dispatcher(bot, None, workers=0)

def merge_pdf(update, context):
    file = update.message.document.get_file()
    input_pdf = "input.pdf"
    output_pdf = "A4_2slides.pdf"

    file.download(input_pdf)

    src = fitz.open(input_pdf)
    out = fitz.open()

    A4_WIDTH = 595
    A4_HEIGHT = 842

    for i in range(0, len(src), 2):
        page = out.new_page(width=A4_WIDTH, height=A4_HEIGHT)

        top_rect = fitz.Rect(0, 0, A4_WIDTH, A4_HEIGHT / 2)
        bottom_rect = fitz.Rect(0, A4_HEIGHT / 2, A4_WIDTH, A4_HEIGHT)

        page.show_pdf_page(top_rect, src, i)

        if i + 1 < len(src):
            page.show_pdf_page(bottom_rect, src, i + 1)

    out.save(output_pdf)

    update.message.reply_document(open(output_pdf, "rb"))

    os.remove(input_pdf)
    os.remove(output_pdf)

dispatcher.add_handler(
    MessageHandler(Filters.document.mime_type("application/pdf"), merge_pdf)
)

@app.route("/", methods=["GET"])
def index():
    return "Bot is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
