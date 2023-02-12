from create import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from random import randint
from kb import kb_main_menu
import datetime

total = 200
difficulty_level = 1
max_step = 28

@dp.message_handler(commands=['start'])
async def mes_start(message: types.Message):
    dtn = datetime.datetime.now()
    botlogfile = open('Bot.log', 'a', encoding='UTF-8')
    print(dtn.strftime("%d-%m-%Y %H:%M"), 'Пользователь ' + message.from_user.first_name, message.from_user.id, 'написал: ' + message.text, file=botlogfile)
    botlogfile.close()
    await message.answer(f'Привет, {message.from_user.full_name}. Начинаем игру в конфеты"', reply_markup=kb_main_menu)

@dp.message_handler(commands=['help'])
async def mes_help(message: types.Message):
    dtn = datetime.datetime.now()
    botlogfile = open('Bot.log', 'a', encoding='UTF-8')
    print(dtn.strftime("%d-%m-%Y %H:%M"), 'Пользователь ' + message.from_user.first_name, message.from_user.id, 'написал: ' + message.text, file=botlogfile)
    botlogfile.close()
    await message.answer('/rules - правила игры\n/set новое количество - изменить количество конфет, лежащих на столе\n/step новое количество - изменить коичество конфет, которое можно взять за ход\n/difficult - поставить уровень сложности выше')

@dp.message_handler(commands=['rules'])
async def mes_rules(message: types.Message):
    global total
    global max_step   
    await message.answer(f'На столе лежит {total} конфет.\nЗа один ход можно забрать не более чем {max_step} конфет.\n Все конфеты оппонента достаются сделавшему последний ход.\nЕсли хочешь изменить количество конфет лежащих на столе, то напиши /set новое количество конфет.\nЕсли хочешь изменить максимальное количество конфет, которое можно взять, то напиши /step новое количество конфет.\nЕсли стало скучно играть, то поставь уровень повыше, написав /difficult')

# Изменение уровня сложности
@dp.message_handler(commands=['difficult'])
async def mes_dif(message: types.Message):
    dtn = datetime.datetime.now()
    botlogfile = open('Bot.log', 'a', encoding='UTF-8')
    print(dtn.strftime("%d-%m-%Y %H:%M"), 'Пользователь ' + message.from_user.first_name, message.from_user.id, 'написал: ' + message.text, file=botlogfile)
    botlogfile.close()
    global difficulty_level
    global total
    global max_step
    bot_step = total//(max_step + 1)
    total -= bot_step
    difficulty_level = 2
    await message.answer(f'Установлен высокий уровень сложности. Я возьму {bot_step}, осталось {total}')

# Изменения изначальных условий
@dp.message_handler(commands=['step'])
async def mes_step(message: types.Message):
    dtn = datetime.datetime.now()
    botlogfile = open('Bot.log', 'a', encoding='UTF-8')
    print(dtn.strftime("%d-%m-%Y %H:%M"), 'Пользователь ' + message.from_user.first_name, message.from_user.id, 'написал: ' + message.text, file=botlogfile)
    botlogfile.close()
    global total
    global max_step
    if len(message.text.split()) < 2:
        await message.answer(f'Ошибка в команде. Напиши /step и число. Например /step 20')
    else:
        temp = int(message.text.split()[1])
        if temp > 2:
            max_step = temp
            await message.answer(f'Теперь можно взять максимум {max_step} конфет за ход.')
        else:
            await message.answer('Слишком мало конфет.')

@dp.message_handler(commands=['set'])
async def mes_settings(message: types.Message):
    dtn = datetime.datetime.now()
    botlogfile = open('Bot.log', 'a', encoding='UTF-8')
    print(dtn.strftime("%d-%m-%Y %H:%M"), 'Пользователь ' + message.from_user.first_name, message.from_user.id, 'написал: ' + message.text, file=botlogfile)
    botlogfile.close()
    global total
    if len(message.text.split()) < 2:
        await message.answer(f'Ошибка в команде. Напиши /set и число. Например /set 100')
    else:
        count = int(message.text.split()[1])
        if count > 29:
            total = count
            await message.answer(f'Количество конфет установлено {total}.')
        else:
            await message.answer('Слишком мало конфет.')

@dp.message_handler()
async def mes_all(message: types.Message):
    dtn = datetime.datetime.now()
    botlogfile = open('Bot.log', 'a', encoding='UTF-8')
    print(dtn.strftime("%d-%m-%Y %H:%M"), 'Пользователь ' + message.from_user.first_name, message.from_user.id, 'написал: ' + message.text, file=botlogfile)
    botlogfile.close()
    global total
    global max_step
    if message.text.isdigit():
        global difficulty_level
        if max_step < int(message.text):
            await message.answer(f'Можно взять максимум {max_step} конфет')
        elif difficulty_level == 1:
            temp_total = total - int(message.text)
            if temp_total == 0:
                await message.answer(f'Осталось {temp_total} конфет. Ты выиграл!')
                total = 200
                difficulty_level = 1
                max_step = 28
            elif temp_total > max_step:
                bot_step = randint(1, max_step)
                total = temp_total - bot_step
                await message.answer(f'Осталось {temp_total} конфет. Я возьму {bot_step} конфет. На столе осталось {total} конфет')
            else:
                bot_step = randint(1, temp_total+1)
                total = temp_total - bot_step
                if total == 0:
                    await message.answer(f'Осталось {temp_total} конфет. Я возьму {bot_step}. Я выиграл')
                    total = 200
                    difficulty_level = 1
                    max_step = 28
                else:
                    await message.answer(f'Осталось {temp_total} конфет. Я возьму {bot_step}. На столе осталось {total} конфет')
        elif difficulty_level == 2:
            temp_total = total - int(message.text)
            if temp_total == 0:
                await message.answer(f'Осталось {temp_total} конфет. Ты выиграл!')
                total = 200
                difficulty_level = 1
                max_step = 28
            elif temp_total > max_step:
                bot_step = (max_step + 1) - int(message.text)
                total = temp_total - bot_step
                await message.answer(f'Осталось {temp_total} конфет. Я возьму {bot_step} конфет. На столе осталось {total} конфет')
            else:
                bot_step = temp_total
                await message.answer(f'Осталось {temp_total} конфет. Я возьму {bot_step}. Я выиграл')
                total = 200
                difficulty_level = 1
                max_step = 28
    else:
         await message.answer('Чтобы вызвать помощь, введите /help')