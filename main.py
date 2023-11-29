import asyncio
from datetime import datetime, timedelta
import logging
import os

from aiogram import Bot, Dispatcher, types, filters
from dateparser import parse
from dotenv import load_dotenv
import requests

load_dotenv()  # Загрузка переменных из .env файла

bot = Bot(token=os.getenv('BOT_TOKEN'))  # Инициализация бота
dp = Dispatcher()  # Инициализация диспетчера


# Основная функция
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot, skip_updates=True)


# Обработчик команды /start
@dp.message(filters.CommandStart())
async def send_welcome(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! Я гидрометеобот, который поможет тебе узнать погоду!\n"
        "Напиши в чат /help, чтобы узнать больше о возможностях!")


# Обработчик команды /help
@dp.message(filters.Command("help"))
async def get_help(message: types.Message):
    await message.answer(
        "/weather <город> - возвращает подробную информацию о погоде в указанном городе в данный момент\n"
        "/forecast <город> - возвращает краткий прогноз погоды на каждые 3 часа на ближайшие 5 дней \n"
        "/weatherattime <город> <время> - возвращает подробную информацию в указанном городе в указанный момент времени"
        ", но не дальше чем на 5 дней вперед"
    )


# Обработчик команды /weather, возвращающей текущие погодные условия в указаном городе
@dp.message(filters.Command("weather"))
async def get_weather(message: types.Message):
    city = message.text.split(maxsplit=1)[1]  # Получения названия города
    url = (f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.getenv('OPENWEATHER_API_KEY')}"
           f"&units=metric&lang=ru")  # Обращение к Weather API
    response = requests.get(url)
    # В случае отсутствия ошибок
    if response.status_code == 200:
        # Получение погодных данных из json файла
        data = response.json()
        icon = data['weather'][0]['icon']
        icon_url = f'https://openweathermap.org/img/wn/{icon[0:2]}d@2x.png'
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        windspeed = data['wind']['speed']
        # Вывод данных вместе с иконкой
        await message.answer_photo(photo=icon_url,
                                   caption=(f"Погода в городе {city.capitalize()} сейчас: {weather.capitalize()} \n"
                                            f" 🌡️ Температура: {temperature}°C \n 💧 Влажность: {humidity}% \n"
                                            f" ⬇️ Давление: {pressure} мм.рт.ст. \n 💨️ Скорость ветра: {windspeed}м/c")
                                   )

    else:
        await message.answer(
            "Ошибка: проверьте правильно ли указан город и повторите попытку.")


# Обработчик команды /forecast, возвращающей погодные условия на ближайшие 5 дней
@dp.message(filters.Command("forecast"))
async def get_forecast(message: types.Message):
    city = message.text.split()[1]  # Получение города из сообщения
    url = (f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={os.getenv('OPENWEATHER_API_KEY')}"
           f"&units=metric&lang=ru")  # Обращение к Weather API
    response = requests.get(url)
    # В случае отсутствия ошибок
    if response.status_code == 200:
        # Получение погодных данных из json файла
        data = response.json()
        # Создание списка данных, которые выведутся в конце
        forecast = []
        for item in data['list']:
            time = item['dt_txt']
            weather = item['weather'][0]['description']
            temperature = item['main']['temp']
            forecast.append(f"{time}: {temperature}°C, {weather.capitalize()}")
        # Вывод объединенного списка данных
        await message.answer("\n".join(forecast))
    else:
        await message.answer(
            "Ошибка: проверьте правильно ли указан город и повторите попытку.")


# Обработчик команды /wheatherattime, возвращающей погодные условия в указанном городе в указанное время
@dp.message(filters.Command("weatherattime"))
async def get_weather_at_time(message: types.Message):
    city = message.text.split(maxsplit=2)[1]  # Получение города из команды
    time = parse(message.text.split(maxsplit=2)[2])  # Получение времени из команды
    url = (f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={os.getenv('OPENWEATHER_API_KEY')}"
           f"&units=metric&lang=ru")  # Обращение к Weather API
    response = requests.get(url)
    # В случае отсутствия ошибок
    if response.status_code == 200:
        # Получение погодных данных из json файла
        data = response.json()
        # Самый подходящий по времени прогноз (изначально такого нет)
        closest_forecast = None
        # Идем по массиву пронозов на каждые 3 часа
        for item in data['list']:
            forecast_time = datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S')
            time_diff = abs(forecast_time - time)
            # Так как интервал прогноза 3 часа, то подходящий прогноз будет находится в ~90 минутах от данного времени
            if time_diff < timedelta(0, 0, 0, 1, 31, 0, 0):
                closest_forecast = item
        # Если подходящий прогноз существует (пользователь не ушел за время в 5 дней), выведем его погодные данные
        if closest_forecast:
            icon = closest_forecast['weather'][0]['icon']
            icon_url = f'https://openweathermap.org/img/wn/{icon[0:2]}d@2x.png'
            weather = closest_forecast['weather'][0]['description']
            temperature = closest_forecast['main']['temp']
            humidity = closest_forecast['main']['humidity']
            pressure = closest_forecast['main']['pressure']
            windspeed = closest_forecast['wind']['speed']
            # Вывод данных вместе с иконкой
            await message.answer_photo(photo=icon_url,
                                       caption=(
                                           f"Погода в городе {city.capitalize()} {message.text.split(maxsplit=2)[2]}:"
                                           f" {weather.capitalize()} \n"
                                           f" 🌡️ Температура: {temperature}°C \n 💧 Влажность: {humidity}% \n"
                                           f" ⬇️ Давление: {pressure} мм.рт.ст. \n 💨️ Скорость ветра: {windspeed}м/c"))
        # Ошибка при выходе пользователем за временные рамки
        else:
            await message.answer("Ошибка: невозможно получить информацию о погоде на данное время")
    # Ошибка при неверном указании города
    else:
        await message.answer(
            "Ошибка: проверьте правильно ли указан город и повторите попытку.")


# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())
