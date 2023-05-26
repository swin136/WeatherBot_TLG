import requests
import datetime
from config import telegram_bot_token, open_weather_token
from main import get_city_coordinates
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


 
bot = Bot(token = telegram_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands = ["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города по-английски и я пришлю сводку погоды!")



@dp.message_handler()
async def get_weather(message: types.Message):
    """
    Пытаемся получить погоду по месту с координатами
    """
  
    code_to_smile = {
         "Clear" : "Ясно \U00002600",
         "Clouds" : "Облачно \U00002601",
         "Rain" : "Дождь \U00002614",
         "Drizzle" : "Дождь \U00002614",
         "Thunderstorm" : "Гроза \U000026A1",
         "Snow" : "Снег \U0001F328",
         "Mist" : "Снег \U0001F328" 
    }

    locate_city = get_city_coordinates(message.text, open_weather_token)
    if locate_city[0] == None:
        await message.reply("С названием Вашего города что-то не так!")

    
    city = locate_city[0]

    try:
        lat = locate_city[1]
        lon = locate_city[2]
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={open_weather_token}&units=metric"
        )
       
        data = r.json()
        # pprint(data)

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile: wd = code_to_smile[weather_description]
        else: wd = "Посмотри в окно, не пойму что за погода"

        cur_temp = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure'] 
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise']) 
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset']) 
        length_of_the_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(data['sys']['sunrise']) 

        if "городской округ" in city: frmt_city =(str(city).replace("городской округ", "")).strip()
        else: frmt_city = city

        await message.reply(f"****** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} ******\n"
              f"[+] Погода в городе {frmt_city}\n"
              f"Температура: {cur_temp} С° {wd}\n"
              f"Влажность: {humidity} %\nДавление: {pressure} мм рт. ст\nВетер: {wind} м\с\n"
              f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\n"
              f"Длительность дня {length_of_the_day}\n"
              f"[+] Хорошего дня!"
              )

            
    except:
        await message.replay("Проверь название города!")




if __name__ == "__main__":
    executor.start_polling(dp)
