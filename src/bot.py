import os
import logging
import yaml
from copy import deepcopy
from croniter import croniter
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from datetime import date, datetime
from aiogram import Bot, Dispatcher, executor, types

from models import Config


TOKEN = os.environ.get('TG_BOT_TOKEN')
params = yaml.safe_load(open('conf/params.yaml', 'r'))
conf = Config(**params)
job_schedule = conf.bot.job_schedule.dict()
msg_start = conf.bot.start_message

logging.basicConfig(level=logging.INFO, 
                    filename=conf.paths.log_path, 
                    format="%(asctime)s [%(threadName)s] [%(levelname)s]  %(message)s")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


def get_next_schedule(js):
    tmp = deepcopy(js)
    base = datetime.now()
    for key in ['minute','hour','day','month']:
        if key not in tmp:
            tmp[key] = '*'
    cron_template = '{minute} {hour} {day} {month} *'.format(**tmp)
    dt_scheduled = croniter(cron_template, base).get_next(datetime)

    return dt_scheduled


@dp.message_handler(commands=['start', 'help'])
async def process_start_command(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    dt_scheduled = get_next_schedule(conf.bot.job_schedule)
    start_msg = msg_start.format(user_full_name=user_full_name, 
                                 dt_scheduled=dt_scheduled)
    
    logging.info(f'Visited user {user_id} {user_full_name}')
    
    await bot.send_message(message.from_user.id, start_msg)


@dp.message_handler(commands=['add_user'])
async def process_add_user(message: types.Message):
    user_id = message.from_user.id
    msg_success = f'Пользователь {user_id} успешно добавлен'
    with open(conf.paths.id_list_path, 'a') as f:
        f.write(f'{user_id}\n')
    logging.info(f'User {user_id} added')
    await bot.send_message(user_id, msg_success)


async def send_notification(msg, **kwargs):
    
    dt = date.today()
    msg_notify = msg.format(dt=dt, **kwargs)
    
    with open(conf.paths.id_list_path, 'r') as f:
        id_list = f.readlines()
    try:
        for user_id in id_list:
            await bot.send_message(text=msg_notify, chat_id=user_id.strip())
    except Exception as ex:
        logging.error('No users were added yet')
    

if __name__ == '__main__':
    
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(send_notification, 
                      **job_schedule, 
                      start_date=datetime.now(), 
                      args=(conf.bot.notification_message,))
    scheduler.start()
    executor.start_polling(dp)
