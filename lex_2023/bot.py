
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from PIL import Image, ImageDraw
from io import BytesIO
import sqlite3
import re

API_TOKEN = ''
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging_middleware = LoggingMiddleware()
dp.middleware.setup(logging_middleware)

# Создаем базу данных SQLite
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    email TEXT,
    password TEXT,
    image BLOB
)
''')
conn.commit()


class RegistrationStates(StatesGroup):
    EMAIL = State()
    PASSWORD = State()
    UPLOAD_IMAGE = State()


@dp.message_handler(commands=['start'])
async def start_registration(message: types.Message):
    await RegistrationStates.EMAIL.set()
    await message.reply("Добро пожаловать! Введите ваш email для регистрации.")
    logging.info(f"User {message.from_user.id} started registration process.")


@dp.message_handler(content_types=['text'], state=RegistrationStates.EMAIL)
async def process_email(message: types.Message, state: FSMContext):
    email = message.text.lower().strip()

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        await message.reply("Неверный формат email. Пожалуйста, введите корректный email.")
        return

    await state.update_data(email=email)
    await RegistrationStates.PASSWORD.set()
    await message.reply("Отлично! Теперь введите пароль (минимум 6 цифр).")
    logging.info(f"User {message.from_user.id} provided email {email}.")


@dp.message_handler(content_types=['text'], state=RegistrationStates.PASSWORD)
async def process_password(message: types.Message, state: FSMContext):
    password = message.text

    if not password.isdigit() or len(password) < 6:
        await message.reply("Неверный формат пароля. Пожалуйста, введите пароль, состоящий минимум из 6 цифр.")
        return

    await state.update_data(password=password)
    await RegistrationStates.UPLOAD_IMAGE.set()
    await message.reply("Прекрасно! Теперь отправьте изображение для загрузки.")
    logging.info(f"User {message.from_user.id} provided password.")


@dp.message_handler(content_types=['photo'], state=RegistrationStates.UPLOAD_IMAGE)
async def process_image(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id
    email = data.get('email')
    password = data.get('password')

    # Получение объекта фото с наивысшим разрешением
    photo = max(message.photo, key=lambda ph: ph.width)
    file_id = photo.file_id
    image = await bot.download_file_by_id(file_id)

    # Сохранение изображения в базе данных
    save_image_to_database(user_id, email, password, image)

    # Обработка и отправка изображения
    rounded_image = process_rounding(image)
    await bot.send_photo(message.chat.id, photo=types.InputFile(BytesIO(rounded_image)))
    await state.finish()
    await message.reply("Регистрация завершена. Спасибо!")


def process_rounding(image):
    with Image.open(image) as img:
        img = img.convert("RGBA")
        size = img.size
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)
        result = Image.new("RGBA", size, (0, 0, 0, 0))
        result.paste(img, (0, 0), mask)
        result.crop(result.getbbox())

        # Сохраняем изображение в байтовый объект
        output_buffer = BytesIO()
        result.save(output_buffer, format="PNG")
        rounded_image_bytes = output_buffer.getvalue()

        return rounded_image_bytes


def save_image_to_database(user_id, email, password, image):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Проверка, существует ли пользователь в базе данных
    cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        # Обновление изображения для существующего пользователя
        cursor.execute('UPDATE users SET email=?, password=?, image=? WHERE user_id=?',(email, password, image.read(), user_id))
    else:
        # Добавление нового пользователя
        cursor.execute('INSERT INTO users (user_id, email, password, image) VALUES (?, ?, ?, ?)',
                       (user_id, email, password, image.read()))

    conn.commit()
    conn.close()

# if __name__ == '__main__':
#     from aiogram import executor
#     executor.start_polling(dp)


async def main():
    await dp.start_polling()