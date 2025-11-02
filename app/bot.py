import os
import tempfile
from pathlib import Path
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from .transcribe import transcribe_audio
from .translate import translate_text
from .srt_util import segments_to_srt


load_dotenv()


BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TEMP_FOLDER = Path(os.environ.get('TEMP_FOLDER', '/tmp/tg_translate'))
TEMP_FOLDER.mkdir(parents=True, exist_ok=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text('שלום! שלח לי סרטון ואחזיר כתוביות מתורגמות לעברית.')


async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
msg = update.message
file_obj = msg.video or msg.document
file = await context.bot.get_file(file_obj.file_id)
path = f"{TEMP_FOLDER}/{file_obj.file_id}.mp4"
await file.download_to_drive(path)


await msg.reply_text('🎧 מתמלל את האודיו...')
wav_path = path.replace('.mp4', '.wav')
os.system(f"ffmpeg -y -i {path} -vn -acodec pcm_s16le -ar 16000 -ac 1 {wav_path}")


segments, full_text = transcribe_audio(wav_path)


await msg.reply_text('🌍 מתרגם לעברית...')
translated = translate_text(full_text)


srt_path = path.replace('.mp4', '.srt')
segments_to_srt(segments, translated, srt_path)


await msg.reply_text('✅ מוכן! שולח את הכתוביות:')
await msg.reply_document(open(srt_path, 'rb'))


for f in [path, wav_path, srt_path]:
try: os.remove(f)
except: pass


if __name__ == '__main__':
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))
app.run_polling()
