# Game of verbs
Проект создан для интегрирования DialogFlow в чат-ботов Telegram и VK.
![тг бот](https://github.com/RomanRVV/game_of_verbs/assets/129319859/06631afa-f5f2-433d-a1a3-585a3f437417)

Ссылки на группу [ВК](https://vk.com/club223682986) и [Телеграмм бота](https://t.me/gameofverbs_bot)

## Как установить
Для запуска скрипта вам понадобится Python 3.10

Скачайте код с GitHub. Затем установите зависимости

```sh
pip install -r requirements.txt
```
## Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` в репозитории и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

- `TG_TOKEN` — Telegram token ([инструкция по созданию бота и получению токена](https://way23.ru/%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%B1%D0%BE%D1%82%D0%B0-%D0%B2-telegram.html))
- `VK_TOKEN` — VK token группы ([инструкция](https://uchet-jkh.ru/i/gde-naxoditsya-token-gruppy-vkontakte/))
- `ADMIN_CHAT_ID` — Chat id администратора ботов (в этот чат будут приходить сообщения об ошибках)
- `PROJECT_ID` — id вашего проекта DialogFlow 

## Как запустить

Создайте интенты в [DialogFlow](https://dialogflow.cloud.google.com/) либо на сайте, либо используя скрипт 

```
python create_intent.py 
```

Также можно указать свой путь до файла

```
python create_intent.py --json_file phrases.json
```

Запуск вк и телеграмм ботов

```
python tg_bot.py
python vk_bot.py
```


## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
