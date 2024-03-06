# Tomato bot

Телеграм бот для відбору до IT відділу

## Запускаємо через Docker
 - Встановлюємо Docker
 - До файлу [.env](.env) записати телеграм токен
 - Будуємо контейнер та запускаємо його
``` shell
docker build -t tomato_bot .
docker run -it --rm tomato_bot
```

## Запускаємо без Docker
 - До файлу [.env](.env) записати телеграм токен
 - підтягуємо бібліотеки
````shell
pip install -r requirements.txt
````
 - запускаємо бота
```shell
python .\tomato_bot\main.py
```