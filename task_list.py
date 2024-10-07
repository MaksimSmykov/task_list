import tkinter as tk
from tkinter import ttk
from tkinter import *
from xmlrpc.client import boolean
from tkinter import colorchooser
from add_methods import check_status, convert_to_bool, print_common_info

task_list = []
priority_color = "#F0E68C"

def time_split(str_):
    split_line = []
    split_line = str_.split(':')
    return f'{split_line[0]}:{split_line[1]}'

def print_task_info(task):
    status = check_status(task)
    print(task)
    str_info = (f'{task_list[int(textbox_insert.get()) - 1]["name"]}'
                f' [{task_list[int(textbox_insert.get()) - 1]["priority"]}] - [Статус: {status}]')
    if 'additional' in task:
        str_info += f' | Доп. информация: {task_list[int(textbox_insert.get()) - 1]["additional"]}'
    if 'time' in task:
        str_info += ' Время: '

    return str_info

def check_color():
    global priority_color
    if isinstance(priority_color, str):
        return priority_color
    elif isinstance(priority_color, tuple):
        return priority_color[1]

def open_txt():
    try:
        with open('task_list.txt', 'r') as text_file:
            lines = text_file.readlines()
            split_line = []
        for line in lines:
            line = line[:-1]
            split_line = line.split(',')
            print(split_line)
            try:
                task = {
                    'name': split_line[0],  # Название задачи
                    'priority': split_line[1],  # Приоритет задачи
                    'completed': convert_to_bool(split_line[2]),  # Статус выполнения задачи (изначально False)
                    'additional': split_line[3]
                }
            except IndexError:
                task = {
                    'name': split_line[0],  # Название задачи
                    'priority': split_line[1],  # Приоритет задачи
                    'completed': convert_to_bool(split_line[2]),  # Статус выполнения задачи (изначально False)
                }
            try:
                task['time'] = split_line[4]
            except IndexError:
                pass
            task_list.append(task)  # Добавление задачи в список задач
            show_tasks_list()
        text_file.close()
    except FileNotFoundError:
        _list.insert('end', 'Задач нет!')

def write_txt():
    try:
        with open('task_list.txt', 'w') as text_file:
            for task in task_list:
                new_list = []
                for value in task.values():
                    if isinstance(value, boolean):
                        new_list.append(str(value))
                    elif len(value) == 0:
                        pass
                    else:
                        new_list.append(value)
                new_str = ','.join(new_list)
                if new_str.endswith(','):
                    new_str = new_str[1: -1]
                text_file.write(f'{new_str}\n')
        text_file.close()
    except FileNotFoundError:
        _list.insert('end', 'Задач нет!')

def show_tasks_list():
    _list.delete(0, 'end')

    global priority_color
    for index, task in enumerate(task_list):  # Цикл по всем задачам
        # Определение статуса задачи в зависимости от того, завершена она или нет
        status = check_status(task)
        task_info = f'{index + 1}. {task["name"]} | Приоритет: [{task["priority"]}] | Статус: {status}'
        if not task['additional'].isspace():
            task_info +=  f' | Доп. информация: {task["additional"]}'
        if 'time' in task:
            task_info += f' | Время: {time_split(task['time'])}'

        _list.insert('end',task_info)  # Вывод информации о задаче

        if task["priority"] == 'Высокий':
            new_color = check_color()
            _list.itemconfig(index, background=new_color)

def add_task():
    """
    Функция для добавления задачи в список задач.
    - task_name: строка, содержащая название задачи
    - *args: дополнительные параметры задачи, переданные как позиционные аргументы
    - priority: приоритет задачи (по умолчанию 'Normal')
    """
    task = {
        'name': textbox_name.get(),  # Название задачи
        'priority': combobox_priority.get(),  # Приоритет задачи
        'completed': False,  # Статус выполнения задачи (изначально False)
    }
    if textbox_add_info.get() == '' or textbox_add_info.get().isspace() == True:
        task['additional'] = ' '
    else:
        task['additional'] = textbox_add_info.get()
    if enabled_time.get() == 1:
        task['time'] = hour.get() + ':' + minute.get()
    if textbox_name.get() and combobox_priority.get():
        task_list.append(task)  # Добавление задачи в список задач
    show_tasks_list()
    textbox_name.delete(0, 'end')
    textbox_add_info.delete(0, 'end')
    write_txt()


def remove_task():
    if textbox_insert.get().isnumeric():
        if int(textbox_insert.get()) <= len(task_list) and int(textbox_insert.get()) != 0:
            textbox_info.delete(0, 'end')
            textbox_info.insert(0, 'Задача: ' + print_task_info(task_list[int(textbox_insert.get()) - 1]) + ' удалена')  # Вывод информации о задаче
            task_list.pop(int(textbox_insert.get()) - 1)
            textbox_insert.delete(0, 'end')
            show_tasks_list()
            write_txt()
        else:
            print_common_info(textbox_info, 0, 'end', 0, 'Задачи с таким номером нет!')
    else:
        print_common_info(textbox_info, 0, 'end', 0, 'Вы ввели отрицательное число или не число в строку для поиска!')


def find_task_by_number():
    if textbox_insert.get().isnumeric():
        if int(textbox_insert.get()) <= len(task_list) and int(textbox_insert.get()) != 0:
            textbox_info.delete(0, 'end')
            textbox_info.insert(0, f'Найдена задача: ' + print_task_info(task_list[int(textbox_insert.get()) - 1]))  # Вывод информации о задаче
            textbox_insert.delete(0, 'end')
        else:
            print_common_info(textbox_info, 0, 'end', 0, 'Задачи с таким номером нет!')
    else:
        print_common_info(textbox_info, 0, 'end', 0, 'Вы ввели отрицательное число или не число в строку для поиска!')


def find_task_by_keyword():
    found = False  # Флаг, указывающий, найдены ли задачи
    textbox_info.delete(0, 'end')
    for task in task_list:  # Перебор всех задач
        if textbox_insert.get().lower() in task['name'].lower():  # Проверка, есть ли ключевое слово в названии задачи
            try:
                status = check_status(task)
                textbox_info.insert('end', f'{task_list.index(task) + 1}. {task["name"]} | '
                                            f'Приоритет: [{task["priority"]}] | Статус: {status} | '
                                            f'Доп. информация: {task["additional"]}; ')
                # textbox_info.insert('end', f'{task_list.index(task) + 1}.' + print_task_info(task) + '; ')
                found = True  # Установка флага в True, если задача найдена
            except KeyError:
                status = check_status(task)
                textbox_info.insert('end', f'{task_list.index(task) + 1}. {task["name"]} | '
                                            f'Приоритет: [{task["priority"]}] | Статус: {status}; ')
                found = True  # Установка флага в True, если задача найдена
    if not found:  # Если задачи не найдены
        print_common_info(textbox_info, 0, 'end', 0, 'Задачи не найдены!')

def complete_task():
    """
    Отмечает задачу как выполненную.
    - task_index: индекс задачи (начинается с 1 для удобства)
    """
    if textbox_insert.get().isnumeric():
        if int(textbox_insert.get()) <= len(task_list) and int(textbox_insert.get()) != 0:
            task = task_list[int(textbox_insert.get()) - 1] # Получение задачи по индексу (минус 1 для корректного доступа)
            if task['completed'] == False:
                task['completed'] = True  # Установка флага выполнения задачи в True
                textbox_info.delete(0, 'end')
                textbox_info.insert(0, f'Задача номер {textbox_insert.get()} выполнена!')  # Сообщение о завершении задачи
                show_tasks_list()
                write_txt()
            else:
                textbox_info.delete(0, 'end')
                textbox_info.insert(0, f'Задача номер {textbox_insert.get()} уже выполнена!')  # Сообщение о завершении задачи
        else:
            print_common_info(textbox_info, 0, 'end', 0, 'Задачи с таким номером нет!')
    else:
        print_common_info(textbox_info, 0, 'end', 0, 'Вы ввели отрицательное число или не число в строку для поиска!')

def choose_color():
    global priority_color
    priority_color = colorchooser.askcolor(
        title="Выберите цвет задач с высоким приоритетом",
        initialcolor="#F0E68C") # Initial color (a warm khaki shade)
    for index, task in enumerate(task_list):  # Цикл по всем задачам
        # Определение статуса задачи в зависимости от того, завершена она или нет
        if task["priority"] == 'Высокий':
            _list.itemconfig(index, background=priority_color[1])

window = tk.Tk()  # создание окна
window.title('Список задач v2.2')
window.geometry('1000x450')
window.resizable(False, False)

canvas_list = tk.LabelFrame(window)
canvas_list.pack(side=LEFT, fill = Y)

label_list = tk.Label(canvas_list, text='Список задач:', font='Arial 11 bold')
label_list.pack(anchor=NW, padx=30, pady=10)
# label_list.place(x=30, y=25)

verticalscrollbar = tk.Scrollbar(canvas_list)
verticalscrollbar.pack(side=RIGHT, fill="y")

horizontalscrollbar = tk.Scrollbar(canvas_list, orient=HORIZONTAL)
horizontalscrollbar.pack(side=BOTTOM, fill="x")

_list = tk.Listbox(canvas_list, width=55, height=23)
_list.pack(padx=30)
# _list.place(x=30, y=50)  # другие методы grid, pack

horizontalscrollbar.config(command = _list.xview)
verticalscrollbar.config(command = _list.yview)

canvas_buttons = tk.LabelFrame(window)
canvas_buttons.pack(expand=True, side=LEFT, fill = BOTH)

canvas_create = tk.LabelFrame(canvas_buttons)
canvas_create.pack(side=TOP, fill = X)

label_textbox = tk.Label(canvas_create, text='Введите новую задачу:', font='Arial 9 bold')
label_textbox.grid(row=0, column=0, columnspan=4, padx=0, pady=10)
label_task_name = tk.Label(canvas_create, text='Название\nзадачи:')
label_task_name.grid(row=1, column=0, padx=20, pady=0)
textbox_name = tk.Entry(canvas_create, width=40)
textbox_name.grid(row=1, column=1, columnspan=2, padx=10)
label_task_add = tk.Label(canvas_create, text='Дополнительная информация:')
label_task_add.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
textbox_add_info = tk.Entry(canvas_create, width=40)
textbox_add_info.grid(row=3, column=0, columnspan=3, pady=5)

label_task_priority = tk.Label(canvas_create, text='Приоритет\nзадачи:')
label_task_priority.grid(row=4, column=0, padx=20, pady=0)
list_priority = ["Низкий", "Средний", "Высокий"]
# по умолчанию будет выбран первый элемент
priority_var = StringVar(value=list_priority[0])
label = ttk.Label(textvariable=priority_var)
combobox_priority = ttk.Combobox(canvas_create, state="readonly", textvariable=priority_var, values=list_priority, width=10)
combobox_priority.grid(row=4, column=1, padx=20, pady=0)
button_color = tk.Button(canvas_create, text='Выбрать цвет', width=13, height=1, command=choose_color)
button_color.grid(row=4, column=2, padx=0, pady=0)

enabled_time = IntVar()
enabled_checkbutton = ttk.Checkbutton(canvas_create, text="Время", variable=enabled_time)
enabled_checkbutton.grid(row=1, column=3,padx=20, pady=6)
hour = tk.Spinbox(canvas_create,from_=0,to=23, wrap=True,width=4,justify=CENTER)
hour.grid(row=1, column=4, padx=0, pady=0)
minute = tk.Spinbox(canvas_create,from_=0,to=59, increment=5, wrap=True,width=4,justify=CENTER)
minute.grid(row=1, column=5, padx=0, pady=0)

button_add = tk.Button(canvas_create, text='Добавить задачу', width=15, height=2, command=add_task)
button_add.grid(row=5, column=2, padx=00, pady=10)


canvas_actions = tk.LabelFrame(canvas_buttons)
canvas_actions.pack(side=TOP, fill = X)

label_textbox_remove = tk.Label(canvas_actions, text='Введите номер или содержащееся слово:')
label_textbox_remove.grid(row=0, column=0, ipadx=70, columnspan=3, padx=0, pady=5)
textbox_insert = tk.Entry(canvas_actions, width=40)
textbox_insert.grid(row=1, column=0, columnspan=3, padx=0, pady=0)
button_remove = tk.Button(canvas_actions, text='Удалить по номеру', width=15, height=1, command=remove_task)
button_remove.grid(row=2, column=0, padx=0, pady=5)
button_find_num = tk.Button(canvas_actions, text='Найти по номеру', width=14, height=1, command=find_task_by_number)
button_find_num.grid(row=2, column=1, padx=0, pady=5)
button_set_completed = tk.Button(canvas_actions, text='Выполнить по номеру', width=18, height=1, command=complete_task)
button_set_completed.grid(row=3, column=0, padx=0, pady=5)
button_find_key = tk.Button(canvas_actions, text='Найти по слову ', width=13, height=1, command=find_task_by_keyword)
button_find_key.grid(row=3, column=1, padx=0, pady=5)

label_result = tk.Label(canvas_actions, text='Результат:', font='Arial 9 bold')
label_result.grid(row=4, column=0, ipadx=70, columnspan=3, padx=0, pady=5)
textbox_info = tk.Entry(canvas_actions, width=50)
textbox_info.grid(row=5, column=0, columnspan=3, padx=0, pady=5)

open_txt()

window.mainloop()  # Обновление информации о происходящем на экране
