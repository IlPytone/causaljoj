import re
import telepot
import requests
from flask import Flask, request
try:
    from Queue import Queue
except ImportError:
    from queue import Queue

coffe_link_mcd = "https://survey.fast-insight.com/mcd/it/voucher_coffee_aug.php"
headers = {
	"lang" : "it",
	"store_id" : "0280",
	"surveyform" : "1224",
	"identifier" : "20190429170424",
	"promo" : "OXM995T9CK4IR",
	"incentivetype" : "2",
	"orderpoint" : "1",
}
TOKEN = "885925187:AAH9GMyKo6EICdqKc5hzHqzXj2Qxyj_PPMQ"
app = Flask(__name__)
update_queue = Queue()
bot = telepot.Bot(TOKEN)
def on_chat_message(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	print(msg)
	if content_type == "text":
		text = msg["text"].lower()
		if text.startswith("/start"):
			bot.sendMessage(chat_id,"Buongiorno, ti auguro di gustarti un buon caffè gratis.")
		elif text.startswith("/ping"):
			bot.sendMessage(chat_id,"Pong.")
		elif text.startswith("/coffe"):
			r = requests.post(coffe_link_mcd, verify = True, data = headers)
			urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', r.text)
			bot.sendFile(pdf_link = urls[1] + "%20Customer%20Feedback%20-%20Coupon%20Web_2.jpg")

bot.message_loop({'chat': on_chat_message}, source=update_queue)
@app.route('/', methods=['GET', 'POST'])
def pass_update():
	update_queue.put(request.data)
	return 'OK [200] HTTP CODE!!'


if __name__ == '__main__':
	app.run(port=8080)
