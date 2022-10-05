import re
import os 
import random
import telepot
import requests
from pathlib import Path
from flask import Flask, request
media_folder = Path(__file__).parent / "media"


try:
    from Queue import Queue
except ImportError:
    from queue import Queue
TOKEN = "5654192709:AAGs4M9nHZD2JFXUrur2S72Lm0_0KeLrnoU"
app = Flask(__name__)
update_queue = Queue()
bot = telepot.Bot(TOKEN)
def on_chat_message(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	print(msg)
	if content_type == "text":
		text = msg["text"].lower()
		if text.startswith("/start"):
			requests.post("https://api.telegram.org/bot885925187:AAH9GMyKo6EICdqKc5hzHqzXj2Qxyj_PPMQ/sendMessage?chat_id="+str(chat_id)+"&text=Remember "+ msg["from"]["first_name"]+", PolyML is the way. 🤙")
		elif text.startswith("/ping"):
			requests.post("https://api.telegram.org/bot885925187:AAH9GMyKo6EICdqKc5hzHqzXj2Qxyj_PPMQ/sendMessage?chat_id="+str(chat_id)+"&text=Pong.")
		if "kuper" in text:
			random_picture = random.choice(os.listdir(media_folder))
			requests.get("https://api.telegram.org/bot885925187:AAH9GMyKo6EICdqKc5hzHqzXj2Qxyj_PPMQ/sendPhoto",verify = True, data = {"chat_id" : chat_id, "photo": f"app/media/{random_picture}"), "reply_to_message_id" : msg["message_id"]})
			
bot.message_loop({'chat': on_chat_message}, source=update_queue)
@app.route('/', methods=['GET', 'POST'])
def pass_update():
	update_queue.put(request.data)
	return 'OK [200] HTTP CODE!!'


if __name__ == '__main__':
	app.run(port=8080)
