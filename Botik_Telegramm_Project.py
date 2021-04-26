import datetime as dt
import time
from random import randint

import requests
from telegram import ReplyKeyboardMarkup
from telegram.error import BadRequest
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters, Updater

from Log_Talega import TOKEN
from Others import my_friends
from bots_functions import bots_functions, bots_future_functions
from dic_quest import around_world_easy, around_world_middle, inventions_easy, inventions_middle, \
    games_and_entertainment_easy, games_and_entertainment_middle, art_easy, art_middle

answer_no = ['no', 'нет', 'отвянь', 'не хочу', 'отстань', 'не буду', 'потом']

sp_ans = []

sp_tasks_list = ['Ваш список дел:']
dic_for_new_func = {}

name_func_temporary = []

counter_points = []

sp_quest_stages = []  # ________________________________________________________________________________________________Порядок вопросов для викторины
while len(sp_quest_stages) != 10:
    num = randint(1, 10)
    if num not in sp_quest_stages:
        sp_quest_stages.append(num)
print(sp_quest_stages)


def start(update,
          context):  # _________________________________________________________________________________________________Старт
    update.message.reply_text('👋')
    update.message.reply_text('Приветствую вас \n'
                              'Чем могу вам помочь? \n'
                              'Список команд будет выведен по команде /help', reply_markup=markup)
    print('/start')


def help(update,
         context):  # __________________________________________________________________________________________________Запрос помощи
    update.message.reply_text('❓')
    update.message.reply_text(bots_functions)


def plans_for_the_future(update,
                         context):  # __________________________________________________________________________Планы на будущее
    update.message.reply_text('❗️❗️❗️')
    update.message.reply_text(bots_future_functions)


def dialoge(update,
            context):  # _______________________________________________________________________________________________Маленький диалог
    update.message.reply_text('🗣')
    update.message.reply_text('Ок \n'
                              'Диалог можно остановить в любое время: \n'
                              'Просто напиши: /stop')
    locality = update.message.text
    print(locality)
    update.message.reply_text(
        "Где ты живешь?".format(**locals()))
    return 1_1


def first_response_dialoge(update, context):
    locality = update.message.text
    print(locality)
    if locality == '/skip':
        update.message.reply_text(
            "Какая погода у вас за окном?".format(**locals()))
        return 1_2
    update.message.reply_text(
        "Какая погода в городе {locality}?".format(**locals()))
    return 1_2


def second_response_dialoge(update, context):
    weather = update.message.text
    print(weather)
    update.message.reply_text("Давайте завершим диалог\n"
                              "Пока я не сказал чего-то лишнего...")
    return ConversationHandler.END


def random_cube(update,
                context):  # ___________________________________________________________________________________________Кинуть 20-ти гранный кубик
    update.message.reply_text('🎲')
    cube = randint(1, 20)
    print(f'-----------------------')
    print(f'Random num (1, 20) = {cube}')
    update.message.reply_text(f"Это число: {cube}")
    if cube <= 5:
        update.message.reply_text("😂")
    elif 5 < cube <= 10:
        update.message.reply_text("🙃")
    elif 10 < cube <= 15:
        update.message.reply_text("👏")
    elif 15 < cube <= 19:
        update.message.reply_text("💪")
    else:
        update.message.reply_text("🖕")


def cube_battle(update,
                context):  # ___________________________________________________________________________________________Битва на кубиках
    update.message.reply_text('🎲 vs 🎲')
    cube_bot = randint(1, 20)
    cube_human = randint(1, 20)
    if cube_bot > cube_human:
        so_thats_mean = 'Я выиграл'
        smile_rezult = '🤣'
    elif cube_bot < cube_human:
        so_thats_mean = 'Вы выиграли'
        smile_rezult = '🎉'
    else:
        so_thats_mean = 'Ничья!!'
        smile_rezult = '🙀'
    print(f'-----------------------')
    print(f'Bot`s random num (1, 20) = {cube_bot}')
    print(f'Human`s random num (1, 20) = {cube_human}')
    update.message.reply_text(f"Это число: {cube_human}\n"
                              f"У меня число: {cube_bot}\n"
                              f"{so_thats_mean}")
    update.message.reply_text(f"{smile_rezult}")


def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


# Обычный обработчик, как и те, которыми мы пользовались раньше.
def set_timer(update,
              context):  # _____________________________________________________________________________________________Таймер
    """Добавляем задачу в очередь"""
    chat_id = update.message.chat_id
    update.message.reply_text('⏱')
    try:
        # args[0] должен содержать значение аргумента
        # (секунды таймера)
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text(
                'Извините, не умеем возвращаться в прошлое')
            return

        # Добавляем задачу в очередь
        # и останавливаем предыдущую (если она была)
        job_removed = remove_job_if_exists(
            str(chat_id),
            context
        )
        context.job_queue.run_once(
            task,
            due,
            context=chat_id,
            name=str(chat_id)
        )
        text = f'Вернусь через {due} секунд!'
        if job_removed:
            text += ' Старая задача удалена.'
        # Присылаем сообщение о том, что всё получилось.
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Использование: /set_timer <секунд>')


def task(context):
    """Выводит сообщение"""
    job = context.job
    context.bot.send_message(job.context, text='Вернулся!')


def unset_timer(update,
                context):  # ___________________________________________________________________________________Сброс таймера
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Хорошо, вернулся сейчас!' if job_removed else 'Нет активного таймера.'
    update.message.reply_text(text)


def time_now(update,
             context):  # ______________________________________________________________________________________________Выводит время
    update.message.reply_text(f'Now: {dt.datetime.now().time()}')


def date_now(update,
             context):  # ______________________________________________________________________________________________Выводит дату
    update.message.reply_text(f'Today: {dt.datetime.now().date()}')


def stop():  # _________________________________________________________________________________________________________Стоп
    return ConversationHandler.END


def my_list(update,
            context):  # _______________________________________________________________________________________________Вывод Списка
    sp_result = "\n".join(sp_tasks_list)
    update.message.reply_text('📂')
    update.message.reply_text('📁')
    update.message.reply_text(sp_result)


def fill_list(update,
              context):  # _____________________________________________________________________________________________Заполнение Списка
    new_task = update.message.text
    update.message.reply_text(f'📝')
    update.message.reply_text(f'Я записал')
    try:
        sp_tasks_list.append(new_task.split(' ')[1])
    except IndexError:
        update.message.reply_text(f'Надо ввести: /fill_list <задача>')
    print(sp_tasks_list)


def del_list(update,
             context):  # ______________________________________________________________________________________________Удаление из списка
    del_task = update.message.text
    update.message.reply_text(f'📝')
    update.message.reply_text(f'Удалил эту задачу\n'
                              f'Чтобы проверить введи /my_list')
    try:
        sp_tasks_list.pop(int(del_task.split(' ')[1]))
    except IndexError:
        update.message.reply_text(f'Надо ввести: /del_list <задача>')
    print(sp_tasks_list)


def me_today(update,
             context):  # ______________________________________________________________________________________________"Ты сегодня..."
    sp_emg = ['😀', '🤣', '🙃', '😍', '🥰', '🤪', '😎', '😒', '😖', '😭',
              '😡', '😱', '🤔', '😐', '😴', '🤑', '😈', '🤡', '🤖', '🧐']
    num_emg = randint(1, 20)
    update.message.reply_text("Ты сегодня...")
    update.message.reply_text(sp_emg[num_emg])


def create_func(update,
                context):  # ___________________________________________________________________________________________Создание своей функции
    update.message.reply_text('👌')
    update.message.reply_text('Напиши мне ее название')
    return 2_1


def first_stage_of_creating(update, context):
    print('----------------------------------------')
    name = update.message.text
    print(name)
    dic_for_new_func[name] = 'New Func'
    name_func_temporary.append(name)
    update.message.reply_text(
        "Что будет делать функция {name}?".format(**locals()))
    return 2_2


def second_stage_of_creating(update, context):
    about_func = update.message.text
    print(about_func)
    dic_for_new_func[name_func_temporary[-1]] = f'About: {about_func}'
    print(f'{name_func_temporary[-1]} -- {dic_for_new_func[name_func_temporary[-1]]}')
    update.message.reply_text(
        'Я отправил моему другу твоё предложение\n'
        'Если он его оценит, то твоя функция добавится в мои')
    return ConversationHandler.END


def map(update,
        context):  # ___________________________________________________________________________________________Вывод карты и координат
    update.message.reply_text('🔎')
    map_rec = update.message.text
    try:
        ans = map_rec.split(' ')[1]
        geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={ans}&format=json"
        response = requests.get(geocoder_request)
        if response:
            # Преобразуем ответ в json-объект
            json_response = response.json()

            # Получаем первый топоним из ответа геокодера.
            # Согласно описанию ответа, он находится по следующему пути:
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            # Полный адрес топонима:
            toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
            # Координаты центра топонима:
            toponym_coodrinates = toponym["Point"]["pos"]
            # Печатаем извлечённые из ответа поля:
            print(toponym_address, "имеет координаты:", toponym_coodrinates)
            update.message.reply_text(f'{toponym_address} имеет координаты: {toponym_coodrinates}')

            # static_api_request = f"https://static-maps.yandex.ru/1.x/?ll=37.677751,55.757718&spn=0.055,0.055&l=map"
            static_api_request = f"https://static-maps.yandex.ru/1.x/?ll={toponym_coodrinates}8&spn=0.055,0.055&l=map"
            context.bot.send_photo(
                update.message.chat_id,
                static_api_request,
                caption="Нашёл:"
            )
    except IndexError:
        update.message.reply_text('Надо так: /map <место>')
    except BadRequest:
        print("Ошибка вывода карты(Ошибка в создании ссылки)")


def others_about(update,
                 context):  # __________________________________________________________________________________________Мои друзья и т.п.
    update.message.reply_text("😏")
    update.message.reply_text("Рад, что ты спросил!!")
    for i in range(len(my_friends)):
        update.message.reply_text(my_friends[i])
        time.sleep(1)


def quest(update,
          context):  # _________________________________________________________________________________________________Викторина
    update.message.reply_text(
        "Пройдите небольшую викторину!\n"
        "Ввелите что-нибудь для продолжения\n")
    return 1


def first_customization_quest(update,
                              context):  # _____________________________________________________________________________Настройки
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
            "1. Вокруг света")
        time.sleep(1)
        update.message.reply_text(
            "2. Изобретения")
        time.sleep(1)
        update.message.reply_text(
            "3. Игры и развлечения")
        time.sleep(1)
        update.message.reply_text(
            "4. Искусство")
        time.sleep(3)
        update.message.reply_text(
            "Итак, ваш выбор...")
        return 2


def second_customization_quest(update, context):
    theme = update.message.text
    if theme == '1':
        sp_ans.append('Вокруг света')
    elif theme == '2':
        sp_ans.append('Изобретения')
    elif theme == '3':
        sp_ans.append('Игры и развлечения')
    elif theme == '4':
        sp_ans.append('Искусство')
    else:
        sp_ans.append('Вокруг света')
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


def thrid_customization_quest(update,
                              context):  # _____________________________________________________________________Конец настроек и Начало викторины
    level = update.message.text
    if level == '1':
        sp_ans.append('Легко')
    elif level == '2':
        sp_ans.append('Нормально')
    else:
        sp_ans.append('Нормально')
    print(level)
    update.message.reply_text(
        "Я вас понял")
    time.sleep(1)
    update.message.reply_text(
        "Мы можем начинать")
    print(sp_ans)
    if sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Легко':
        update.message.reply_text(around_world_easy[f'{sp_quest_stages[0]}.'])
        update.message.reply_text(around_world_easy[f'variants{sp_quest_stages[0]}'])
    elif sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Нормально':
        update.message.reply_text(around_world_middle[f'{sp_quest_stages[0]}.'])
        update.message.reply_text(around_world_middle[f'variants{sp_quest_stages[0]}'])
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Легко':
        update.message.reply_text(inventions_easy[f'{sp_quest_stages[0]}.'])
        update.message.reply_text(inventions_easy[f'variants{sp_quest_stages[0]}'])
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Нормально':
        update.message.reply_text(inventions_middle[f'{sp_quest_stages[0]}.'])
        update.message.reply_text(inventions_middle[f'variants{sp_quest_stages[0]}'])
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Легко':
        update.message.reply_text(games_and_entertainment_easy[f'{sp_quest_stages[0]}.'])
        update.message.reply_text(games_and_entertainment_easy[f'variants{sp_quest_stages[0]}'])
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Нормально':
        update.message.reply_text(games_and_entertainment_middle[f'{sp_quest_stages[0]}.'])
        update.message.reply_text(games_and_entertainment_middle[f'variants{sp_quest_stages[0]}'])
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Легко':
        update.message.reply_text(around_world_easy[f'{sp_quest_stages[0]}.'])
        update.message.reply_text(around_world_easy[f'variants{sp_quest_stages[0]}'])
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Нормально':
        update.message.reply_text(art_middle[f'{sp_quest_stages[0]}.'])
        update.message.reply_text(art_middle[f'variants{sp_quest_stages[0]}'])
    return 4


def first_question(update, context):
    ans = update.message.text
    key_dic = f'ans{sp_quest_stages[0]}'
    if sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Легко':
        if ans == around_world_easy[key_dic][0] or ans == around_world_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = around_world_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Нормально':
        if ans == around_world_middle[key_dic][0] or ans == around_world_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = around_world_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Легко':
        if ans == inventions_easy[key_dic][0] or ans == inventions_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = inventions_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Нормально':
        if ans == inventions_middle[key_dic][0] or ans == inventions_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = inventions_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Легко':
        if ans == games_and_entertainment_easy[key_dic][0] or ans == games_and_entertainment_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = games_and_entertainment_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Нормально':
        if ans == games_and_entertainment_middle[key_dic][0] or ans == games_and_entertainment_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = games_and_entertainment_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Легко':
        if ans == art_easy[key_dic][0] or ans == art_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = art_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Нормально':
        if ans == art_middle[key_dic][0] or ans == art_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = art_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    if sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Легко':
        update.message.reply_text(around_world_easy[f'{sp_quest_stages[1]}.'])
        update.message.reply_text(around_world_easy[f'variants{sp_quest_stages[1]}'])
    elif sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Нормально':
        update.message.reply_text(around_world_middle[f'{sp_quest_stages[1]}.'])
        update.message.reply_text(around_world_middle[f'variants{sp_quest_stages[1]}'])
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Легко':
        update.message.reply_text(inventions_easy[f'{sp_quest_stages[1]}.'])
        update.message.reply_text(inventions_easy[f'variants{sp_quest_stages[1]}'])
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Нормально':
        update.message.reply_text(inventions_middle[f'{sp_quest_stages[1]}.'])
        update.message.reply_text(inventions_middle[f'variants{sp_quest_stages[1]}'])
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Легко':
        update.message.reply_text(games_and_entertainment_easy[f'{sp_quest_stages[1]}.'])
        update.message.reply_text(games_and_entertainment_easy[f'variants{sp_quest_stages[1]}'])
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Нормально':
        update.message.reply_text(games_and_entertainment_middle[f'{sp_quest_stages[1]}.'])
        update.message.reply_text(games_and_entertainment_middle[f'variants{sp_quest_stages[1]}'])
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Легко':
        update.message.reply_text(art_easy[f'{sp_quest_stages[1]}.'])
        update.message.reply_text(art_easy[f'variants{sp_quest_stages[1]}'])
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Нормально':
        update.message.reply_text(around_world_easy[f'{sp_quest_stages[1]}.'])
        update.message.reply_text(around_world_easy[f'variants{sp_quest_stages[1]}'])
    return 5


def second_question(update, context):
    ans = update.message.text
    key_dic = f'ans{sp_quest_stages[1]}'
    if sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Легко':
        if ans == around_world_easy[key_dic][0] or ans == around_world_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = around_world_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Нормально':
        if ans == around_world_middle[key_dic][0] or ans == around_world_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = around_world_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Легко':
        if ans == inventions_easy[key_dic][0] or ans == inventions_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = inventions_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Нормально':
        if ans == inventions_middle[key_dic][0] or ans == inventions_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = inventions_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Легко':
        if ans == games_and_entertainment_easy[key_dic][0] or ans == games_and_entertainment_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = games_and_entertainment_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Нормально':
        if ans == games_and_entertainment_middle[key_dic][0] or ans == games_and_entertainment_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = games_and_entertainment_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Легко':
        if ans == art_easy[key_dic][0] or ans == art_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = art_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Нормально':
        if ans == art_middle[key_dic][0] or ans == art_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = art_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    if sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Легко':
        update.message.reply_text(around_world_easy[f'{sp_quest_stages[2]}.'])
        update.message.reply_text(around_world_easy[f'variants{sp_quest_stages[2]}'])
    elif sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Нормально':
        update.message.reply_text(around_world_middle[f'{sp_quest_stages[2]}.'])
        update.message.reply_text(around_world_middle[f'variants{sp_quest_stages[2]}'])
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Легко':
        update.message.reply_text(inventions_easy[f'{sp_quest_stages[2]}.'])
        update.message.reply_text(inventions_easy[f'variants{sp_quest_stages[2]}'])
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Нормально':
        update.message.reply_text(inventions_middle[f'{sp_quest_stages[2]}.'])
        update.message.reply_text(inventions_middle[f'variants{sp_quest_stages[2]}'])
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Легко':
        update.message.reply_text(games_and_entertainment_easy[f'{sp_quest_stages[2]}.'])
        update.message.reply_text(games_and_entertainment_easy[f'variants{sp_quest_stages[2]}'])
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Нормально':
        update.message.reply_text(games_and_entertainment_middle[f'{sp_quest_stages[2]}.'])
        update.message.reply_text(games_and_entertainment_middle[f'variants{sp_quest_stages[2]}'])
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Легко':
        update.message.reply_text(art_easy[f'{sp_quest_stages[2]}.'])
        update.message.reply_text(art_easy[f'variants{sp_quest_stages[2]}'])
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Нормально':
        update.message.reply_text(art_middle[f'{sp_quest_stages[2]}.'])
        update.message.reply_text(art_middle[f'variants{sp_quest_stages[2]}'])
    return 6


def third_question(update, context):
    ans = update.message.text
    key_dic = f'ans{sp_quest_stages[2]}'
    if sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Легко':
        if ans == around_world_easy[key_dic][0] or ans == around_world_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = around_world_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Нормально':
        if ans == around_world_middle[key_dic][0] or ans == around_world_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = around_world_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Легко':
        if ans == inventions_easy[key_dic][0] or ans == inventions_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = inventions_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Нормально':
        if ans == inventions_middle[key_dic][0] or ans == inventions_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = inventions_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Легко':
        if ans == games_and_entertainment_easy[key_dic][0] or ans == games_and_entertainment_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = games_and_entertainment_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Нормально':
        if ans == games_and_entertainment_middle[key_dic][0] or ans == games_and_entertainment_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = games_and_entertainment_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Легко':
        if ans == art_easy[key_dic][0] or ans == art_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = art_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Нормально':
        if ans == art_middle[key_dic][0] or ans == art_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = art_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    if sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Легко':
        update.message.reply_text(around_world_easy[f'{sp_quest_stages[3]}.'])
        update.message.reply_text(around_world_easy[f'variants{sp_quest_stages[3]}'])
    elif sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Нормально':
        update.message.reply_text(around_world_middle[f'{sp_quest_stages[3]}.'])
        update.message.reply_text(around_world_middle[f'variants{sp_quest_stages[3]}'])
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Легко':
        update.message.reply_text(inventions_easy[f'{sp_quest_stages[3]}.'])
        update.message.reply_text(inventions_easy[f'variants{sp_quest_stages[3]}'])
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Нормально':
        update.message.reply_text(inventions_middle[f'{sp_quest_stages[3]}.'])
        update.message.reply_text(inventions_middle[f'variants{sp_quest_stages[3]}'])
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Легко':
        update.message.reply_text(games_and_entertainment_easy[f'{sp_quest_stages[3]}.'])
        update.message.reply_text(games_and_entertainment_easy[f'variants{sp_quest_stages[3]}'])
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Нормально':
        update.message.reply_text(games_and_entertainment_middle[f'{sp_quest_stages[3]}.'])
        update.message.reply_text(games_and_entertainment_middle[f'variants{sp_quest_stages[3]}'])
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Легко':
        update.message.reply_text(art_easy[f'{sp_quest_stages[3]}.'])
        update.message.reply_text(art_easy[f'variants{sp_quest_stages[3]}'])
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Нормально':
        update.message.reply_text(art_middle[f'{sp_quest_stages[3]}.'])
        update.message.reply_text(art_middle[f'variants{sp_quest_stages[3]}'])
    return 7


def forth_question(update, context):
    ans = update.message.text
    key_dic = f'ans{sp_quest_stages[3]}'
    if sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Легко':
        if ans == around_world_easy[key_dic][0] or ans == around_world_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = around_world_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Нормально':
        if ans == around_world_middle[key_dic][0] or ans == around_world_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = around_world_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Легко':
        if ans == inventions_easy[key_dic][0] or ans == inventions_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = inventions_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Нормально':
        if ans == inventions_middle[key_dic][0] or ans == inventions_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = inventions_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Легко':
        if ans == games_and_entertainment_easy[key_dic][0] or ans == games_and_entertainment_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = games_and_entertainment_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Нормально':
        if ans == games_and_entertainment_middle[key_dic][0] or ans == games_and_entertainment_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = games_and_entertainment_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Легко':
        if ans == art_easy[key_dic][0] or ans == art_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = art_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Нормально':
        if ans == art_middle[key_dic][0] or ans == art_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = art_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    if sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Легко':
        update.message.reply_text(around_world_easy[f'{sp_quest_stages[4]}.'])
        update.message.reply_text(around_world_easy[f'variants{sp_quest_stages[4]}'])
    elif sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Нормально':
        update.message.reply_text(around_world_middle[f'{sp_quest_stages[4]}.'])
        update.message.reply_text(around_world_middle[f'variants{sp_quest_stages[4]}'])
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Легко':
        update.message.reply_text(inventions_easy[f'{sp_quest_stages[4]}.'])
        update.message.reply_text(inventions_easy[f'variants{sp_quest_stages[4]}'])
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Нормально':
        update.message.reply_text(inventions_middle[f'{sp_quest_stages[4]}.'])
        update.message.reply_text(inventions_middle[f'variants{sp_quest_stages[4]}'])
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Легко':
        update.message.reply_text(games_and_entertainment_easy[f'{sp_quest_stages[4]}.'])
        update.message.reply_text(games_and_entertainment_easy[f'variants{sp_quest_stages[4]}'])
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Нормально':
        update.message.reply_text(games_and_entertainment_middle[f'{sp_quest_stages[4]}.'])
        update.message.reply_text(games_and_entertainment_middle[f'variants{sp_quest_stages[4]}'])
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Легко':
        update.message.reply_text(art_easy[f'{sp_quest_stages[4]}.'])
        update.message.reply_text(art_easy[f'variants{sp_quest_stages[4]}'])
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Нормально':
        update.message.reply_text(art_middle[f'{sp_quest_stages[4]}.'])
        update.message.reply_text(art_middle[f'variants{sp_quest_stages[4]}'])
    return 8


def fifth_question(update, context):
    ans = update.message.text
    key_dic = f'ans{sp_quest_stages[4]}'
    if sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Легко':
        if ans == around_world_easy[key_dic][0] or ans == around_world_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = around_world_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Нормально':
        if ans == around_world_middle[key_dic][0] or ans == around_world_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = around_world_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Легко':
        if ans == inventions_easy[key_dic][0] or ans == inventions_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = inventions_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Нормально':
        if ans == inventions_middle[key_dic][0] or ans == inventions_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = inventions_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Легко':
        if ans == games_and_entertainment_easy[key_dic][0] or ans == games_and_entertainment_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = games_and_entertainment_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Нормально':
        if ans == games_and_entertainment_middle[key_dic][0] or ans == games_and_entertainment_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = games_and_entertainment_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Легко':
        if ans == art_easy[key_dic][0] or ans == art_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = art_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Нормально':
        if ans == art_middle[key_dic][0] or ans == art_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = art_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    if sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Легко':
        update.message.reply_text(around_world_easy[f'{sp_quest_stages[5]}.'])
        update.message.reply_text(around_world_easy[f'variants{sp_quest_stages[5]}'])
    elif sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Нормально':
        update.message.reply_text(around_world_middle[f'{sp_quest_stages[5]}.'])
        update.message.reply_text(around_world_middle[f'variants{sp_quest_stages[5]}'])
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Легко':
        update.message.reply_text(inventions_easy[f'{sp_quest_stages[5]}.'])
        update.message.reply_text(inventions_easy[f'variants{sp_quest_stages[5]}'])
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Нормально':
        update.message.reply_text(inventions_middle[f'{sp_quest_stages[5]}.'])
        update.message.reply_text(inventions_middle[f'variants{sp_quest_stages[5]}'])
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Легко':
        update.message.reply_text(games_and_entertainment_easy[f'{sp_quest_stages[5]}.'])
        update.message.reply_text(games_and_entertainment_easy[f'variants{sp_quest_stages[5]}'])
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Нормально':
        update.message.reply_text(games_and_entertainment_middle[f'{sp_quest_stages[5]}.'])
        update.message.reply_text(games_and_entertainment_middle[f'variants{sp_quest_stages[5]}'])
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Легко':
        update.message.reply_text(art_easy[f'{sp_quest_stages[5]}.'])
        update.message.reply_text(art_easy[f'variants{sp_quest_stages[5]}'])
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Нормально':
        update.message.reply_text(art_middle[f'{sp_quest_stages[5]}.'])
        update.message.reply_text(art_middle[f'variants{sp_quest_stages[5]}'])
    return 9


def sixth_question(update, context):
    ans = update.message.text
    key_dic = f'ans{sp_quest_stages[5]}'
    if sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Легко':
        if ans == around_world_easy[key_dic][0] or ans == around_world_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = around_world_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Нормально':
        if ans == around_world_middle[key_dic][0] or ans == around_world_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = around_world_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Легко':
        if ans == inventions_easy[key_dic][0] or ans == inventions_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = inventions_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Нормально':
        if ans == inventions_middle[key_dic][0] or ans == inventions_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = inventions_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Легко':
        if ans == games_and_entertainment_easy[key_dic][0] or ans == games_and_entertainment_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = games_and_entertainment_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Нормально':
        if ans == games_and_entertainment_middle[key_dic][0] or ans == games_and_entertainment_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = games_and_entertainment_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Легко':
        if ans == art_easy[key_dic][0] or ans == art_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = art_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Нормально':
        if ans == art_middle[key_dic][0] or ans == art_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = art_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    if sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Легко':
        update.message.reply_text(around_world_easy[f'{sp_quest_stages[6]}.'])
        update.message.reply_text(around_world_easy[f'variants{sp_quest_stages[6]}'])
    elif sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Нормально':
        update.message.reply_text(around_world_middle[f'{sp_quest_stages[6]}.'])
        update.message.reply_text(around_world_middle[f'variants{sp_quest_stages[6]}'])
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Легко':
        update.message.reply_text(inventions_easy[f'{sp_quest_stages[6]}.'])
        update.message.reply_text(inventions_easy[f'variants{sp_quest_stages[6]}'])
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Нормально':
        update.message.reply_text(inventions_middle[f'{sp_quest_stages[6]}.'])
        update.message.reply_text(inventions_middle[f'variants{sp_quest_stages[6]}'])
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Легко':
        update.message.reply_text(games_and_entertainment_easy[f'{sp_quest_stages[6]}.'])
        update.message.reply_text(games_and_entertainment_easy[f'variants{sp_quest_stages[6]}'])
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Нормально':
        update.message.reply_text(games_and_entertainment_middle[f'{sp_quest_stages[6]}.'])
        update.message.reply_text(games_and_entertainment_middle[f'variants{sp_quest_stages[6]}'])
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Легко':
        update.message.reply_text(art_easy[f'{sp_quest_stages[6]}.'])
        update.message.reply_text(art_easy[f'variants{sp_quest_stages[6]}'])
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Нормально':
        update.message.reply_text(art_middle[f'{sp_quest_stages[6]}.'])
        update.message.reply_text(art_middle[f'variants{sp_quest_stages[6]}'])
    return 10


def seventh_question(update, context):
    ans = update.message.text
    key_dic = f'ans{sp_quest_stages[6]}'
    if sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Легко':
        if ans == around_world_easy[key_dic][0] or ans == around_world_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = around_world_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Нормально':
        if ans == around_world_middle[key_dic][0] or ans == around_world_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = around_world_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Легко':
        if ans == inventions_easy[key_dic][0] or ans == inventions_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = inventions_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Нормально':
        if ans == inventions_middle[key_dic][0] or ans == inventions_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = inventions_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Легко':
        if ans == games_and_entertainment_easy[key_dic][0] or ans == games_and_entertainment_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = games_and_entertainment_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Нормально':
        if ans == games_and_entertainment_middle[key_dic][0] or ans == games_and_entertainment_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = games_and_entertainment_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Легко':
        if ans == art_easy[key_dic][0] or ans == art_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = art_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Нормально':
        if ans == art_middle[key_dic][0] or ans == art_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = art_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    if sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Легко':
        update.message.reply_text(around_world_easy[f'{sp_quest_stages[7]}.'])
        update.message.reply_text(around_world_easy[f'variants{sp_quest_stages[7]}'])
    elif sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Нормально':
        update.message.reply_text(around_world_middle[f'{sp_quest_stages[7]}.'])
        update.message.reply_text(around_world_middle[f'variants{sp_quest_stages[7]}'])
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Легко':
        update.message.reply_text(inventions_easy[f'{sp_quest_stages[7]}.'])
        update.message.reply_text(inventions_easy[f'variants{sp_quest_stages[7]}'])
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Нормально':
        update.message.reply_text(inventions_middle[f'{sp_quest_stages[7]}.'])
        update.message.reply_text(inventions_middle[f'variants{sp_quest_stages[7]}'])
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Легко':
        update.message.reply_text(games_and_entertainment_easy[f'{sp_quest_stages[7]}.'])
        update.message.reply_text(games_and_entertainment_easy[f'variants{sp_quest_stages[7]}'])
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Нормально':
        update.message.reply_text(games_and_entertainment_middle[f'{sp_quest_stages[7]}.'])
        update.message.reply_text(games_and_entertainment_middle[f'variants{sp_quest_stages[7]}'])
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Легко':
        update.message.reply_text(art_easy[f'{sp_quest_stages[7]}.'])
        update.message.reply_text(art_easy[f'variants{sp_quest_stages[7]}'])
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Нормально':
        update.message.reply_text(art_middle[f'{sp_quest_stages[7]}.'])
        update.message.reply_text(art_middle[f'variants{sp_quest_stages[7]}'])
    return 11


def eighth_question(update, context):
    ans = update.message.text
    key_dic = f'ans{sp_quest_stages[7]}'
    if sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Легко':
        if ans == around_world_easy[key_dic][0] or ans == around_world_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = around_world_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Нормально':
        if ans == around_world_middle[key_dic][0] or ans == around_world_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = around_world_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Легко':
        if ans == inventions_easy[key_dic][0] or ans == inventions_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = inventions_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Нормально':
        if ans == inventions_middle[key_dic][0] or ans == inventions_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = inventions_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Легко':
        if ans == games_and_entertainment_easy[key_dic][0] or ans == games_and_entertainment_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = games_and_entertainment_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Нормально':
        if ans == games_and_entertainment_middle[key_dic][0] or ans == games_and_entertainment_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = games_and_entertainment_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Легко':
        if ans == art_easy[key_dic][0] or ans == art_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = art_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Нормально':
        if ans == art_middle[key_dic][0] or ans == art_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = art_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    if sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Легко':
        update.message.reply_text(around_world_easy[f'{sp_quest_stages[8]}.'])
        update.message.reply_text(around_world_easy[f'variants{sp_quest_stages[8]}'])
    elif sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Нормально':
        update.message.reply_text(around_world_middle[f'{sp_quest_stages[8]}.'])
        update.message.reply_text(around_world_middle[f'variants{sp_quest_stages[8]}'])
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Легко':
        update.message.reply_text(inventions_easy[f'{sp_quest_stages[8]}.'])
        update.message.reply_text(inventions_easy[f'variants{sp_quest_stages[8]}'])
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Нормально':
        update.message.reply_text(inventions_middle[f'{sp_quest_stages[8]}.'])
        update.message.reply_text(inventions_middle[f'variants{sp_quest_stages[8]}'])
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Легко':
        update.message.reply_text(games_and_entertainment_easy[f'{sp_quest_stages[8]}.'])
        update.message.reply_text(games_and_entertainment_easy[f'variants{sp_quest_stages[8]}'])
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Нормально':
        update.message.reply_text(games_and_entertainment_middle[f'{sp_quest_stages[8]}.'])
        update.message.reply_text(games_and_entertainment_middle[f'variants{sp_quest_stages[8]}'])
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Легко':
        update.message.reply_text(art_easy[f'{sp_quest_stages[8]}.'])
        update.message.reply_text(art_easy[f'variants{sp_quest_stages[8]}'])
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Нормально':
        update.message.reply_text(art_middle[f'{sp_quest_stages[8]}.'])
        update.message.reply_text(art_middle[f'variants{sp_quest_stages[8]}'])
    return 12


def ninth_question(update, context):
    ans = update.message.text
    key_dic = f'ans{sp_quest_stages[8]}'
    if sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Легко':
        if ans == around_world_easy[key_dic][0] or ans == around_world_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = around_world_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Нормально':
        if ans == around_world_middle[key_dic][0] or ans == around_world_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = around_world_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Легко':
        if ans == inventions_easy[key_dic][0] or ans == inventions_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = inventions_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Нормально':
        if ans == inventions_middle[key_dic][0] or ans == inventions_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = inventions_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Легко':
        if ans == games_and_entertainment_easy[key_dic][0] or ans == games_and_entertainment_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = games_and_entertainment_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Нормально':
        if ans == games_and_entertainment_middle[key_dic][0] or ans == games_and_entertainment_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = games_and_entertainment_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Легко':
        if ans == art_easy[key_dic][0] or ans == art_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = art_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Нормально':
        if ans == art_middle[key_dic][0] or ans == art_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = art_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    if sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Легко':
        update.message.reply_text(around_world_easy[f'{sp_quest_stages[9]}.'])
        update.message.reply_text(around_world_easy[f'variants{sp_quest_stages[9]}'])
    elif sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Нормально':
        update.message.reply_text(around_world_middle[f'{sp_quest_stages[9]}.'])
        update.message.reply_text(around_world_middle[f'variants{sp_quest_stages[9]}'])
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Легко':
        update.message.reply_text(inventions_easy[f'{sp_quest_stages[9]}.'])
        update.message.reply_text(inventions_easy[f'variants{sp_quest_stages[9]}'])
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Нормально':
        update.message.reply_text(inventions_middle[f'{sp_quest_stages[9]}.'])
        update.message.reply_text(inventions_middle[f'variants{sp_quest_stages[9]}'])
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Легко':
        update.message.reply_text(games_and_entertainment_easy[f'{sp_quest_stages[9]}.'])
        update.message.reply_text(games_and_entertainment_easy[f'variants{sp_quest_stages[9]}'])
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Нормально':
        update.message.reply_text(games_and_entertainment_middle[f'{sp_quest_stages[9]}.'])
        update.message.reply_text(games_and_entertainment_middle[f'variants{sp_quest_stages[9]}'])
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Легко':
        update.message.reply_text(art_easy[f'{sp_quest_stages[9]}.'])
        update.message.reply_text(art_easy[f'variants{sp_quest_stages[9]}'])
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Нормально':
        update.message.reply_text(art_middle[f'{sp_quest_stages[9]}.'])
        update.message.reply_text(art_middle[f'variants{sp_quest_stages[9]}'])
    return 13


def tenth_question(update, context):
    ans = update.message.text
    key_dic = f'ans{sp_quest_stages[9]}'
    if sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Легко':
        if ans == around_world_easy[key_dic][0] or ans == around_world_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = around_world_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Вокруг света' and sp_ans[1] == 'Нормально':
        if ans == around_world_middle[key_dic][0] or ans == around_world_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = around_world_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Легко':
        if ans == inventions_easy[key_dic][0] or ans == inventions_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = inventions_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Изобретения' and sp_ans[1] == 'Нормально':
        if ans == inventions_middle[key_dic][0] or ans == inventions_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = inventions_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Легко':
        if ans == games_and_entertainment_easy[key_dic][0] or ans == games_and_entertainment_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = games_and_entertainment_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Игры и развлечения' and sp_ans[1] == 'Нормально':
        if ans == games_and_entertainment_middle[key_dic][0] or ans == games_and_entertainment_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = games_and_entertainment_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Легко':
        if ans == art_easy[key_dic][0] or ans == art_easy[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = art_easy[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    elif sp_ans[0] == 'Искусство' and sp_ans[1] == 'Нормально':
        if ans == art_middle[key_dic][0] or ans == art_middle[key_dic]:
            update.message.reply_text('Правильно')
            counter_points.append('+')
        else:
            update.message.reply_text('Нет')
            right_ans = art_middle[key_dic]
            update.message.reply_text(f'Правильный ответ: {right_ans}')
    points = len(counter_points) * 10
    update.message.reply_text(f'В итоге вы набрали: {points} баллов.')
    return ConversationHandler.END


def main():  # _________________________________________________________________________________________________________Main()
    updater = Updater(TOKEN, use_context=True)

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('dialoge', dialoge)],
        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1_1: [MessageHandler(Filters.text, first_response_dialoge)],
            # Функция читает ответ на второй вопрос и завершает диалог.
            1_2: [MessageHandler(Filters.text, second_response_dialoge)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("random_cube", random_cube))
    dp.add_handler(CommandHandler("cube_battle", cube_battle))
    dp.add_handler(CommandHandler("set_timer", set_timer))
    dp.add_handler(CommandHandler("unset_timer", unset_timer))
    dp.add_handler(CommandHandler("my_list", my_list))
    dp.add_handler(CommandHandler("fill_list", fill_list))
    dp.add_handler(CommandHandler("del_list", del_list))
    dp.add_handler(CommandHandler("me_today", me_today))

    new_func = ConversationHandler(
        # Точка входа в диалог.
        entry_points=[CommandHandler('create_func', create_func)],

        # Состояние внутри диалога.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            2_1: [MessageHandler(Filters.text, first_stage_of_creating)],
            # Функция читает ответ на второй вопрос и завершает диалог.
            2_2: [MessageHandler(Filters.text, second_stage_of_creating)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(CommandHandler("map", map))
    dp.add_handler(CommandHandler("time_now", time_now))
    dp.add_handler(CommandHandler("date_now", date_now))
    dp.add_handler(CommandHandler("others_about", others_about))
    dp.add_handler(CommandHandler("plans_for_the_future", plans_for_the_future))
    dp.add_handler(conv_handler)
    dp.add_handler(new_func)
    # Quest

    quest_history = ConversationHandler(
        entry_points=[CommandHandler('quest', quest)],
        states={
            1: [MessageHandler(Filters.text, first_customization_quest)],
            2: [MessageHandler(Filters.text, second_customization_quest)],
            3: [MessageHandler(Filters.text, thrid_customization_quest)],
            4: [MessageHandler(Filters.text, first_question)],
            5: [MessageHandler(Filters.text, second_question)],
            6: [MessageHandler(Filters.text, third_question)],
            7: [MessageHandler(Filters.text, forth_question)],
            8: [MessageHandler(Filters.text, fifth_question)],
            9: [MessageHandler(Filters.text, sixth_question)],
            10: [MessageHandler(Filters.text, seventh_question)],
            11: [MessageHandler(Filters.text, eighth_question)],
            12: [MessageHandler(Filters.text, ninth_question)],
            13: [MessageHandler(Filters.text, tenth_question)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(quest_history)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    reply_keyboard = [['/help']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    print('Для начала введите /start')
    main()
