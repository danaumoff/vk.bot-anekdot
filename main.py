# TO DO:
# 1. Покупка видеокарт (не сделано)
# 2. Попробовать сделать донаты (если успеем) (не сделано)
# 

from webbrowser import get
from pyowm import OWM
import vk_api
import random
import json
from pyowm.utils.config import get_config_from
import sqlite3

connect = sqlite3.connect("data.db")
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vk_id VARCHAR(32) UNIQUE,
    name VARCHAR(64),
    surname VARCHAR(64),
    money INTEGER(11)
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS gpus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(64) UNIQUE,
    click_m INTEGER(11),
    price INTEGER(11)
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS users_gpus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER(11),
    gpu_id INTEGER(11)
    )""")

def insert_user_sql(vk_id,):
    global connect
    global cursor
    vk_info = vk.method("users.get", {"user_ids": int(vk_id)})
    name = vk_info[0].get('first_name')
    surname = vk_info[0].get('last_name')
    cursor.execute("""INSERT INTO users (vk_id, name, surname, money) VALUES (?, ?, ?, ?)""", [
                   vk_id, name, surname, 0])
    connect.commit()


def add_money(vk_id, money):
    global connect
    global cursor
    cursor.execute(
        """UPDATE users SET money = money + ? WHERE vk_id = ?""", [money, vk_id])
    connect.commit()


def get_money(vk_id):
    global connect
    global cursor
    cursor.execute("""SELECT money FROM users WHERE vk_id = ?""", [vk_id])
    money = cursor.fetchone()
    connect.commit()
    return money[0]


def get_top():
    global connect
    global cursor
    cursor.execute(
        """SELECT name, surname, money FROM users ORDER BY money DESC LIMIT 3""")
    result = cursor.fetchall()
    connect.commit()
    return result

def add_coins(vk_id, money):
    global connect
    global cursor
    cursor.execute("""UPDATE users SET money = money + ? WHERE vk_id = ?""", [money, vk_id])
    connect.commit()

def get_gpus():
    global connect
    global cursor
    cursor.execute("""SELECT name FROM gpus""")
    gpus = cursor.fetchall()
    return gpus

def gpus_list():
    gpus = get_gpus()
    result = []
    for gpu in gpus:
        result.append(gpu[0])
    return result


def add_gpus_to_db():
    global connect
    global cursor
    reserv_gpus = [["GTX 1080 TI", 5, 100], ["RTX 2060 TI", 20, 500], ["RTX 3090 TI", 100, 3000], ["SUPER-CRYPTO ELON MUSK VIDEOCARD", 2000, 100000]]
    for gpu in reserv_gpus:
        cursor.execute("""INSERT INTO gpus (name, click_m, price) VALUES (?, ?, ?)""", [
        gpu[0], gpu[1], gpu[2]])
    connect.commit()


# ---SETTINGS VK---#
token = "ba9f6c1f234bbd5fad965b35349f008409a151276872cf8a79345024711f66863d72f5d2c9ec6f661a80c"  # api-key
vk = vk_api.VkApi(token=token)
vk._auth_token()
# ---SETTINGS VK---#


def get_button(label, color, payload=''):  # функция вызова клавиатуры
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }


keyboard = {"one_time": False, "buttons": [[get_button(label="Анекдот", color="positive")], [get_button(
    label="Команды", color="positive")], [get_button(label="Симулятор майнера", color="primary")]]}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))
keyboard1 = {"one_time": False, "buttons": [[get_button(label="Анекдот", color="primary")], [get_button(label="Привет", color="primary")], [
    get_button(label="Погода", color="primary")], [get_button(label="Симулятор майнера", color="primary")]]}
keyboard1 = json.dumps(keyboard1, ensure_ascii=False).encode('utf-8')
keyboard1 = str(keyboard1.decode('utf-8'))
keyboard2 = {"one_time": False, "buttons": [
    [get_button(label="Выключить бота", color="negative")]]}
keyboard2 = json.dumps(keyboard2, ensure_ascii=False).encode('utf-8')
keyboard2 = str(keyboard2.decode('utf-8'))
keyboard3 = {"one_time": False, "buttons": [[get_button(label="+ 1 Сатоши", color="positive")], [get_button(
    label="Показать счёт", color="primary")], [get_button(label="Топ игроков", color="primary")],[get_button(label="Видеокарты", color="primary")]]}
keyboard3 = json.dumps(keyboard3, ensure_ascii=False).encode('utf-8')
keyboard3 = str(keyboard3.decode('utf-8'))
keyboardgpu = {"one_time": False, "buttons": []}
for gpu in get_gpus():
    keyboardgpu["buttons"].append([get_button(label=gpu[0], color="positive")])
keyboardgpu = json.dumps(keyboardgpu, ensure_ascii=False).encode('utf-8')
keyboardgpu = str(keyboardgpu.decode('utf-8'))



jokes = ['— Почему ваши дети все время ссорятся? — Kонфликт версий, — отвечает программист.',
         'Для программиста монитор — это реальный рабочий стол, системный блок — журнальный, а клавиатура — обеденный.',
         'Один программист другому: — Вот представь:  — У тебя есть 1000 рублей... Или, для круглого счета, пусть у тебя 1024.',
         'Зовет директор к себе программистов и сисадмина. — Какая сволочь удалила мой доступ к сети! Уволю нафиг! — ???? — Еще раз спрашиваю — кто удалил? Сисадмин:  — Я не удалял... Программисты:  — Мы тоже не удаляли! — Тогда объясните мне, что это? Вот папка "Сетевые подключения", видите? А вот значок — "Удаленный доступ к сети"... Последний раз спрашиваю — по—хорошему — КТО УДАЛИЛ???!!!б',
         'Работа программиста и шамана имеет много общего — оба бормочут непонятные слова, совершают непонятные действия и не могут объяснить, как оно работает.',
         'Первый урок английского. Учительница: — Кто из вас, дети, знает все английские буквы. Вовочка (программист маленький): — Я. — Hу называй, по порядку. — Q, W, E, R, T, Y...',
         'Встречаются два бывших одноклассника. Один — новый русский, а другой — программист. Первый спрашивает второго: — Ну что, братан, как дела? — Да вот, уже почти год сижу на Яве, пишу всякие приложения. — Ну ты крут! Впрочем, я тоже в этом году на Кипре две недели пробыл.',
         'Блондинка спрашивает программиста: — И что делать с этой программой? — Установи и крякни. — Установила и крякнула ничего не работает. — Ты как крякала? — Как уточка.',
         'Жена посылает мужа-программиста в магазин: - Купи батон колбасы. Да, и спроси, есть ли яйца. Если есть - возьми десяток. Программист приходит в магазин: - Батон колбасы, пожалуйста. Ага, спасибо. А яйца у вас в продаже есть? - Есть. - Тогда, пожалуйста, ещё девять батонов колбасы.'
         ]


def get_weather(city):
    try:
        owm = OWM('75b6b6bf8c7775c44dc00cb28f622ea8')
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(city)
        w = observation.weather
        t = w.temperature('celsius')
        t1 = t['temp']
        t2 = t['feels_like']
        st = w.status
        if st == 'Rain':
            st = 'дождь'
        elif st == 'Clouds':
            st = 'облачно'
        elif st == 'Snow':
            st = 'снег'
        elif st == 'Fog' or st == 'Mist':
            st = 'туман'
        elif st == "Clear":
            st = 'ясно'
        elif 'light' in st:
            wth = st.split()[1]
            if wth == 'rain':
                st = 'слабый дождь'
            if wth == 'snow':
                st = 'слабый снег'
        else:
            st = st + "(ещё не переведено)"
        ans = "В городе/стране {0} {1}, температура {2}, ощущается как {3}".format(
            city, st, t1, t2)
        return ans
    except Exception as e:
        return "Проверьте правильность написания региона"


print(gpus_list())


def exit_bot():
    exit()


def main():
    while True:
        messages = vk.method("messages.getConversations", {
                             "offset": 0, "count": 20, "filter": "unanswered"})
        if messages["count"] >= 1:
            id = messages["items"][0]["last_message"]["from_id"]
            user_word = messages["items"][0]["last_message"]["text"].lower()
            if user_word == "привет":
                vk.method("messages.send", {"peer_id": id, "message": "Привет!",
                          'keyboard': keyboard, "random_id": random.randint(1, 2147483647)})
            elif user_word == "анекдот":
                joke = jokes[random.randint(0, len(jokes))]
                vk.method("messages.send", {
                          'peer_id': id, "message": joke, 'keyboard': keyboard, 'random_id': random.randint(1, 2147483647)})
            elif 'погода' in user_word:
                try:
                    city = user_word.split()[1]
                    vk.method("messages.send", {'peer_id': id, "message": get_weather(
                        city), 'keyboard': keyboard, 'random_id': random.randint(1, 2147483647)})
                except Exception:
                    vk.method("messages.send", {'peer_id': id, "message": "Введите команду в виде 'погода <название_города>'",
                              'keyboard': keyboard, 'random_id': random.randint(1, 2147483647)})
            elif user_word == "команды":
                vk.method("messages.send", {'peer_id': id, "message": "погода <название_города>\nАнекдот\nПривет",
                          'keyboard': keyboard1, 'random_id': random.randint(1, 2147483647)})
            elif user_word == "симулятор майнера":
                try:
                    insert_user_sql(id)
                except:
                    pass
                vk.method("messages.send", {'peer_id': id, "message": "Добро пожаловать в симулятор майнера",
                          'keyboard': keyboard3, 'random_id': random.randint(1, 2147483647)})
            elif user_word == "+ 1 сатоши":
                try:
                    insert_user_sql(id)
                except:
                    pass
                add_money(id, 1)
                vk.method("messages.send", {"peer_id": id, "message": "Вам начислено 1 сатоши",
                          'keyboard': keyboard3, "random_id": random.randint(1, 2147483647)})
            elif user_word == "показать счёт":
                vk.method("messages.send", {"peer_id": id, "message": "Счёт: "+str(get_money(
                    id)), 'keyboard': keyboard3, "random_id": random.randint(1, 2147483647)})
            elif user_word == "видеокарты":
                vk.method("messages.send", {"peer_id": id, "message": "Выбор видеокарт", 'keyboard': keyboardgpu, "random_id": random.randint(1, 2147483647)})
            # elif user_word in get_gpus()
            elif "добавить" in user_word:
                money = int(user_word.split()[1])
                add_coins(id, money)
                vk.method("messages.send", {"peer_id": id, "message": "OKEY", "random_id": random.randint(1, 2147483647)})
            elif user_word == "топ игроков":
                msg = "ТОП ИГРОКОВ:\n"
                top = get_top()
                for i in range(0, len(top)):
                    msg += top[i][0] + " " + top[i][1] + \
                        " -- " + str(top[i][2]) + " сатоши\n"
                vk.method("messages.send", {
                          "peer_id": id, "message": msg, 'keyboard': keyboard3, "random_id": random.randint(1, 2147483647)})
            else:
                vk.method("messages.send", {"peer_id": id, "message": "Я тебя не понимаю",
                          'keyboard': keyboard, "random_id": random.randint(1, 2147483647)})


try:
    main()
except Exception:
    main()
