import re
import telepot
import requests
import pornhub
from flask import Flask, request
print(dir(pornhub))
try:
    from Queue import Queue
except ImportError:
    from queue import Queue
TOKEN = "885925187:AAH9GMyKo6EICdqKc5hzHqzXj2Qxyj_PPMQ"
search_keywords = []
total = []
app = Flask(__name__)
update_queue = Queue()
bot = telepot.Bot(TOKEN)
def on_chat_message(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	print(msg)
	if content_type == "text":
		text = msg["text"].lower()
		if text.startswith("/start"):
			requests.post("https://api.telegram.org/bot885925187:AAH9GMyKo6EICdqKc5hzHqzXj2Qxyj_PPMQ/sendMessage?chat_id="+str(chat_id)+"&text=Buongiorno "+ msg["from"]["first_name"]+", ti auguro di gustarti un buon caffè gratis. 🤙")
		elif text.startswith("/ping"):
			requests.post("https://api.telegram.org/bot885925187:AAH9GMyKo6EICdqKc5hzHqzXj2Qxyj_PPMQ/sendMessage?chat_id="+str(chat_id)+"&text=Pong.")
		elif text.startswith("/ph/"):
			cat = text[4:]
			search_keywords.append(cat)
			client = pornhub.PornHub(search_keywords)
			for video in client.getVideos(10,page=4):
				total.append(video)
			for i in total:
				requests.get("https://api.telegram.org/bot885925187:AAH9GMyKo6EICdqKc5hzHqzXj2Qxyj_PPMQ/sendPhoto",verify = True, data = {"chat_id" : chat_id, "photo" : i["background"], "caption":"""Title:{0}
				Url: {1}
				Duration: {2}
				Rating: {3}""".format(i["name"], i["url"], i["duration"], i["rating"]), "reply_to_message_id" : msg["message_id"]})
bot.message_loop({'chat': on_chat_message}, source=update_queue)
@app.route('/', methods=['GET', 'POST'])
def pass_update():
	update_queue.put(request.data)
	return 'OK [200] HTTP CODE!!'


if __name__ == '__main__':
	app.run(port=8080)
