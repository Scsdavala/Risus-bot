from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import random

BOT_TOKEN = "8331009511:AAGZIDOMzAdL_QlE5MG5bJgY7xPD0aa-bDc"
BOT_NAME = "Risus"
ADMIN_ID = 453158012

WELCOME_TEXT = """
*Привіт, я невидимий співрозмовник 🤫*  
Мені неважливо, як ти виглядаєш і де ти знаходишся.  
Я хочу почути те, про що ти мовчиш — те, що тисне на груди.  
Усе анонімно. Я не психолог — я той, хто чує.  
Може, вже досить мовчати?  
Напиши хоча б одне речення — я відповім.
"""

ABOUT_TEXT = """
*Risus — твій анонімний співрозмовник 🤫🇺🇦*  
Ми створили Risus, щоб кожен українець мав місце, де можна виговоритися, поділитися тим, що тисне на серце, або просто отримати пораду без осуду й без зайвих питань.  
Тут ти можеш:  
• виговоритися повністю анонімно  
• поділитися своїми проблемами та переживаннями  
• отримати підтримку та слушну пораду  
• знайти розуміння у складний момент  

Після кожної розмови бот дає коротку психологічну пораду, яка допоможе заспокоїтись, відновитись і продовжити рух далі.  

Жодної реєстрації. Жодних даних. Лише ти й співрозмовник, який слухає.  
Все цілком безкоштовно.  
Але якщо захочеш — у боті є донат, який допомагає підтримувати та розвивати Risus.  

*Бо іноді людині достатньо просто того, щоб її хтось почув.*  
Пиши, коли важко. Risus поруч.
"""

DONATE_TEXT = """
*Донат — підтримай Risus та ЗСУ* ❤️  

Кожна гривня — це підтримка тих, хто нас захищає.  

**Банківська картка (Монобанк):**  
`4874070010202685`  

**Крипта (USDT TRC20):**  
`12CM8vHSMfar7nGekYTphvbBS2rHD4DqLd`  

*Не забувай донатити на ЗСУ — це наш спільний обов’язок.*  
Дякую тобі за підтримку! Ти робиш різницю. 🙏
"""

PSYCH_TIPS = [
    "Дихай повільно: 4 секунди вдих — 4 затримка — 4 видих. Це заспокоює нервову систему.",
    "Ти не сам. Навіть у найтемніші моменти є світло — ти його знайдеш.",
    "Запиши 3 речі, за які ти вдячний сьогодні. Це змінює фокус.",
    "Ти сильніший, ніж думаєш. Ти вже пройшов стільки — і пройдеш ще.",
    "Дозволь собі бути вразливим. Це не слабкість — це сила."
]

def main_menu():
    keyboard = [
        [InlineKeyboardButton("Розпочати розмову", callback_data="start_chat")],
        [InlineKeyboardButton("Про мене", callback_data="about")],
        [InlineKeyboardButton("Донат", callback_data="donate")],
        [InlineKeyboardButton("Завершити діалог", callback_data="end")],
    ]
    return InlineKeyboardMarkup(keyboard)

CHAT_ACTIVE = "chat_active"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_TEXT, parse_mode='Markdown', reply_markup=main_menu())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "start_chat":
        context.user_data[CHAT_ACTIVE] = True
        await query.edit_message_text(
            "Чат розпочато! Пиши — я передам твої слова адміну.\n"
            "Або натисни /stop, щоб завершити.",
            reply_markup=back_button()
        )

    elif query.data == "about":
        await query.edit_message_text(ABOUT_TEXT, parse_mode='Markdown', reply_markup=back_button())

    elif query.data == "donate":
        await query.edit_message_text(DONATE_TEXT, parse_mode='Markdown', reply_markup=back_button())

    elif query.data == "end":
        tip = random.choice(PSYCH_TIPS)
        await query.edit_message_text(
            f"Дякую за розмову! ❤️\n"
            f"Ось маленька порада:\n_{tip}_\n\n"
            f"Пиши /start, коли захочеш повернутись.",
            parse_mode='Markdown'
        )
        if context.user_data.get(CHAT_ACTIVE):
            context.user_data[CHAT_ACTIVE] = False

    elif query.data == "back":
        await query.edit_message_text(WELCOME_TEXT, parse_mode='Markdown', reply_markup=main_menu())
        if context.user_data.get(CHAT_ACTIVE):
            context.user_data[CHAT_ACTIVE] = False

async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get(CHAT_ACTIVE):
        user = update.message.from_user
        username = f"@{user.username}" if user.username else "Анонім"
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"Нова анонімна розмова від {username} ({user.id}):\n\n{update.message.text}"
        )
        await update.message.reply_text("Повідомлення відправлено. Я чекаю відповіді...")

async def stop_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get(CHAT_ACTIVE):
        context.user_data[CHAT_ACTIVE] = False
        tip = random.choice(PSYCH_TIPS)
        await update.message.reply_text(
            f"Чат завершено.\n"
            f"Ось маленька порада:\n_{tip}_\n\n"
            f"Пиши /start, щоб почати знову.",
            parse_mode='Markdown',
            reply_markup=main_menu()
        )

def back_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="back")]])

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("stop", stop_chat))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_admin))
    print(f"{BOT_NAME} запущений!")
    app.run_polling()
