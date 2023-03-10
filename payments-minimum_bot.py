import asyncio
import logging

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType

from yookassa import Configuration, Payment
import uuid

from messages import MESSAGES
from config import BOT_TOKEN, PAYMENTS_PROVIDER_TOKEN, TIME_MACHINE_IMAGE_URL,account_id_cfg,secret_key_cfg
from dict_to_db import dict_to_db_func

idempotence_key = str(uuid.uuid4())
Configuration.account_id = account_id_cfg
Configuration.secret_key = secret_key_cfg

logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)


loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot, loop=loop)

def create_invoice():
    payment = Payment.create({
        "amount": {
            "value": "200.00",
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/vpn_buy_tunnel_bot"
        },
        "description": "Заказ №1"
    }, idempotence_key)
    global payment_id
    payment_id = payment.id
    return payment.confirmation.confirmation_url

@dp.message_handler(commands=['start'])
async def process_terms_command(message: types.Message):
    print(message)
    await message.reply(MESSAGES['terms'], reply=False)


@dp.message_handler(commands=['terms'])
async def process_terms_command(message: types.Message):
    await message.reply(MESSAGES['terms'], reply=False)


@dp.message_handler(commands=['buy'])
async def process_buy_command(message: types.Message):
    if secret_key_cfg[:4] == 'test':
        await bot.send_message(message.chat.id, MESSAGES['pre_buy_demo_alert'])

    await bot.send_message(message.chat.id, create_invoice())
    await bot.send_message(message.chat.id, '''После оплаты напишите '/check' ''')

@dp.message_handler(commands=['check'])
async def process_terms_command(message: types.Message):
    try:
        payment = Payment.find_one(payment_id)
        if payment.paid == True:
            await bot.send_message(message.chat.id, MESSAGES['successful_payment'].format(total_amount=200,currency="RUB"))
        else:
            await bot.send_message(message.chat.id, 'Оплата еще не поступила')
    except:
        await bot.send_message(message.chat.id, 'Кажется вы еще ничего не покупали')


if __name__ == '__main__':
    executor.start_polling(dp, loop=loop)
