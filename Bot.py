"""
Telegram бот для записи на массаж к Ольге
Красивое меню с переходом на DIKIDI Online
"""

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ============ НАСТРОЙКИ ============
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN environment variable is required")
COMPANY_ID = "905912"
BOOKING_URL = f"https://dikidi.ru/{COMPANY_ID}"

# Информация о мастере
MASTER_NAME = "Ольга"
MASTER_PHONE = "+7 (999) 161-29-49"
MASTER_ADDRESS = "г. Ярославль, квартал Светлояр, д.1 Корп 4, цокольный этаж, кабинет 8"
WORK_HOURS = "Пн-Пт: 10:00-19:00\nСб: Выходной\nВс: 11:00-15:00"

# Услуги с прямыми ссылками на запись (отсортированы по алфавиту)
SERVICES = [
    {
        "name": "Антицеллюлитный массаж",
        "price": "1 200₽",
        "duration": "50 минут",
        "desc": "Коррекция фигуры и борьба с целлюлитом",
        "url": "https://dkd.su/905912/s/8799940"
    },
    {
        "name": "Антицеллюлитный массаж живота и бока",
        "price": "750₽",
        "duration": "25 минут",
        "desc": "Уменьшение объёмов талии",
        "url": "https://dkd.su/905912/s/8803448"
    },
    {
        "name": "Антицеллюлитный массаж ягодиц и бедер",
        "price": "750₽",
        "duration": "35 минут",
        "desc": "Коррекция проблемных зон",
        "url": "https://dkd.su/905912/s/8803458"
    },
    {
        "name": "Аппаратный массаж рук и парафинотерапия",
        "price": "300₽",
        "duration": "10 минут",
        "desc": "Уход за кожей рук",
        "url": "https://dkd.su/905912/s/20127792"
    },
    {
        "name": "Детский массаж спины",
        "price": "600₽",
        "duration": "25 минут",
        "desc": "Укрепление мышечного корсета",
        "url": "https://dkd.su/905912/s/8803408"
    },
    {
        "name": "Детский общий массаж",
        "price": "750₽",
        "duration": "45 минут",
        "desc": "Для детей любого возраста",
        "url": "https://dkd.su/905912/s/17183299"
    },
    {
        "name": "Икроножные мышцы и ступни",
        "price": "850₽",
        "duration": "15 минут",
        "desc": "Точечная работа с икрами и стопами",
        "url": "https://dkd.su/905912/s/20488893"
    },
    {
        "name": "Кинезиотейпирование при гиноидной липодистрофии",
        "price": "800₽",
        "duration": "35 минут",
        "desc": "Укрепление соединительной ткани",
        "url": "https://dkd.su/905912/s/16415638"
    },
    {
        "name": "Лимфодренажный массаж спины и рук",
        "price": "1 100₽",
        "duration": "40 минут",
        "desc": "Улучшение лимфотока верхней части тела",
        "url": "https://dkd.su/905912/s/19923546"
    },
    {
        "name": "Лимфодренажный массаж тела",
        "price": "1 700₽",
        "duration": "1 час",
        "desc": "Выведение лишней жидкости и токсинов",
        "url": "https://dkd.su/905912/s/8799946"
    },
    {
        "name": "Массаж головы",
        "price": "350₽",
        "duration": "10 минут",
        "desc": "Снятие головной боли и напряжения",
        "url": "https://dkd.su/905912/s/9406834"
    },
    {
        "name": "Массаж нижних конечностей",
        "price": "850₽",
        "duration": "30 минут",
        "desc": "Расслабление мышц ног",
        "url": "https://dkd.su/905912/s/8803426"
    },
    {
        "name": "Массаж ног детский",
        "price": "550₽",
        "duration": "20 минут",
        "desc": "Для правильного развития",
        "url": "https://dkd.su/905912/s/9480018"
    },
    {
        "name": "Массаж ног лимфодренажный",
        "price": "850₽",
        "duration": "30 минут",
        "desc": "Снятие отёков и усталости ног",
        "url": "https://dkd.su/905912/s/8799974"
    },
    {
        "name": "Массаж рук",
        "price": "400₽",
        "duration": "10 минут",
        "desc": "Расслабление мышц рук",
        "url": "https://dkd.su/905912/s/15352768"
    },
    {
        "name": "Массаж спины",
        "price": "900₽",
        "duration": "30 минут",
        "desc": "Снятие напряжения в спине",
        "url": "https://dkd.su/905912/s/16063566"
    },
    {
        "name": "Массаж живота медовый (Восстановление)",
        "price": "800₽",
        "duration": "30 минут",
        "desc": "Улучшение пищеварения и детокс",
        "url": "https://dkd.su/905912/s/10319604"
    },
    {
        "name": "Медовый массаж на проблемные участки (ягодицы, бедра)",
        "price": "850₽",
        "duration": "30 минут",
        "desc": "Коррекция фигуры",
        "url": "https://dkd.su/905912/s/16415612"
    },
    {
        "name": "Медовый массаж живота (Похудение)",
        "price": "800₽",
        "duration": "30 минут",
        "desc": "Интенсивная работа с жировыми отложениями",
        "url": "https://dkd.su/905912/s/20488884"
    },
    {
        "name": "Моделирующий 3Д массаж лица и декольте",
        "price": "1 000₽",
        "duration": "30 минут",
        "desc": "Лифтинг-эффект и омоложение",
        "url": "https://dkd.su/905912/s/15332916"
    },
    {
        "name": "Общий массаж",
        "price": "1 500₽",
        "duration": "1 час",
        "desc": "Полное расслабление всего тела",
        "url": "https://dkd.su/905912/s/8799926"
    },
    {
        "name": "ШВЗ (шейно-воротниковая зона)",
        "price": "700₽",
        "duration": "20 минут",
        "desc": "Для офисных работников и водителей",
        "url": "https://dkd.su/905912/s/18198767"
    },
]

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

logging.getLogger('httpx').setLevel(logging.WARNING)

# ============ ГЛАВНОЕ МЕНЮ ============


def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("📅 Записаться онлайн", url=BOOKING_URL)],
        [InlineKeyboardButton("💆 Услуги и цены", callback_data="services")],
        [InlineKeyboardButton("📍 Контакты", callback_data="contacts")],
        [InlineKeyboardButton("❓ Частые вопросы", callback_data="faq")],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    welcome = f"""
👋 Привет, {user.first_name}!

Меня зовут {MASTER_NAME}, я профессиональный массажист.

🌟 Здесь вы можете:
• Посмотреть все услуги и цены
• Записаться на удобное время

⬇️ Выберите нужный раздел:
"""

    if update.message:
        await update.message.reply_text(welcome, reply_markup=get_main_menu())
    else:
        await update.callback_query.edit_message_text(
            welcome, reply_markup=get_main_menu())


# ============ УСЛУГИ ============


async def show_services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = "💆 **УСЛУГИ И ЦЕНЫ**\n\n"

    for s in SERVICES:
        text += f"**{s['name']}**\n💰 {s['price']} • ⏱ {s['duration']}\n_{s['desc']}_\n\n"

    keyboard = []
    for s in SERVICES:
        btn_text = s['name'][:30] + "..." if len(s['name']) > 30 else s['name']
        keyboard.append(
            [InlineKeyboardButton(f"📅 {btn_text} — {s['price']}", url=s['url'])])

    keyboard.append([
        InlineKeyboardButton("📂 Показать по категориям", callback_data="categories")
    ])
    keyboard.append([
        InlineKeyboardButton("◀️ Назад", callback_data="back")
    ])

    await query.edit_message_text(text,
                                  reply_markup=InlineKeyboardMarkup(keyboard),
                                  parse_mode="Markdown")


async def show_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    category = query.data.replace("cat_", "")

    categories = {
        "general": {
            "title": "🧘 Общий массаж и релакс",
            "services": [3, 8, 9, 14, 15, 20, 21]  # Аппаратный, Лимфо спины, Лимфо тела, Рук, Спины, Общий, ШВЗ
        },
        "anti": {
            "title": "💪 Антицеллюлитный массаж",
            "services": [0, 1, 2, 7]  # Все антицеллюлитные + кинезиотейпирование
        },
        "legs": {
            "title": "🦵 Массаж ног",
            "services": [6, 11, 12, 13]  # Икроножные, Нижних конечностей, Детский, Лимфо
        },
        "face": {
            "title": "💆‍♀️ Лицо и голова",
            "services": [10, 19]  # Массаж головы, Моделирующий 3Д
        },
        "honey": {
            "title": "🍯 Медовый массаж",
            "services": [16, 17, 18]  # Живота восстановление, На проблемные, Живота похудение
        },
        "kids": {
            "title": "👶 Детский массаж",
            "services": [4, 5]  # Спины, Общий
        }
    }

    cat_data = categories.get(category)
    if not cat_data:
        return

    text = f"**{cat_data['title']}**\n\n"

    keyboard = []
    for idx in cat_data['services']:
        s = SERVICES[idx]
        text += f"**{s['name']}**\n💰 {s['price']} • ⏱ {s['duration']}\n_{s['desc']}_\n\n"
        keyboard.append([InlineKeyboardButton(f"📅 {s['name']}", url=s['url'])])

    keyboard.append([
        InlineKeyboardButton("◀️ Назад к категориям", callback_data="services")
    ])

    await query.edit_message_text(text,
                                  reply_markup=InlineKeyboardMarkup(keyboard),
                                  parse_mode="Markdown")


async def show_categories(update: Update,
                          context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Разделяем услуги по категориям (отсортированы по алфавиту)
    keyboard = [
        [
            InlineKeyboardButton("💪 Антицеллюлитный массаж",
                                 callback_data="cat_anti")
        ],
        [InlineKeyboardButton("👶 Детский массаж", callback_data="cat_kids")],
        [InlineKeyboardButton("💆‍♀️ Лицо и голова", callback_data="cat_face")],
        [InlineKeyboardButton("🍯 Медовый массаж", callback_data="cat_honey")],
        [InlineKeyboardButton("🦵 Массаж ног", callback_data="cat_legs")],
        [
            InlineKeyboardButton("🧘 Общий массаж и релакс",
                                 callback_data="cat_general")
        ],
        [InlineKeyboardButton("◀️ Назад к списку", callback_data="services")],
    ]

    text = """
📂 **УСЛУГИ ПО КАТЕГОРИЯМ**

Выберите категорию:
"""

    await query.edit_message_text(text,
                                  reply_markup=InlineKeyboardMarkup(keyboard),
                                  parse_mode="Markdown")


# ============ КОНТАКТЫ ============


async def show_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = f"""
📍 **КОНТАКТЫ**

👤 Мастер: {MASTER_NAME}

📞 Телефон: {MASTER_PHONE}

📍 Адрес: {MASTER_ADDRESS}

🕐 **Время работы:**
{WORK_HOURS}

💬 Свяжитесь со мной любым удобным способом!
"""

    phone_clean = MASTER_PHONE.replace(" ", "").replace("(", "").replace(
        ")", "").replace("-", "").replace("+", "")

    keyboard = [
        [
            InlineKeyboardButton("💬 WhatsApp",
                                 url=f"https://wa.me/{phone_clean}")
        ],
        [
            InlineKeyboardButton("📱 Telegram",
                                 url="https://t.me/Olga_smirnova76")
        ],
        [
            InlineKeyboardButton("🔵 ВКонтакте",
                                 url="https://vk.com/olenkasmirnova82")
        ],
        [InlineKeyboardButton("📅 Записаться онлайн", url=BOOKING_URL)],
        [InlineKeyboardButton("◀️ Назад", callback_data="back")],
    ]

    await query.edit_message_text(text,
                                  reply_markup=InlineKeyboardMarkup(keyboard),
                                  parse_mode="Markdown")


async def show_faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = """
❓ **ЧАСТЫЕ ВОПРОСЫ**

**Как записаться?**
Нажмите «Записаться онлайн» — откроется страница с расписанием, где вы выберете услугу и удобное время.

**Можно ли отменить запись?**
Да, отмена бесплатна за 3+ часа до сеанса. Отменить можно в DIKIDI или написав мне.

**Как подготовиться к массажу?**
• Не принимайте пищу за 1-2 часа до сеанса
• Примите душ перед визитом
• Сообщите о противопоказаниях (если есть)

**Есть ли противопоказания?**
Массаж не рекомендуется при:
• Повышенной температуре
• Острых воспалительных процессах
• Кожных заболеваниях в стадии обострения
• Онкологии (без разрешения врача)

При сомнениях — напишите мне!

**Формы оплаты?**
Наличные, перевод на карту, СБП.

**Где проходит массаж?**
Уточните адрес при записи или напишите мне.
"""

    keyboard = [
        [
            InlineKeyboardButton("💬 Задать свой вопрос",
                                 callback_data="ask_question")
        ],
        [InlineKeyboardButton("📅 Записаться", url=BOOKING_URL)],
        [InlineKeyboardButton("◀️ Назад", callback_data="back")],
    ]

    await query.edit_message_text(text,
                                  reply_markup=InlineKeyboardMarkup(keyboard),
                                  parse_mode="Markdown")


async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    phone_clean = MASTER_PHONE.replace(" ", "").replace("(", "").replace(
        ")", "").replace("-", "").replace("+", "")

    text = f"""
💬 **Задать вопрос**

Вы можете:
• Написать сообщение прямо в этот чат
• Написать в WhatsApp
• Написать в Telegram

Я отвечу как можно скорее! 😊
"""

    keyboard = [
        [
            InlineKeyboardButton("💬 WhatsApp",
                                 url=f"https://wa.me/{phone_clean}")
        ],
        [
            InlineKeyboardButton("📱 Telegram",
                                 url="https://t.me/Olga_smirnova76")
        ],
        [InlineKeyboardButton("◀️ Назад", callback_data="faq")],
    ]

    await query.edit_message_text(text,
                                  reply_markup=InlineKeyboardMarkup(keyboard),
                                  parse_mode="Markdown")


# ============ ОБРАБОТКА СООБЩЕНИЙ ============


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текстовых сообщений от клиентов"""
    user = update.effective_user
    text = update.message.text

    # Логируем сообщение (можно настроить пересылку на твой Telegram)
    logger.info(f"Сообщение от {user.first_name} (@{user.username}): {text}")

    response = f"""
✅ Спасибо за сообщение!

Я получила ваш вопрос и отвечу в ближайшее время.

Для срочных вопросов звоните:
📞 {MASTER_PHONE}
"""

    keyboard = [[InlineKeyboardButton("📅 Записаться", url=BOOKING_URL)],
                [InlineKeyboardButton("🏠 Главное меню", callback_data="back")]]

    await update.message.reply_text(
        response, reply_markup=InlineKeyboardMarkup(keyboard))


# ============ ОБРАБОТЧИК КНОПОК ============


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data == "services":
        await show_services(update, context)
    elif data == "categories":
        await show_categories(update, context)
    elif data.startswith("cat_"):
        await show_category(update, context)
    elif data == "contacts":
        await show_contacts(update, context)
    elif data == "faq":
        await show_faq(update, context)
    elif data == "ask_question":
        await ask_question(update, context)
    elif data == "back":
        await start(update, context)


# ============ ЗАПУСК ============


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("🚀 Бот Ольги запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
