# WeatherBot
Телеграм бот для узнавания погоды (https://t.me/senchweatherbot). Для получения данных о погоде используется Weather API
от OpenWeatherMap (https://openweathermap.org/api). На данный момент у бота есть 6 команд: 

/weather <город> - возвращает подробную информацию о погоде в указанном городе в данный момент

![](/screenshots/screenshot_1.png?raw=true "Скриншот1")

/forecast <город> - возвращает краткий прогноз погоды на каждые 3 часа на ближайшие 5 дней 

![](/screenshots/screenshot_2.png?raw=true "Скриншот2")

/weatherattime <город> <время> - возвращает подробную информацию о погоде в указанном городе в указанный момент времени 

![](/screenshots/screenshot_3.png?raw=true "Скриншот3")

Время в этом случае можно указывать в произвольном читаемом формате

![](/screenshots/screenshot_4.png?raw=true "Скриншот4")

Нельзя получить информацию о погоде дальше чем на 5 дней вперед

![](/screenshots/screenshot_5.png?raw=true "Скриншот5")

/addcity <город> - добавление города в любимые

![](/screenshots/screenshot_6.png?raw=true "Скриншот6")

/favoritecity - получение любимого города

![](/screenshots/screenshot_7.png?raw=true "Скриншот7")

/removecity - удаление любимого города

![](/screenshots/screenshot_8.png?raw=true "Скриншот8")