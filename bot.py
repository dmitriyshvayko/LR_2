from aiogram import Bot, Dispatcher,types,executor
import random

TOKEN = '5855661042:AAFe5y1pcUCySxO44QTMUnKVMNmUS2k1cKI'

bot = Bot(token=TOKEN)
dp  = Dispatcher(bot)

attempts = 5

users = {}

def rand():
    return random.randint(1,100)


@dp.message_handler(commands=['start'])
async def start(message:types.Message):
    await message.answer('Это игра Угадай число.\nПравила и доступные команды - \n/help')

    await bot.send_animation(message.chat.id ,r"https://media.tenor.com/Rem6iMDIaYMAAAAC/papich-arthas.gif")

    if message.from_user.id not in users:
        users[message.from_user.id] = {'state': False,
                                       'number': None,
                                       'attempts': None,
                                       'total_games': 0,
                                       'wins': 0}

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer('Правила игры:\nЯ загадываю число от 1 до 100,'
                         f'а вам нужно его угадать за {attempts} ' 
                         'попыток.\n\nДоступные команды:\n/help - правила '
                         'игры и список команд\n/cancel - выйти из игры\n'
                         '/stat - посмотреть статистику\n/go - начать игру'
                        )


@dp.message_handler(commands=['stat'])
async def stat(message: types.Message):
    await message.answer(f'Total games - {users[message.from_user.id]["total_games"]}\n'
                         f'Wins - {users[message.from_user.id]["wins"]}'
                        )


@dp.message_handler(commands=['cancel'])
async def cancel(message: types.Message):
     if users[message.from_user.id]["state"]:
         await message.answer("Теперь ты не играешь.Сыграть еще раз - /go")
         users[message.from_user.id]["state"] = False
     else:
        await message.answer("Ты и так не играешь,дружище!")


@dp.message_handler(commands=['go'])
async def go(message: types.Message):
    if not users[message.from_user.id]["state"]:
        users[message.from_user.id]["state"] = True
        users[message.from_user.id]["number"] =  rand()
        users[message.from_user.id]["attempts"] = attempts

        await message.answer("Игра началась!Попробуй угадать число")

    else:
        await message.answer("Ты и так играешь,дружище!")
        

def numb_filter(message : types.Message):
    return (message.text.isdigit()) and (1 <= int(message.text) <= 100)


@dp.message_handler(numb_filter)
async def game(message: types.Message):
    if users[message.from_user.id]["state"]:
        if int(message.text) == users[message.from_user.id]["number"]:
            await message.answer("Поздравляю,ты угадал!")

            await bot.send_animation(message.chat.id ,r"https://media.tenor.com/dnTNlgOnLzsAAAAC/%D0%BF%D0%B0%D0%BF%D0%B8%D1%87-dance.gif")

            users[message.from_user.id]["wins"] += 1
            users[message.from_user.id]["total_games"] += 1
            users[message.from_user.id]["state"] = False

            await message.answer("Еще раз сыграть - /go\n"
                                 "Посмотреть статистику - /stat")

        if int(message.text) < users[message.from_user.id]["number"]:
            await message.answer("Загаданное число больше /\ ")
            users[message.from_user.id]["attempts"] += -1
            await message.answer(f"Оставшееся число попыток - {users[message.from_user.id]['attempts']}")

        if int(message.text) > users[message.from_user.id]["number"]:
            await message.answer("Загаданное число меньше \/ " )
            users[message.from_user.id]["attempts"] += -1
            await message.answer(f"Оставшееся число попыток - {users[message.from_user.id]['attempts']}")

        if users[message.from_user.id]["attempts"] == 0:
            await message.answer("Попытки закончились.ТЫ проиграл\n"
                                 f'Загаднное число - {users[message.from_user.id]["number"]}\n'
                                 "Еще раз сыграть - /go\n"
                                 "Посмотреть статистику - /stat")
            await bot.send_animation(message.chat.id ,r"https://media.tenor.com/iBU7ZHKt8vUAAAAd/papich.gif")

            users[message.from_user.id]["total_games"] += 1
            users[message.from_user.id]["state"] = False
    else:
        await message.answer("Мы еще не начали.Для начала игры напишите - /go")

    
@dp.message_handler()
async def send_echo(message: types.Message):
    await message.answer("ЧЕЕЕЕГО???"
                         "/help - доступные команды"
                         )
    await bot.send_animation(message.chat.id ,r"https://media.tenor.com/fzUs9BbFLi8AAAAd/papich-%D0%BF%D0%B0%D0%BF%D0%B8%D1%87.gif")

executor.start_polling(dp,skip_updates = True)
