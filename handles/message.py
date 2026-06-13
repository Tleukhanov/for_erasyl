from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,                        
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from forms.user import Form
from aiogram.fsm.context import FSMContext
from aiogram import Bot
import aiosqlite

router = Router()

# ----,база данных

DB_NAME="Meropryatya.sql"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                email TEXT,
                number INTEGER
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS orders(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                tariff TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        await db.commit()

async def insert_db(user_id, name, age, email, number):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
            INSERT OR IGNORE INTO users (id, name, age, email, number) 
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, name, age, email, number))
        await db.commit() 

async def check_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.cursor()
        await db.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        user = await  cursor.fetchone()
        await cursor.close()
        return user is not None
    
    
async def get_all_orders():
    async with aiosqlite.connect(DB_NAME) as db:    
        cursor = await db.execute("""
            SELECT users.name, users.number, orders.tariff 
            FROM orders 
            JOIN users ON orders.user_id = users.id
        """)
        return await cursor.fetchall()

async def GET_USERS():
    async with aiosqlite.connect(DB_NAME) as db:
        Select=await db.execute("SELECT * FROM users")
        result=await Select.fetchall()
        return result


# ----
def procces_fsm():
    Keyboard=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Пройти анкету",callback_data="Form")]
        ]

    )
    return Keyboard



def get_order_start_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛒 Оформить заказ", callback_data="make_order")]
        ]
    )
    return keyboard
# изменить их калббак дата (изменил)
def get_tariffs_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💎 VIP пакет — 15 000 тг", callback_data="tariff_VIP")],
            [InlineKeyboardButton(text="✨ CLASSIC пакет — 5 000 tг", callback_data="tariff_CLASSIC")],
            [InlineKeyboardButton(text="🌱 EKONOM пакет — 3 000 тг", callback_data="tariff_EKONOM")],
        ]
    )
    return keyboard


@router.callback_query(lambda c: c.data == "Form")
async def processing_of_data(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Давайте начнем заполнять анкету!\nСперва введите свое имя:")
    await state.set_state(Form.name)
    await callback.answer() 

@router.message(Form.name, F.text)
async def procces_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Отлично!\nТеперь введите свой возраст:")
    await state.set_state(Form.age)

@router.message(Form.age, F.text)
async def procces_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Возраст должен быть числом. Введите еще раз:")
        return
    
    if int(message.text) <= 1 or int(message.text) >= 120:
        await message.answer("Возраст должен быть от 1 до 120 лет. Введите еще раз:")
        return

    await state.update_data(age=int(message.text))
    await message.answer("Отлично!\nТеперь введите свой емайл:")
    await state.set_state(Form.email)

@router.message(Form.email, F.text)
async def procces_email(message: Message, state: FSMContext):
    email_text = message.text
    if "@" not in email_text:
        await message.answer("Некорректный емайл! Емайл должен содержать @. Введите еще раз:")
        return
    await state.update_data(email=email_text)

    await message.answer("Отлично!\nТеперь введите свой номер телефона:")
    await state.set_state(Form.number)

@router.message(Form.number, F.text)
async def procces_number(message: Message, state: FSMContext):
    if message.text.startswith("/"):
        await state.clear()
        await start(message)
        return
    
    if not message.text.isdigit():
        await message.answer("Номер должен состоять только из чисел. Введите еще раз:")
        return

    await state.update_data(number=message.text)

    data = await state.get_data()
    name = data["name"]
    age = data["age"]
    email = data["email"]
    number = data["number"]
    user_id=message.from_user.id

    await message.answer(f"Анкета готова!\nИмя: {name}\nВозраст: {age}\nEmail: {email}\nНомер: {number}")
    await insert_db(user_id,data['name'], data['age'], data['email'], data['number'])
    await state.clear()
    await message.answer("Теперь вам доступен заказ:",   
                        reply_markup=get_order_start_keyboard())

def get_main_keyboard_inline():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[ 
            [InlineKeyboardButton(text="💬 Написать в WhatsApp", url="https://wa.me/77765584001")],
            [InlineKeyboardButton(text="ℹ️ Подробнее о сервисе", callback_data="info more")]
        ]
    )
    return keyboard

@router.callback_query(lambda c: c.data == "info more")
async def more_info(callback: CallbackQuery):
    await callback.message.answer(
        "✨ <b>Семей Мероприятие</b> — это чат для удобного заказа организации мероприятий "
        "на любой вкус, бюджет и уровень. \n\n"
        "Мы берём на себя все хлопоты, чтобы ваш праздник прошёл на высшем уровне! 🥂",
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "make_order")
async def process_order_click(callback: CallbackQuery):
    await callback.message.answer(
        "🎯 <b>Пожалуйста, выберите подходящий тарифный пакет:</b>", 
        parse_mode="HTML", 

        reply_markup=get_tariffs_keyboard()
    )
    await callback.answer() 

# ВОТ здесь изменил
@router.callback_query(F.data.startswith("tariff")) 
async def process_tariff_selection(callback: CallbackQuery):
    chosen_tariff = callback.data.split("_")[1]
    user_id = callback.from_user.id
    
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT INTO orders (user_id, tariff) VALUES (?, ?)", (user_id, chosen_tariff))
        await db.commit()
        
    await callback.message.answer(f"✅ Ваш заказ на тариф {chosen_tariff} принят!")
    await callback.answer()

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/about")],
            [KeyboardButton(text="Старт"), KeyboardButton(text="/help")]
        ],
        resize_keyboard=True
    )
    return keyboard

@router.message(Command("start"))
@router.message(F.text.lower() == "старт")
async def start(message: Message,state:FSMContext):
    await state.clear()
    user_id=message.from_user.id
    if await check_user(user_id):
        await message.answer("С возвращением! Выберите действие:",reply_markup=get_order_start_keyboard())
    else:
        await message.answer(
            f"Добро пожаловать в <b>Семей Мероприятие</b>, {message.from_user.first_name}! 👋\n\n"
            "Мы организуем незабываемые праздники и события. "
            "Нажмите на кнопку ниже, что бы пройти анкету, или используйте /help.",
            parse_mode="HTML",
            reply_markup=procces_fsm()
        )

@router.message(Command("help"))
async def help(message: Message):
    await message.answer(
        "📋 <b>Доступные команды бота:</b>\n\n"
        "/start — Перезапустить бота и открыть главное меню\n"
        "/help — Показать список доступных команд\n"
        "/about — Узнать информацию о нас и контакты",
        parse_mode="HTML",
        reply_markup=get_main_keyboard()
    )

@router.message(Command("about"))
async def about(message: Message):
    await message.answer(
        f"💼 <b>О нашем проекте:</b>\n\n"
        f"Приветствуем, {message.from_user.first_name}! Мы занимаемся профессиональной организацией "
        f"мероприятий в городе Семей.\n\n"
        f"📞 Наш прямой контактный номер: <b>+77765584001</b>\n"
        f"<i>(Нажмите на номер телефона выше, чтобы позвонить)</i>\n\n"
        f"Вы можете узнать подробнее по кнопке ниже:",
        parse_mode="HTML",
        reply_markup=get_main_keyboard_inline()
    )

@router.message(Command("show_users_db"))
async def show_users(message: Message):
    users =  await GET_USERS()
    await message.answer(f"Все пользыватели:{users}")

@router.message(Command("orders"))
async def show_all_orders(message: Message):
    orders = await get_all_orders()
    if not orders:
        await message.answer("Пока нет ни одного заказа.")
        return
    
    text = "📋 <b>Список всех заказов:</b>\n\n"
    for order in orders:
        text += f"👤 Имя: {order[0]} | 📞 Тел: {order[1]} | 💎 Тариф: {order[2]}\n"
    
    await message.answer(text, parse_mode="HTML")

@router.message(F.photo)
async def photo_proccess(message:Message):
    photo=message.photo[-1]
    file_id=photo.file_id

    await message.answer(
        f"Вы отправили фото!\n ID photo:<code>{file_id}</code>",
                        parse_mode="HTML"
                        )
    
    await message.answer_photo(file_id,caption="Вот ваше фото")


@router.message(F.video)
async def video_proccess(message:Message):
    video=message.video
    file_id=video.file_id
    duration=video.duration

    await message.answer(
        f"Вы отправили видио!\n ID photo:<code>{file_id}</code>\nДлительность: <code>{duration}</code>",
                        parse_mode="HTML"
                        )
    
    await message.answer_video(file_id,caption="Вот ваше видио")

@router.message(F.document)
async def document_proccess(message:Message,bot:Bot):
    document=message.document
    file_id=document.file_id

    file = await bot.get_file(file_id)
    file_path=file.file_path

    local_path=f"dowlands/{document.file_name}"

    await bot.download_file(file_path=file_path,destination=local_path)

    await message.answer("Файл сохранен")



@router.message()
async def handle_unknown_messages(message: Message):
    await message.answer(
        "⚠️ <i>Извините, я вас не понял. Пожалуйста, воспользуйтесь кнопками меню или отправьте команду /start.</i>",
        parse_mode="HTML"
    )       