import time
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters, Updater
from Log_Talega import TOKEN

flag_quest_complited = False
answer_no = ['no', 'нет', 'отвянь', 'не хочу', 'отстань', 'не буду', 'потом']

sp_ans = []
from dic_quest import easy


def start_quest(update, context):
    update.message.reply_text(
        "Привет. Пройдите небольшую викторину!\n"
        "Вы можете прервать викторину, послав команду /stop.\n")
    return 1


def first_customization_quest(update, context):
    ans = update.message.text
    print(ans)
    if ans.lower() in answer_no:
        update.message.reply_text(
            "Ну ладно\n"
            "Если вы захотите пройти мою викторину, вы знаете где меня найти\n"
            "Для повторного запуска введите /start")
        return ConversationHandler.END
    else:
        update.message.reply_text(
            "Для начала выберите тему вопроса.")
        time.sleep(1)
        update.message.reply_text(
            "1. Игры")
        time.sleep(1)
        update.message.reply_text(
            "2. Музыка")
        time.sleep(1)
        update.message.reply_text(
            "3. Кино")
        time.sleep(1)
        update.message.reply_text(
            "4. Открытия и Изобретения")
        time.sleep(3)
        update.message.reply_text(
            "Итак, ваш выбор...")
        return 2


def second_customization_quest(update, context):
    theme = update.message.text
    sp_ans.append(theme)
    print(theme)
    update.message.reply_text(
        "Хорошо")
    time.sleep(1)
    update.message.reply_text(
        "Выберите сложность")
    time.sleep(1)
    update.message.reply_text(
        "1. Легко")
    time.sleep(1)
    update.message.reply_text(
        "2. Нормально")
    time.sleep(1)
    update.message.reply_text(
        "3. Сложно")
    time.sleep(2)
    update.message.reply_text(
        "Ваш выбор...")
    return 3


def thrid_customization_quest(update, context):
    level = update.message.text
    sp_ans.append(level)
    print(level)
    update.message.reply_text(
        "Я вас понял")
    time.sleep(1)
    update.message.reply_text(
        "Мы можем начинать")
    update.message.reply_text(
        easy[sp_ans[0]])


'''
def first_question(update, context):
    if sp_ans[1] == 1 or sp_ans[1].lower() == 'легко':
        update.message.reply_text(
            easy[sp_ans[0]])'''


def stop(update, context):
    return ConversationHandler.END


def main_quest():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    quest = ConversationHandler(
        entry_points=[CommandHandler('start_quest', start_quest)],
        states={
            1: [MessageHandler(Filters.text, first_customization_quest)],
            2: [MessageHandler(Filters.text, second_customization_quest)],
            3: [MessageHandler(Filters.text, thrid_customization_quest)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(quest)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main_quest()
    
