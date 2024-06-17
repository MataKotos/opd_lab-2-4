import asyncio
import logging
import time
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

class Question(object):
    def __init__(self, message, variants: list, answerId):
        self.message = message
        self.variants = variants
        self.answerId = answerId

# Массив всех вопросов, которые будут задаваться пользователю
questions = [
    Question("Какое насекомое вызвало короткое замыкание в ранней версии вычислительной машины, тем самым породив термин «компьютерный баг» («баг» в переводе с англ. «насекомое»)?",
             ["Мотылёк", "Муха", "Таракан", "Японский хрущик"], 0),
    Question("Под каким названием известна единица с последующими ста нулями?",
        ["Гугол", "Мегатрон", "Гигабит", "Наномоль"], 0),
    Question("Сколько кубиков в кубике Рубика?",
        ["22", "24", "26", "28"], 2),
    Question("Какая единица измерения названа в честь итальянского дворянина?",
        ["Паскаль", "Ом", "Вольт", "Герц"], 2)

]

# Словарь, где ключ - пользователь, а значение - индекс вопроса, на котором он остановился
currentQuestionIds = {}

# Логирование для обработки ошибок или понимания, что всё идёт как надо
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token="6590127281:AAG27TtBDhkhPV1GMqTDQKDbHWl8VKU0uZE")

# Диспетчер
dp = Dispatcher()

# Обрабатываем команду "/start"
@dp.message(Command("start"))
async def start(message: types.Message):
    # Если пользователь уже есть в базе данных
    if message.sender_chat in currentQuestionIds:
        await message.answer("Давайте продолжим викторину!")
        # Спрашиваем вопрос, на котором он остановился
        await ask(message)
    else:
        await message.answer("Начинаем викторину!")
        # Устанавливаем значение 0, дав боту понять, что пользователь уже начал игру и спрашиваем первый вопрос
        currentQuestionIds[message.sender_chat] = 0
        await ask(message)

@dp.message()
async def handle_message(message: types.Message):
    print(message.from_user.username + ' writes: ' + message.text)

    # Если это команда старта - игнорируем, её обработает метод выше
    if message.text == '/start':
        return

    # Если пользователь хочет сыграть заново
    if message.text == 'Заново':
        # Возвращаем пользователя к первому вопросу
        currentQuestionIds[message.sender_chat] = 0
        await ask(message)
        return

    # Если пользователь есть в словаре
    if message.sender_chat in currentQuestionIds:
        # Создаём переменную-индекс текущего вопроса (для удобства)
        questionIndex = currentQuestionIds[message.sender_chat]

        # Если текст сообщения - один из вариантов ответа
        if message.text in questions[questionIndex].variants:
            # Создаём переменную-индекс выбранного ответа (для удобства)
            answerIndex = questions[questionIndex].variants.index(message.text)

            # Если ответ правильный
            if answerIndex == questions[questionIndex].answerId:
                # Если это не последний вопрос
                if questionIndex != len(questions) - 1:
                    await message.answer("Верно! Продолжаем...")
                    currentQuestionIds[message.sender_chat] += 1

                    # Переходим к следующему вопросу
                    await ask(message)
                else:
                    # Поздравляем пользователя и предлагаем сыграть заново
                    kb = [[types.KeyboardButton(text="Заново")]]
                    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
                    await message.answer("Супер! Вы прошли викторину!", reply_markup=keyboard)
            else:
                # В случае неправильного ответа возвращаем пользователя к первому вопросу
                await message.answer("Неправильно. Давайте заново.")
                currentQuestionIds[message.sender_chat] = 0
                await ask(message)


# Метод, задающий пользователю вопрос
async def ask(message: types.Message):
    # Получаем вопрос, на котором остановился пользователь
    question = questions[currentQuestionIds[message.sender_chat]]

    # Кнопки для вариантов ответа будут заливаться сюда
    kb = [[], [types.KeyboardButton(text="Заново")]]
    # Создаём кнопочки из вариантов ответа
    for item in question.variants:
        # Добавляем кнопку с вариантом ответа
        button = types.KeyboardButton(text=item)
        kb[0].append(button)

    # Задаём вопрос и показываем кнопки
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer(question.message, reply_markup=keyboard)

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())