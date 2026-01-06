from telegram.ext import Updater, MessageHandler, Filters
import fitz  # PyMuPDF
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]

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

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.document.mime_type("application/pdf"), merge_pdf))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":

    main()
