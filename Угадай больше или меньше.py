import time
from random import randint

from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters, Updater
from Log_Talega import TOKEN

orig_num = randint(1, 19)


def start(update, context):
    update.message.reply_text(
        f"Угадай следующее число будет больше или меньше числа {orig_num}\n"
        f"Диапозон чисел: от 0 до 20")
    time.sleep(1)
    return 1


def Ugadaika(update, context):
    ugad = update.message.text
    rand_num = randint(0, 20)
    time.sleep(1)
    update.message.reply_text(
        f"Было число: {orig_num}\n"
        f"Вы сказали, что новое число будет {ugad.upper()}\n"
        f"Выпало число: {rand_num}\n")
    time.sleep(1)
    if ugad.lower() == 'больше' and orig_num > rand_num:
        update.message.reply_text(
            f"Вы проиграли")
    elif ugad.lower() == 'меньше' and orig_num < rand_num:
        update.message.reply_text(
            f"Вы проиграли")
    elif ugad.lower() == 'больше' and orig_num < rand_num:
        update.message.reply_text(
            f"Вы выграли")
    elif ugad.lower() == 'меньше' and orig_num > rand_num:
        update.message.reply_text(
            f"Вы выграли")
    return ConversationHandler.END


def stop(update, context):
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(Filters.text, Ugadaika)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()
    

if __name__ == '__main__':
    main()
