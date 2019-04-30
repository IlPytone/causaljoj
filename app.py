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
			requests.post("https://api.telegram.org/bot885925187:AAH9GMyKo6EICdqKc5hzHqzXj2Qxyj_PPMQ/sendMessage?chat_id="+str(chat_id)+"&text=Buongiorno "+ msg["from"]["first_name"]+", ti auguro di gustarti un buon caffè gratis. 🤙")
		elif text.startswith("/ping"):
			requests.post("https://api.telegram.org/bot885925187:AAH9GMyKo6EICdqKc5hzHqzXj2Qxyj_PPMQ/sendMessage?chat_id="+str(chat_id)+"&text=Pong.")
		elif text.startswith("/coffe"):
			r = requests.post(coffe_link_mcd, verify = True, data = headers)
			urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', r.text)
			requests.post("https://api.telegram.org/bot885925187:AAH9GMyKo6EICdqKc5hzHqzXj2Qxyj_PPMQ/sendDocument?chat_id="+str(chat_id)+"&document="+"http://survey.fast-insight.com/mcd/it/v2025_coupon.php?code="+ urls[74:106] + "&type=c"))

bot.message_loop({'chat': on_chat_message}, source=update_queue)
@app.route('/', methods=['GET', 'POST'])
def pass_update():
	update_queue.put(request.data)
	return 'OK [200] HTTP CODE!!'


if __name__ == '__main__':
	app.run(port=8080)
