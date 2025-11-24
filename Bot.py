"""
Telegram бот для записи на массаж к Ольге
Красивое меню с переходом на DIKIDI Online
"""

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ============ НАСТРОЙКИ ============
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8507485840:AAHeVLw3aCyWMzInGS07wq2csPbGvf7B0e4")
COMPANY_ID = "905912"
BOOKING_URL = f"https://dikidi.ru/{COMPANY_ID}"

# Информация о мастере
MASTER_NAME = "Ольга"
MASTER_PHONE = "+7 (999) 161-29-49"
MASTER_EMAIL = "os3188275@gmail.com"
WORK_HOURS = "Пн-Пт: 10:00-19:00\nСб: 11:00-16:00\nВс: Выходной"

# QR-код для записи (укажи путь к файлу Qr_1.jpg)
QR_CODE_PATH = "Qr_1.jpg"  # положи файл рядом с bot.py

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
        "name": "Аппаратный массаж рук + парафинотерапия",
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
        "name": "Кинезиотейпирование",
        "price": "800₽",
        "duration": "35 минут",
        "desc": "При гиноидной липодистрофии",
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
        "name": "Медовый массаж",
        "price": "850₽",
        "duration": "30 минут",
        "desc": "Детокс и питание кожи",
        "url": "https://dkd.su/905912/s/16415612"
    },
    {
        "name": "Медовый массаж живота",
        "price": "800₽",
        "duration": "30 минут",
        "desc": "Улучшение пищеварения и детокс",
        "url": "https://dkd.su/905912/s/10319604"
    },
    {
        "name": "Моделирующий 3Д массаж лица",
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

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ============ ГЛАВНОЕ МЕНЮ ============

def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("📅 Записаться онлайн", url=BOOKING_URL)],
        [InlineKeyboardButton("💆 Услуги и цены", callback_data="services")],
        [InlineKeyboardButton("📍 Контакты", callback_data="contacts")],
        [InlineKeyboardButton("📱 QR-код для записи", callback_data="qr")],
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
• Получить QR-код для быстрой записи

⬇️ Выберите нужный раздел:
"""
    
    if update.message:
        await update.message.reply_text(welcome, reply_markup=get_main_menu())
    else:
        await update.callback_query.edit_message_text(welcome, reply_markup=get_main_menu())

# ============ УСЛУГИ ============

async def show_services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Разделяем услуги по категориям
    keyboard = [
        [InlineKeyboardButton("🧘 Общий массаж и релакс", callback_data="cat_general")],
        [InlineKeyboardButton("💪 Антицеллюлитный массаж", callback_data="cat_anti")],
        [InlineKeyboardButton("🦵 Массаж ног", callback_data="cat_legs")],
        [InlineKeyboardButton("💆‍♀️ Лицо и голова", callback_data="cat_face")],
        [InlineKeyboardButton("🍯 Медовый массаж", callback_data="cat_honey")],
        [InlineKeyboardButton("👶 Детский массаж", callback_data="cat_kids")],
        [InlineKeyboardButton("📋 Все услуги списком", callback_data="all_services")],
        [InlineKeyboardButton("◀️ Назад", callback_data="back")],
    ]
    
    text = """
💆 **УСЛУГИ И ЦЕНЫ**

Выберите категорию услуг или посмотрите полный список:
"""
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def show_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    category = query.data.replace("cat_", "")
    
    categories = {
        "general": {
            "title": "🧘 Общий массаж и релакс",
            "services": [0, 1, 3, 4, 13]  # индексы в SERVICES
        },
        "anti": {
            "title": "💪 Антицеллюлитный массаж",
            "services": [2, 11, 12]
        },
        "legs": {
            "title": "🦵 Массаж ног",
            "services": [5, 6, 7]
        },
        "face": {
            "title": "💆‍♀️ Лицо и голова",
            "services": [8, 15]
        },
        "honey": {
            "title": "🍯 Медовый массаж",
            "services": [9, 10]
        },
        "kids": {
            "title": "👶 Детский массаж",
            "services": [18, 19, 20]
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
    
    keyboard.append([InlineKeyboardButton("◀️ Назад к категориям", callback_data="services")])
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def show_all_services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    text = "💆 **ВСЕ УСЛУГИ**\n\n"
    
    for s in SERVICES[:10]:  # Первые 10 услуг
        text += f"• **{s['name']}** — {s['price']} ({s['duration']})\n"
    
    text += f"\n_...и ещё {len(SERVICES)-10} услуг_\n\n"
    text += "👇 Нажмите на услугу ниже для записи:"
    
    keyboard = []
    for s in SERVICES:
        btn_text = s['name'][:30] + "..." if len(s['name']) > 30 else s['name']
        keyboard.append([InlineKeyboardButton(f"{btn_text} — {s['price']}", url=s['url'])])
    
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="services")])
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

# ============ КОНТАКТЫ ============

async def show_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    text = f"""
📍 **КОНТАКТЫ**

👤 Мастер: {MASTER_NAME}

📞 Телефон: {MASTER_PHONE}
📧 Email: {MASTER_EMAIL}

🕐 **Время работы:**
{WORK_HOURS}

💬 Свяжитесь со мной любым удобным способом!
"""
    
    phone_clean = MASTER_PHONE.replace(' ', '').replace('(', '').replace(')', '').replace('-', '').replace('+', '')
    
    keyboard = [
        [InlineKeyboardButton("📞 Позвонить", url=f"tel:{MASTER_PHONE}")],
        [InlineKeyboardButton("💬 WhatsApp", url=f"https://wa.me/{phone_clean}")],
        [InlineKeyboardButton("📧 Написать email", url=f"mailto:{MASTER_EMAIL}")],
        [InlineKeyboardButton("📅 Записаться онлайн", url=BOOKING_URL)],
        [InlineKeyboardButton("◀️ Назад", callback_data="back")],
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

# ============ QR-КОД ============

async def show_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    text = """
📱 **QR-КОД ДЛЯ ЗАПИСИ**

Отсканируйте QR-код камерой телефона для быстрой записи!

Или используйте кнопку ниже 👇
"""
    
    keyboard = [
        [InlineKeyboardButton("📅 Открыть страницу записи", url=BOOKING_URL)],
        [InlineKeyboardButton("◀️ Назад", callback_data="back")],
    ]
    
    # Пытаемся отправить QR-код
    try:
        # Удаляем предыдущее сообщение
        await query.message.delete()
        
        # Отправляем QR-код
        with open(QR_CODE_PATH, 'rb') as photo:
            await context.bot.send_photo(
                chat_id=query.message.chat_id,
                photo=photo,
                caption=text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown"
            )
    except FileNotFoundError:
        # Если файл не найден, просто показываем текст
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=text + "\n\n⚠️ _QR-код временно недоступен_",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Ошибка отправки QR: {e}")
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

# ============ FAQ ============

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
        [InlineKeyboardButton("💬 Задать свой вопрос", callback_data="ask_question")],
        [InlineKeyboardButton("📅 Записаться", url=BOOKING_URL)],
        [InlineKeyboardButton("◀️ Назад", callback_data="back")],
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    phone_clean = MASTER_PHONE.replace(' ', '').replace('(', '').replace(')', '').replace('-', '').replace('+', '')
    
    text = f"""
💬 **Задать вопрос**

Вы можете:
• Написать сообщение прямо в этот чат
• Позвонить: {MASTER_PHONE}
• Написать в WhatsApp

Я отвечу как можно скорее! 😊
"""
    
    keyboard = [
        [InlineKeyboardButton("💬 WhatsApp", url=f"https://wa.me/{phone_clean}")],
        [InlineKeyboardButton("📞 Позвонить", url=f"tel:{MASTER_PHONE}")],
        [InlineKeyboardButton("◀️ Назад", callback_data="faq")],
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

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
    
    keyboard = [
        [InlineKeyboardButton("📅 Записаться", url=BOOKING_URL)],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="back")]
    ]
    
    await update.message.reply_text(response, reply_markup=InlineKeyboardMarkup(keyboard))

# ============ ОБРАБОТЧИК КНОПОК ============

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    
    if data == "services":
        await show_services(update, context)
    elif data.startswith("cat_"):
        await show_category(update, context)
    elif data == "all_services":
        await show_all_services(update, context)
    elif data == "contacts":
        await show_contacts(update, context)
    elif data == "qr":
        await show_qr(update, context)
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
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("🚀 Бот Ольги запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()