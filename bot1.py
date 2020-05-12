import time
import vk_api
import random
import wikipedia
import requests
import beat
import bs4
vk = vk_api.VkApi(token='34e79cbc4c66ba3f64a9b5f7fa3f0f3a2f2588cd4fd1a21b5b637b870e9b3434104515c768fa6cdeb0612') 
wikipedia.set_lang("RU")

values = {'out': 0, 'count': 100, 'time_offset': 60}


def write_msg(user_id, message, random_id):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random_id})


def get_user(user):
    fie_lds = "bdate, city, sex, country, nickname,followers_count, occupation"
    r = vk.method('users.get', {'user_id': user, 'fields': fie_lds})
    print(r[0]['first_name'], r[0]['last_name'])
    nameuser = r[0]['first_name']
    return nameuser


def _clean_all_tag_from_str(string_line):
    result = ""
    not_skip = True
    for i in list(string_line):
        if not_skip:
            if i == "<":
                not_skip = False
            else:
                result += i
        else:
            if i == ">":
                not_skip = True

    return result


def _get_time():
    request = requests.get("https://my-calend.ru/date-and-time-today")
    b = bs4.BeautifulSoup(request.text, "html.parser")
    return _clean_all_tag_from_str(str(b.select(".page")[0].findAll("h2")[1])).split()[1]


def check_message(message_in, user):  # Анализ input, генерация output
    message = ' этот бот предназначен специально для очень веселого, отзывчивого, невероятно умного человека. Максим Алексеевич, это для вас!' \
            '\nнапишите "помощь"'
    nameuser = get_user(user)
    try:
        req = " ".join(message_in.split()[1:])
        message_in = message_in.lower()
        if "/" in message_in:
            if ('помощь' or 'что ты можешь') in message_in:
                message = "Я мало что могу, но надеюсь для бота потянет: " \
                          "\n/поиск - выдаю случайного человека, с которым вы можете познакомиться" \
                          "\n/wiki - выдаю данные из Википедии по запросу '/wiki'" \
                          "\n/помощь - показываю текущую справку с командами." \
                          "\n/время - показываю текущее время по запросу '/время'" \
                          "\nтак же вы можете со мной ограниченно поболтать. Отвечу на слова приветствия, вопрос как дела и может еще что то. "
            elif "поиск" in message_in:
                message = "Попробуй познакомиться с этим человеком: vk.com/id" + str(
                    random.randrange(1, 432000000))
            elif "wiki" in message_in:
                message = 'Вот что я нашёл: \n' + str(
                    wikipedia.summary(" ".join(message_in.split()[1:])))
            elif 'время' in message_in:
                message = 'точное время: \n' + str(
                    _get_time())
            else:
                message = nameuser + ", извините, у меня нет такой команды. Все команды можно посмотреть по запросу '/помощь'."
        if message_in in ["привет", "приветик", "добрый день", "здравствуйте", "здравствуй"]:
            message = "здравствуйте, лучший учитель в мире " + nameuser
        elif message_in in ["как дела?", "как дела", "как поживаешь", "как настроение"]:
            message = nameuser + ", все отлично, главное чтоб у вас все было хорошо! думаю вам интересно почему я не ходила на ваши занятия. спросите! "
        elif message_in in ['почему ты не ходила на занятия', "почему тебя не было", "где ты была", "почему"]:
            message = 'оправдания своему поступку я еще не придумала, но будьте уверены я не теряла времени зря! спросите меня какой балл я хочу за проект. '
            # return message, attachment
        elif message_in in ['какой', "какй балл ты хочешь", "какой балл ты хочешь за проект"]:
            message = "ну я согласна и на 50, но 70-80 меня бы обрадовали больше. кстати вы ведь соскучались по Сириусу?"
        elif message_in in ["да", "конечно", "естественно", "очень", "невероятно"]:
            message = 'полностью с вами согласна! такое прекрасное место... если вам интересно, можете спросить когда у меня день рождения) '
        elif message_in in ['когда у тебя день рождения', "когда", "когда день рождения"]:
            message = ['я думала вы знаете( 30 апреля. представляете как грстно отмечать его в условиях карантина! ладно, думаю вам уже надоело. до свидания! ']
        elif message_in in ['пока','досвидания','доброй ночи','удачи']:
            message = 'ciao'
        return message
    except Exception:
        pass
            


while True:
    response = vk.method('messages.getConversations', values)
    print(response)
    if response['items']:
        values['last_message_id'] = response['items'][0]['last_message']['id']
    for item in response['items']:
        user = item['last_message'][u'from_id']
        if user > 0:
            print(item)
            rand_id = item['last_message'][u'random_id']
            # nameuser = get_user(user)
            message_in = item['last_message']['text']
            message = check_message(message_in, user)

            write_msg(user, message, rand_id)

    time.sleep(0.5)
