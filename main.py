import os
from flask import Flask, render_template_string
import threading, random, time
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- آپ کا ٹوکن Render سے لے گا ---
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

app = Flask(__name__)
signals = []

HTML = """
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{background:#0f1115;color:white;font-family:sans-serif;text-align:center;padding:15px}
.card{background:#1c1f26;padding:15px;border-radius:15px;margin:10px 0;border:1px solid #00ff8855}
.strong{color:#00ff88;font-weight:bold} .medium{color:#ffcc00} .weak{color:#ff4444}
h1{color:#00ff88}
</style></head><body>
<h1>💎 SULEHRI BOT V3</h1><p>Payout 80%+ Filter | Live Scanner</p>
<p>Last: {{time}}</p>
{% for s in signals %}
<div class="card"><b>{{s.pair}}</b> | {{s.action}} | Payout: {{s.payout}}% | <span class="{{s.c}}">{{s.s}}</span></div>
{% endfor %}
</body></html>
"""

@app.route('/')
def home():
    return render_template_string(HTML, signals=list(reversed(signals[-15:])), time=datetime.now().strftime("%H:%M:%S"))

def gen():
    pairs=["EUR/USD","GBP/USD","USD/JPY","BTC/USD","EUR/JPY"]
    while True:
        payout=random.randint(78,95)
        if payout>=80:
            v=random.randint(1,100)
            s="STRONG" if v>75 else "MEDIUM" if v>45 else "WEAK"
            c="strong" if v>75 else "medium" if v>45 else "weak"
            a=random.choice(["BUY","SELL"])
            signals.append(type('obj',(object,),{'pair':random.choice(pairs),'action':a,'payout':payout,'s':s,'c':c}))
            if len(signals)>50: signals.pop(0)
        time.sleep(12)

# --- TELEGRAM BOT PART ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Sulehri Bot Live hai!\n\n💎 Latest Signals dekhne ke liye website kholen:\nhttps://sulehri-bot.onrender.com\n\nBot har 12 sec me signal generate kar raha hai.")

def run_telegram():
    if not BOT_TOKEN:
        print("BOT TOKEN NAHI MILA!")
        return
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    print("Telegram Bot Starting...")
    application.run_polling()

# --- DONO KO SATH CHALANA ---
threading.Thread(target=gen, daemon=True).start()
threading.Thread(target=run_telegram, daemon=True).start()

if __name__=='__main__': 
    app.run(host='0.0.0.0', port=10000)
