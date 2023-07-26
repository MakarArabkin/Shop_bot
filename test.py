from aiogram import types
import json
from DB import DBConnection

db = DBConnection()

def welcome_message():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("🧥 Куртки 🧥"))
    keyboard.add(types.KeyboardButton("👟 Кроссовки 👟"))
    keyboard.add(types.KeyboardButton("🗑 Корзина 🗑"))
    return keyboard


def sneakers_buttons():

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=cb) for name, cb in
                       {f'🛍 Все модели 🛍': json.dumps({'M': 'ALL-MODEL'})}.items()])
    
    keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=cb) for name, cb in
                       {f'🔎 Поиск по размеру 🔎': json.dumps({'M': 'FIND-BY-SIZE'})}.items()])
    

    return keyboard

def orders():
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add(types.KeyboardButton('♻️ Отправить заказ ♻️'))
    keyboard.add(types.KeyboardButton('🔙Вернуться в главное меню'))
    return keyboard


def counters(m,page, count, flag):
    keyboard = types.InlineKeyboardMarkup(row_width=6)
    
    if flag == 'F' or flag == 'A':
            keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=cb) for name, cb in
                        {f'🛒 Добавить в корзину 🛒': json.dumps({'M': 'AD-TO-ORDER'})}.items()])
    elif flag == 'O':
        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=cb) for name, cb in
                    {f'❌ Удалить ❌': json.dumps({'M': 'DEL','PAGE': page, 'FLAG': flag})}.items()])

    if page != count and count > 1 and page > 1:
            
        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=cb) for name, cb in
                       {f'←': json.dumps({'M': 'COUNTER', 'PAGE': page-1, 'COUNT': count, 'FLAG': flag}),
                        f'{page}/{count}': json.dumps({'M': ' '}),
                        f'→': json.dumps({'M': 'COUNTER', 'PAGE': page+1, 'COUNT': count, 'FLAG': flag})}.items()])

    elif page == count and count > 1:

        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=cb) for name, cb in
                       {f'←': json.dumps({'M': 'COUNTER', 'PAGE': page-1, 'COUNT': count, 'FLAG': flag}),
                        f'{page}/{count}': json.dumps({'M': ' '})}.items()])               

    elif page == 1 and count != 1:

        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=cb) for name, cb in
                       {f'{page}/{count}': json.dumps({'M': ' '}),
                        f'→': json.dumps({'M': 'COUNTER', 'PAGE': page+1, 'COUNT': count, 'FLAG': flag})}.items()])
        
        
    if flag == 'F' or flag == 'A':
        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=cb) for name, cb in
                    {f'🔙 Вернуться в главное меню': json.dumps({'M': 'BACK-TO-MENU'})}.items()])
    elif flag == 'O' :
        size_order(m,keyboard,page,flag)
    return keyboard

def size_order(m,keyboard,page,flag):
    id = m.split("Артикул:")[-1].split("\n")[0].strip()

    si = m.split("Выбранные размеры:")[-1].split("\n")[0].strip().split(" ")

    text =[]

    for x in db.data['Sneakers']:
        if str(x['ID']) == id:
            for i,_ in enumerate(x['Size']):
                text.insert(i,str(_))
                for size_acept in si:
                    if size_acept == str(_):text.insert(i,'✅')
                
    print(text)

    for x in db.data['Sneakers']:
        if str(x['ID']) == id:
            for i,_ in enumerate(x['Size']):
                
                if i == 0 and text[i] != '✅' :
                    keyboard.row(*[types.InlineKeyboardButton(text=name, callback_data=cb) for name, cb in
                                {f'{text[i]}': json.dumps({'M': 'OR-SIZE','SIZE': _ , 'PAGE': page, 'FLAG': flag})}.items()])
                elif text[i] != '✅': 
                    keyboard.insert(*[types.InlineKeyboardButton(text=name, callback_data=cb) for name, cb in
                                {f'{text[i]}': json.dumps({'M': 'OR-SIZE','SIZE': _ , 'PAGE': page, 'FLAG': flag})}.items()])
                elif i == 0 and text[i] == '✅' :
                    keyboard.row(*[types.InlineKeyboardButton(text=name, callback_data=cb) for name, cb in
                                {f'{text[i]}': json.dumps({'M': 'DEL-SIZE','SIZE': _ , 'PAGE': page, 'FLAG': flag})}.items()])
                elif text[i] == '✅': 
                    keyboard.insert(*[types.InlineKeyboardButton(text=name, callback_data=cb) for name, cb in
                                {f'{text[i]}': json.dumps({'M': 'DEL-SIZE','SIZE': _ , 'PAGE': page, 'FLAG': flag})}.items()])

def size_show(all_size):
    keyboard = types.InlineKeyboardMarkup(row_width=len(all_size))

    for _ in range(len(all_size)):
        keyboard.insert(*[types.InlineKeyboardButton(text=name, callback_data=cb) for name, cb in
                       {f'{all_size[_]}': json.dumps({'M': 'SHOW-SIZE','SIZE': all_size[_]})}.items()])
        
    keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=cb) for name, cb in
                    {f'🔙 Назад ': json.dumps({'M': 'BACK-TO-MENU'})}.items()])
    
    return keyboard