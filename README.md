# Пример работы
![Пример](https://github.com/popkovaleks/nl_recognizer_bot/blob/main/screenshots/Снимок%20экрана%202023-01-15%20в%2021.17.09.png?raw=true)

# Установка
Для запуска достаточно создать файл .env, в котором описаны переменные окружения.

Файл .env:
```
TELEGRAM_TOKEN=<токен телеграм бота>
PROJECT_ID=<id проекта google cloud>
GOOGLE_APPLICATION_CREDENTIALS=<путь до файла application_default_credentials>
VK_API_TOKEN=<токен сообщества vk>
TELEGRAM_TOKEN_LOGS=<бот для отправки логов>
TG_CHAT_ID=<идентификатор пользователя телеграма для получения логов>
```

## Токен telegram-бота
Для создания телеграм бота напишите боту [BotFather](https://t.me/BotFather), там вы создадите бота, и вам будет выдан токен бота.

## Токен бота сообщества вконтакте
Токен можно сгенерировать в меню управления сообщества на вкладке API

## Запуск
После заполнения файла с переменными можно запускать ботов с помощью команд
```
python3 telegram_bot.py
python3 vk_bot.py
```

## Тренировка бота
Натренировать бота можно с помощью скрипта create_intents.py, который запускается следующей командой
```
python3 create_intents.py --p [путь до файла json]
```
Пример файла для обучения бота по [ссылке](https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json)