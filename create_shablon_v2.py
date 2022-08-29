#******************************************************************************#
# Программа оформления шапок в python файлах                                   #
#                                                                              #
#******************************************************************************#
# Андрей Закуров 2022-08-21                                                    #
#                                                                              #
#******************************************************************************#
# При первом запуске скрипт проводит опрос пользователя для получения          #
# необходимойинформации, и выводит список python файлов находящихся в одной    #
# нимпапке, и предлагает пользователю оформить шапку как выборочно по номеру   #
# файла,так и во всех сразу. Можно так же создавать новые файлы.               #
#                                                                              #
#******************************************************************************#

from os import listdir, system
from os.path import isfile
from datetime import date

#
# имя файла для сохранения результатов
DATA_FILE = 'data_shablon.txt'


# шапка интерфейса
def head_script():
    print('#', '*' * 78, '#', sep='')
    print('#', ' ' * 20, 'скрипт создания шапки', sep='')


# проверки
def is_valid(name, data):
    if not isfile(name):
        return 'new'
    else:
        with open(name, 'r', encoding='utf-8') as File:
            for i in range(len(data)):
                if data[i] != File.readline().rstrip():
                    return 'add'
        return 'head_ok'


# получение от  пользователя или загрузка из файла данных о проекте
def get_data(command, file=DATA_FILE):
    ret = []

    # получение от пользователя
    if command == 'new':
        questions = [
            'ВВедите название проекта: ',
            'ВВедите свое имя: ',
            'Теперь краткое описание проекта в одну строку\nне используя ENTER: '
        ]
        print('Новый проект')
        for quest in questions:
            if quest == questions[1]:
                ret.append(input(quest) + ' ' + str(date.today()))
            else:
                ret.append(input(quest))
        return ret

    # загрузка из файла
    if command == 'get':
        with open(DATA_FILE, 'r', encoding='utf-8') as File:
            return [line.rstrip() for line in File.readlines()]
    
# поиск python файлов

def get_files():
    
    # имя этого скрипта
    script_name = __file__.split('/')[-1]
    data = {}
    # список с содержимым папки
    all_files = listdir()
    count = 1
    
    for file in all_files:
        if '.' in file:
            if isfile(file) and file.split('.')[1] == 'py' and file != script_name:
                data[count] = file
                count += 1
    return data    


# генерация шапки
def gen_header(content):
    ret = []
    line_add = ''
    border = '#' + '*' * 78 + '#'
    empty = '#' + ' ' * 78 + '#'
    ret.append(border)
    for line in range(len(content)):
        if line == 2:
            if len(content[line]) + 4 > 80:
                stroka = content[line].split()
                line_add = '# '
                count = 2
                for word in stroka:
                    if count + len(word) + 2 < 80:
                        line_add += word + ' '
                        count += len(word) + 1
                    elif count + len(word) + 2 > 80:
                        line_add += ' ' * (79 - len(line_add)) + '#'
                        ret.append(line_add)
                        line_add = '# ' + word
                        count = 3 + len(word)
                ret.append(line_add + (' ' * (79 - len(line_add))) + '#')

        else:
            ret.append('# ' + content[line] + (' ' * (76 - len(content[line]))) + ' #')
        ret.append(empty)
        ret.append(border)
    return ret


# проверка на наличе шапки, загрузка при ее отсутствии в шапке
def run_header(name_file, content):
    comm = {'new': 'w', 'add': 'r+'}
    result_valid = is_valid(name_file, content)
    temp_per = []
    
    if result_valid == 'head_ok':
        print(f'в файле {name_file} шапка уже существует')
        return True
    
    with open(name_file, comm[result_valid], encoding='utf-8') as File:
        if result_valid == 'new':
            print(f'файл {name_file} создан')
            print(*content, sep='\n', file=File)
        if result_valid == 'add':
            print(f'в файл {name_file} добавлена шапка')
            temp_per = [line for line in File.readlines()]
            File.seek(0)
            print(*content, sep='\n', file=File)
            print(*temp_per, sep='', file=File)
        return True

# редактирование шапки
def head_edit(old_data):
    system('clear')
    head_script()
    data = get_data('new')
    with open(DATA_FILE, 'w', encoding='utf-8') as File:
        print(*data, sep='\n', file=File)    
    
if __name__ == '__main__':

    project_status = isfile(DATA_FILE)
    data = []

    system('clear')
    head_script()

    while True:
        
        # новый проект
        if not project_status:
            data = get_data('new')
            with open(DATA_FILE, 'w', encoding='utf-8') as File:
                print(*data, sep='\n', file=File)
            project_status = True


        # существующий проект
        if project_status:
            no_name = ['head', 'exit', 'all']
            data = get_data('get')
            files = get_files()

            print(f'В проекте {data[0]} имеются следующие файлы:')

            for key, name in files.items():
                print(f'{key}: {name}')

            print('Введите: номер файла или имя нового')
            print('Для редактирования шапки введите: head')
            print('Для выбора всех файлов введите: all')
            print('для выхода введите: exit')
            name = input('>>')

            if name.lower() == 'exit':
                break

            if name.lower() == 'head':
                head_edit(data)

                
            if name.lower() == 'all':
                for file in files:
                    run_header(files[file], gen_header(data))
                    
            if name.isdigit() and files[int(name)]:
                run_header(files[int(name)], gen_header(data))

            if not name.isdigit() and name.lower() not in no_name:
                run_header(name, gen_header(data))
            system('clear')
            head_script()

