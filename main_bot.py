import json
import test

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram import types
from DB import DBConnection
from states import *






TOKEN = ""
bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())
db = DBConnection()


@dp.message_handler(commands=['start'])
async def welcome_message(m):
    first_name = m.chat.first_name
    await bot.send_message(m.chat.id, f"Привет, {first_name} ! Я тестовый бот для тебя",    reply_markup=test.welcome_message())


@dp.message_handler(content_types=['text'])
async def Main_menu(m: types.Message):
    print(m.chat.id)
    if not str(m.chat.id) in db.orders["Change Orders"]:
        db.orders["Change Orders"][str(m.chat.id)] = []
        db.update_order()

    if m.text == "Привет":
        await bot.send_message(m.chat.id, "Привет, чем я могу тебе помочь?")

    elif m.text == "👟 Кроссовки 👟":
        await bot.send_photo(m.chat.id, db.picture_menu,caption="Что конкретно вас интересует?",
                               reply_markup=test.sneakers_buttons())

    elif m.text == "🧥 Куртки 🧥": 
        rand_meme = "https://sun9-east.userapi.com/sun9-17/s/v1/ig2/4qBrzGackWYVTaQV8cCxmaHgMUtY9zQ5fRBM00haoK5wVrEASitf4JgjMgCQiMjzD6MCUNVdVsD8cpsHc-dph-xV.jpg?size=1000x1000&quality=95&type=album"
        await bot.send_photo(m.chat.id, rand_meme, caption='К сожалению, этот раздел еще в разработке')

    elif m.text == "🗑 Корзина 🗑":
        if  db.orders['Change Orders'][str(m.chat.id)] == []:
            await bot.send_message(m.chat.id, text="Ваша корзина ПУСТА", reply_markup=test.orders())
        else:
            await bot.send_message(m.chat.id, text="Ваша корзина", reply_markup=test.orders())
            flag = 'O'
            first_massage = True
            page = 1
            await show_sneakers(m, page ,first_massage,flag) 

    elif m.text == "🔙Вернуться в главное меню":
        await bot.send_message(m.chat.id, text="Главное меню", reply_markup=test.welcome_message())
    
    elif m.text == '♻️ Отправить заказ ♻️':
        await bot.send_message(m.chat.id, text="Ваш заказ отправлен", reply_markup=test.welcome_message())

async def show_sneakers(m, page,flag_first_massage,flag_find):
    print(f"show_all_sneakers")
    index = page - 1

    if flag_find == 'F':base_show = db.base_find['Sneakers_find']
    elif flag_find == 'O': base_show = db.orders['Change Orders'][str(m.chat.id)]
    elif flag_find == 'A': base_show = db.data['Sneakers']

    if flag_find == 'F' or flag_find == 'A': size_text = 'Размерный ряд:'
    elif flag_find == 'O': size_text = 'Выбранные размеры:'

    picture = base_show[index]['Picture']
    name = base_show[index]['Name']
    size_show = ""
    id = base_show[index]['ID']
    price = base_show[index]['Price']

    for j in range(len(base_show[index]['Size'])):
        size_show += " "+ str(base_show[index]['Size'][j])
    
    text = f"Наименование: {name}\
            \n{size_text} {size_show}\
            \nАртикул: {id}\
            \nЦена: {price}"
    
    if flag_first_massage:
        await bot.send_photo(m.chat.id, picture, caption = text,
                             reply_markup=test.counters(text,page,len(base_show),flag_find))
    else:
        update_massage = types.InputMedia(media=picture, caption=text)
        await m.edit_media( media= update_massage ,reply_markup=test.counters(text,page,len(base_show),flag_find))

@dp.callback_query_handler()
async def callback(callback_query: types.CallbackQuery):
    m = callback_query.message
    data = json.loads(callback_query.data)
    method = data['M']
    
    if method == 'COUNTER':
        first_massage = False
        await show_sneakers(m, data['PAGE'],first_massage,data['FLAG'])

    elif method == 'ALL-MODEL':
        flag = 'A'
        first_massage = False
        page = 1
        await show_sneakers(m, page ,first_massage,flag)
    elif method == 'FIND-BY-SIZE':
        print("Find_By_size")
        await bot.edit_message_caption(chat_id=m.chat.id,message_id=m.message_id,caption=f'Доступные размеры {all_size()}',reply_markup=test.size_show(all_size()))
    elif method == 'BACK-TO-MENU':
        await bot.edit_message_media(chat_id=m.chat.id, message_id=m.message_id, media=types.InputMediaPhoto(db.picture_menu))
        await bot.edit_message_caption(chat_id = m.chat.id,message_id=m.message_id,caption='Что конкретно вас интересует?',
                                    reply_markup=test.sneakers_buttons())
    elif method == 'SHOW-SIZE':
        print("Show_size")
        size = data['SIZE']
        find_fill(size)
        flag = 'F'
        first_massage = False
        page = 1
        await show_sneakers(m, page ,first_massage,flag) 

    elif method == 'AD-TO-ORDER':
        print("AD-TO-ORDER")
        name = m.caption.split("Наименование:")[-1].split("\n")[0].strip()
        ad_to_order(m)
        await callback_query.answer(text = name + " 👟 \n" + "Добавлено в корзину 🎁",show_alert=True)

    elif method == 'DEL':

        id = m.caption.split("Артикул:")[-1].split("\n")[0].strip()

        for i,x in enumerate(db.orders['Change Orders'][str(m.chat.id)]):
            if str(x['ID']) == id:
                db.orders['Change Orders'][str(m.chat.id)].pop(i)
                break
                
        db.update_order()

        if  db.orders['Change Orders'][str(m.chat.id)] == []:

            await callback_query.answer(text = "Корзина пуста",show_alert=True)
            await bot.delete_message(chat_id = m.chat.id, message_id = m.message_id)

        else:

            first_massage = False
            page = 1
            await show_sneakers(m, page ,first_massage,data['FLAG']) 

    elif method == 'OR-SIZE':

        db.orders['Change Orders'][str(m.chat.id)][data['PAGE']-1]['Size'].append(data['SIZE'])
        db.update_order()
        first_massage_1 = False
        await show_sneakers(m, data['PAGE'],first_massage_1,data['FLAG'])
    elif  method == 'DEL-SIZE':
        db.orders['Change Orders'][str(m.chat.id)][data['PAGE']-1]['Size'].remove(data['SIZE'])
        db.update_order()
        first_massage_1 = False
        await show_sneakers(m, data['PAGE'],first_massage_1,data['FLAG'])
    else:
        print("Необработанный процесс")

def all_size():
    base_parsing = db.data['Sneakers']
    all_size_list = []
    for _ in range(len(base_parsing)):
        all_size_list.extend(base_parsing[_]['Size'])
    sort_list = sorted(list(set(all_size_list)))
    return(sort_list)

def ad_to_order(m):

    id = m.caption.split("Артикул:")[-1].split("\n")[0].strip()
        
    if str(m.chat.id) in db.orders["Change Orders"]:
        for x in db.data["Sneakers"]:
            if str(x['ID']) == id:
                print(x)
                db.orders["Change Orders"][str(m.chat.id)].append(x)
                db.orders["Change Orders"][str(m.chat.id)][-1]["Size"] = []
    else:
        print("ERROR")

    db.update_order()

def create_oder(m):
    db.cls_order(m)
    base_order_id = db.base_order_id['Orders'][m.chat.id]
    print(base_order_id)
    base_parsing = db.data['Sneakers']
    for i in range(len(base_order_id)):
        for _ in range(len(base_parsing)):
            if base_parsing[_]['ID'] == base_order_id[i]:
                db.order['Sneakers_order'][m.chat.id].append(base_parsing[_])

def find_fill(size):
    db.cls_find()
    base_parsing = db.data['Sneakers']
    for _ in range(len(base_parsing)):
        if size in base_parsing[_]['Size']:
            db.base_find['Sneakers_find'].append(base_parsing[_])
        
if __name__ == "__main__":
    loopa = dp.loop
    executor.start_polling(dp)
