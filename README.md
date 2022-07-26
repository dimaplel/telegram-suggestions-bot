# Suggestions Bot - Telegram 🇬🇧

[_Версія українською 🇺🇦_](github.com/dimaplel/telegram-suggestions-bot#suggestions-bot---telegram--1)

Bot was created originally for IASA Student Council to handle suggestions, questions and requests. However, you can 
freely fork this repository and create your own bot.

## How bot works

1. User sends a message to the bot
2. Bot forwards the message to the chat
3. Chat participant replies to the forwarded message
4. Bot copies the answer and sends it to user

## Features

- __Text, Photos, Videos, Documents, GIFs, Voice Messages__ and __Geolocation__ are supported
- Customisable messages for bot to answer
- Ban/unban users using reply
- Messages editing. Changes would be displayed in private/group chat

> ❗ __Note: changing pictures/videos is not possible, only their captions__

### Banning/unbanning

To ban spamming/unfriendly users, you should reply on forwarded from user message like this: `/ban` or like this: `/ban <reason>`, 
where the reason will be displayed to user if he would try to send something again. Then, bot will reply to you whether 
it was successful or not.

In contrast, to unban users, you should reply on user's message with `/unban` and bot will notify on command success 
or failure.

### Message editing

Message editing is implemented using SQL table. When a message is being sent - bot inserts original message id and
forwarded message id into SQL table. For place optimisation in the table a script was written, which deletes row 
after some time passes. You can copy script from
[`sql_script.txt`](https://github.com/dimaplel/telegram-suggestions-bot/blob/main/sql_script.txt). To configure time 
interval after which a row is being deleted, `INTERVAL '<interval>'` should be set  according to time standards in SQL.

## Config

To setup a bot for your own usage, you should specify those variables in 
[`config.py`](https://github.com/dimaplel/telegram-suggestions-bot/blob/main/config.py).

``` bash
# Bot Data
TOKEN = # your bot's token
CHAT_ID = # chat id where the bot will forward users' messages

# Database Data
HOSTNAME = # host of sql database
DATABASE = # database name
USERNAME = # username to log in
PORT_ID = # port to connect to database
DB_PASS = # password to access database
```

To change default text to your custom, redefine values of the dictionary for each phrase in 
[`config.py`](https://github.com/dimaplel/telegram-suggestions-bot/blob/main/config.py).

``` bash
# Predefined text to send
TEXT_MESSAGES = {
    'start': 'Welcome to Suggestions Bot 👋 \n\n Please, send your message and we will process your request.',
    'message_template': '<i>Message from: <b>@{0}</b>.</i>\n\n{1}<b>id: {2}</b>',
    'is_banned': '❌ User is banned!', 'has_banned': '✅ User has been successfully banned!',
    'already_banned': '❌ User is already banned!', 'has_unbanned': '✅ User has been successfully un-banned!',
    'not_banned': '❌ There is no such user in the ban list!',
    'user_banned': '🚫 You cannot send messages to this bot!',
    'user_unbanned': '🥳 You have proven your innocence, and now you can write to this bot again!',
    'user_reason_banned': '🚫 You cannot send messages to this bot due to the reason: <i>{}</i>.',
    'pending': 'Thank you for your request! We are already into processing it.',
    'unsupported_format': '❌ Format of your message is not supported and it will not be forwarded.',
    'message_not_found': '❌ It looks like your message was sent more that a day ago. Message to edit was not found!',
    'message_was_not_edited': '❌ Unfortunately you cannot edit images/videos themselves.'
                              'Please, send a new message.',
    'reply_error': '❌ Please, reply with /ban or /unban only on forwarded from user messages!'
}
```

## Installation guide

1. Clone this repository using terminal or tools in your IDE: 
`https://github.com/dimaplel/telegram-suggestions-bot.git`
2. Change directory in terminal `cd $repository-direcory`
3. Download requirements `pip install -r requirements.txt`
4. Edit and update [`config.py`](https://github.com/dimaplel/telegram-suggestions-bot/blob/main/config.py)
5. Create a new routine operator in your SQL database and insert script from 
[`sql_script.txt`](https://github.com/dimaplel/telegram-suggestions-bot/blob/main/sql_script.txt) so that database 
could delete rows by itself after some time. By the way, don't forget to configure SQL user instead of `<user>` tag
6. Run the bot `python bot.py` or by deploying it to [__Heroku__](https://heroku.com/deploy)

## Authors

* [Dmytro Ivanenko](https://github.com/dimaplel)
* [Nikita Ryabin](https://github.com/akaspeh)

***
# Suggestions Bot - Telegram 🇺🇦

Початково, бот був створений для СтудРади ІПСА для обробки пропозицій, питань та запитів. Однак ви легко можете форкати 
даний репозиторій і кастомізувати його під свої потреби.

## Як працює бот

1. Користувач надсилає повідомлення боту
2. Бот пересилає повідомлення в чат
3. Учасник чату відповідає на переслане повідомлення
4. Бот копіює відповідь і надсилає її користувачеві

## Особливості

- Підтримуються __Текст, Зображення, Відео, Документи, Гіфки, Голосові Повідомлення__ та __Геолокація__
- Кастомізація стандартних відповідей бота на трігери або команди
- Бан/розбан користувачів за допомогою відповіді на повідомлення
- Редагування повідомлень. Зміни відображатимуться в приватному/груповому чаті

> ❗ __Примітка: змінити зображення/відео неможливо, лише підпис__

### Бан/розбан

Для того, щоб забанити користувачів, що спамлять або поводять себе непривітно, ви маєте відповісти на повідомлення 
користувача так: `/ban` або так: `/ban <причина>`, де причина відобразиться, якщо цей користувач знову спробує щось 
надіслати. Потім, бот відповість статусом виконання операції.

На противагу, щоб розбанити користувача, потрібно відповісти на повідомлення користувача `/unban`, і бот відповість, що 
команда виконалась успішно чи невдало.

### Редагування повідомлень

Редагування повідомлень реалізовано за допомогою SQL таблиці. Коли присилається повідомлення - бот вставляє
в таблицю id оригінального повідомлення та id пересланого повідомлення. Задля оптимізації місця у таблиці було 
написано скрипт, який видаляє рядок через деякий час (перевірка на час здійснюється, коли новий елемент додається
до таблиці). Детально ознайомитися з ним та скопіювати можна з
[`sql_script.txt`](https://github.com/dimaplel/telegram-suggestions-bot/blob/main/sql_script.txt). 
За час для видалення відповідає значення `INTERVAL '<interval>'`, який оформлюється згідно з форматом часу SQL.

## Config

Для того, щоб налаштувати бота для власного використання, потрібно вказати наступні змінні в 
[`config.py`](https://github.com/dimaplel/telegram-suggestions-bot/blob/main/config.py)

``` bash
# Bot Data
TOKEN = # токен вашого бота
CHAT_ID = # id чату, куди бот пересилатиме повідомлення від користувачів

# Database Data
HOSTNAME = # хост бази даних sql
DATABASE = # ім'я бази данних
USERNAME = # username для входу в базу даних
PORT_ID = # порт для з'єднання з базою даних
DB_PASS = # пароль для бази даних
```

Для того, щоб змінити стандартний текст відповідей бота на ваш власний, змініть значення в словнику для кожної фрази в 
[`config.py`](https://github.com/dimaplel/telegram-suggestions-bot/blob/main/config.py)

``` bash
# Predefined text to send
TEXT_MESSAGES = {
    'start': 'Ласкаво просимо 👋\n\nНапишіть своє запитання / пропозицію, і ми відповімо Вам найближчим часом.',
    'message_template': '<i>Повідомлення від: <b>@{0}</b>.</i>\n\n{1}<b>id: {2}</b>',
    'is_banned': '❌ Користувач забанений!', 'has_banned': '✅ Користувач був успішно забанений!',
    'already_banned': '❌ Користувач уже забанений!', 'has_unbanned': '✅ Користувач був успішно розбанений!',
    'not_banned': '❌ Такого користувача немає в бан-лісті!',
    'user_banned': '🚫 Ви більше не можете писати в бот пропозицій!',
    'user_reason_banned': '🚫 Ви більше не можете писати в бот пропозицій через причину: <i>{}</i>.',
    'user_unbanned': '🥳 Сама благодать зійшла з небес, і тепер ви знову можете писати до боту пропозицій!',
    'pending': 'Дякуємо за ваше звернення. Ми вже оброблюємо Ваш запит!',
    'unsupported_format': '❌ Формат вашого повідомлення не підтримується, воно не буде переслане.',
    'message_not_found': '❌ Схоже, що ви відправляли повідомлення більше трьох діб тому, повідомлення не було знайдено!'
    , 'message_was_not_edited': '❌ На жаль не можна редагувати зображення в повідомленнях. '
                                'Будь ласка, надішліть нове зображення',
    'reply_error': '❌ Будь-ласка, давайте відповідь /ban або /unban лише на переслані від користувачів повідомлення!'
}
```

## Керівництво по встановленню

1. Зклонуйте репозиторій за допомогою терміналу або інструментів у вашій IDE: `https://github.com/dimaplel/telegram-suggestions-bot.git`
2. Змініть папку в терміналі `cd $repository-directory`
3. Встановіть вимоги `pip install -r requirements.txt`
4. Відредагуйте та оновіть [`config.py`](https://github.com/dimaplel/telegram-suggestions-bot/blob/main/config.py)
5. Створіть новий routine operator у вашій базі даних SQL та вставте скрипт з 
[`sql_script.txt`](https://github.com/dimaplel/telegram-suggestions-bot/blob/main/sql_script.txt), щоб база даних самостійно 
видаляла рядки таблиці після деякого часу. До речі, не забудьте зазначити користувача в базі даних замість тегу `<user>`
6. Запустіть бота локально `python bot.py` або за допомогою [__Heroku__](https://heroku.com/deploy)

## Автори

* [Дмитро Іваненко](https://github.com/dimaplel)
* [Нікіта Рябін](https://github.com/akaspeh)
