"""
Telegram bot на Python + aiogram | Прогноз погоды в любом городе | API погоды | Парсинг JSON
https://www.youtube.com/watch?v=fa1FUW1jLAE&t=909s
"""

import requests
import datetime
from pprint import pprint
from config import open_weather_token, replace_flag_cities_UA 


def get_weather(calc_lat, calc_lon, city, open_weather_token):
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

    try:
        lat = calc_lat
        lon = calc_lon
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
        country  = data['sys']['country']

        if "городской округ" in city: frmt_city =(str(city).replace("городской округ", "")).strip()
        else: frmt_city = city

        # Замена UA - RU
        if frmt_city in replace_flag_cities_UA: country = replace_flag_cities_UA[frmt_city]

        print(f"****** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} ******\n"
              f"[+] Погода в городе {frmt_city} {country}\n"
              f"Температура: {cur_temp} С° {wd}\n"
              f"Влажность: {humidity} %\nДавление: {pressure} мм рт. ст\nВетер: {wind} м\с\n"
              f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\n"
              f"Длительность дня {length_of_the_day}\n"
              f"Хорошего дня!"
              )

            
    except Exception as ex:
        print(ex)
        print("Проверь название города!")


def get_city_coordinates(city, open_weather_token):
    """
    Пытаемся получить кординаты города, выбранного пользователем 
    """
    result = [None, None, None]
    try:
        r = requests.get(
             f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={open_weather_token}"
        )
    except Exception as ex:
                print(ex)
                print("Проверь название города!")
    data = r.json()
    # pprint(data)

    # Парсим наши данные: название города на русском, широту и долготу 
    if len(data) != 0:
         result[0] = data[0]['local_names']["ru"]
         result[1] = data[0]['lat']
         result[2] = data[0]['lon']

    return result



def main():
    city = input("Введите город: ").strip().capitalize()
    
    locate_city = get_city_coordinates(city, open_weather_token)
    if locate_city[0] != None:
        #  print(f"[+] Ваш город: {locate_city[0]} широта {locate_city[1]}, долгота {locate_city[2]}")
         get_weather(calc_lat = locate_city[1], calc_lon = locate_city[2], city = locate_city[0], open_weather_token = open_weather_token)
    else: print("Я не нашел Ваш город!")
    

if __name__ == "__main__":
    main()
