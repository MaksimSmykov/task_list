import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.messagebox as mb
# Импорт модуля для преобразования кортежей через format
from time import strftime, sleep
from xmlrpc.client import boolean
from tkinter import colorchooser

from requests import delete
import tkcalendar as tkc
from tkcalendar import Calendar
from add_methods import check_status, convert_to_bool, print_common_info

task_list = []
priority_color = "#F0E68C"
showed = False

def show_info(tasks):
    global showed
    msg = f"Время выполнять задания:\n"
    for key, value in tasks.items():
        msg += str(value) + '. ' + str(key) + '\n'
    showed = False
    print(showed)
    print(msg)
    mb.showinfo("Напоминание", msg)

def show_current_time():
    str_time = strftime('%H:%M:%S')
    str_date = strftime('%d.%m.%Y')
    label_time.config(text='Сейчас: ' + str_time)
    label_date.config(text='Сегодня: ' + str_date)
    label_time.after(1000, show_current_time)

i = 0
def check_time():
    global i
    i += 1
    print(i)
    if str(label_time['text']).endswith('00'):
        print('00')
        print(window.after_id)
        check_to_do()
        window.after_cancel(window.after_id)
        return True
    window.after_id = window.after(1000, check_time)

# Функция отображения времени и даты
def check_to_do():
    global showed
    tasks = {}
    if showed == False:
        for task in task_list:
            if not task['time'].isspace():
                if not task['date'].isspace():
                    if (str_split(task['time'],':') == strftime('%H:%M') and
                            str_split(task['date'],'.') == strftime('%d.%m.%Y')) and not task['completed']:
                        tasks[task['name']] = task_list.index(task) + 1
                else:
                    if str_split(task['time'], ':') == strftime('%H:%M') and not task['completed']:
                            tasks[task['name']] = task_list.index(task) + 1
            elif not task['date'].isspace():
                if str_split(task['date'], '.') == strftime('%d.%m.%Y') and not task['completed']:
                    tasks[task['name']] = task_list.index(task) + 1
    if len(tasks) > 0:
        show_info(tasks)
    window.after(60000, check_to_do)


def str_split(str_, split_sign):
    split_line = []
    split_line = str_.split(split_sign)
    for line in range(len(split_line)):
        if len(split_line[line]) == 1:
            split_line[line] = '0' + split_line[line]
    new_str = ''
    for line in split_line:
        new_str += line
        new_str += split_sign
    new_str = new_str[:-1]
    return new_str

def print_task_info(task):
    status = check_status(task)
    str_info = (f'{task_list[int(textbox_insert.get()) - 1]["name"]}'
                f' [{task_list[int(textbox_insert.get()) - 1]["priority"]}] - [Статус: {status}]')
    if not task['additional'].isspace():
        str_info += f' | Доп. информация: {task_list[int(textbox_insert.get()) - 1]["additional"]}'
    if not task['time'].isspace():
        str_info += f' | Время: {task['time']}'
    if not task['date'].isspace():
        str_info += f' | Дата: {task['date']}'

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
            split_line = line.split('!@!')
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
            try:
                task['date'] = split_line[5]
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
                new_str = '!@!'.join(new_list)
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
        task_info = ''
        if task['completed']:
            task_info += f'{u'\u2713'}'
        task_info += f' {index + 1}. {task["name"]} | Приоритет: [{task["priority"]}]'
        if not task['additional'].isspace():
            task_info +=  f' | Доп. информация: {task["additional"]}'
        if not task['time'].isspace():
            task_info +=  f' | Время: {str_split(task['time'],':')}'
        if not task['date'].isspace():
            task_info +=  f' | Дата: {str_split(task['date'],'.')}'


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
    else:
        task['time'] = ' '
    if enabled_date.get() == 1:
        task['date'] = chosen_date.get()
    else:
        task['date'] = ' '
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

def remove_all_completed():
    count = 0
    for task in task_list.copy():
        if task['completed']:
            task_list.remove(task)
            count += 1
    textbox_info.delete(0, 'end')
    textbox_info.insert(0, f'Все выполненные задачи удалены. Количество: {count}')  # Вывод информации о задаче
    show_tasks_list()
    write_txt()

def rename_task():
    task_list[int(textbox_insert.get()) - 1]['name'] = textbox_info.get()
    textbox_info.delete(0, 'end')
    textbox_info.insert(0, f'Задача {int(textbox_insert.get())} переименована')  # Вывод информации о задаче
    textbox_insert.delete(0, 'end')
    show_tasks_list()
    write_txt()

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
        if (textbox_insert.get().lower() in task['name'].lower() or
                textbox_insert.get().lower() in task['additional'].lower()):  # Проверка, есть ли ключевое слово в названии задачи
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
                textbox_insert.delete(0, 'end')
                show_tasks_list()
                write_txt()
            else:
                textbox_info.delete(0, 'end')
                textbox_info.insert(0, f'Задача номер {textbox_insert.get()} уже выполнена!')  # Сообщение о завершении задачи
        else:
            print_common_info(textbox_info, 0, 'end', 0, 'Задачи с таким номером нет!')
    else:
        print_common_info(textbox_info, 0, 'end', 0, 'Вы ввели отрицательное число или не число в строку для поиска!')

# def rename(number):
#     task_list[number]['name'] = textbox_insert.get()

def choose_color():
    global priority_color
    priority_color = colorchooser.askcolor(
        title="Выберите цвет задач с высоким приоритетом",
        initialcolor="#F0E68C") # Initial color (a warm khaki shade)
    for index, task in enumerate(task_list):  # Цикл по всем задачам
        # Определение статуса задачи в зависимости от того, завершена она или нет
        if task["priority"] == 'Высокий':
            _list.itemconfig(index, background=priority_color[1])

def pick_date(event):
    global calendar_, date_window
    date_window = tk.Toplevel()
    date_window.grab_set()
    date_window.title('Выберите дату')
    date_window.geometry('250x220+590+370')
    date_window.resizable(False, False)
    calendar_ = tkc.Calendar(date_window, selectmode='day', locale='ru_RU', date_pattern='dd.mm.y')
    calendar_.pack(expand=True, side=TOP, fill = X)

    date_btn = tk.Button(date_window, text='Выбрать дату', command=grab_date)
    date_btn.pack(expand=True, side=BOTTOM)

def grab_date():
    chosen_date.delete(0, END)
    chosen_date.insert(0, calendar_.get_date())
    date_window.destroy()

window = tk.Tk()  # создание окна
window.title('Список задач v2.2')
window.geometry('780x500')
window.resizable(False, False)

canvas_list = tk.LabelFrame(window)
canvas_list.pack(side=LEFT, fill = Y)

label_list = tk.Label(canvas_list, text='Список задач:', font='Arial 11 bold')
label_list.pack(anchor=NW, padx=30, pady=10)

verticalscrollbar = tk.Scrollbar(canvas_list)
verticalscrollbar.pack(side=RIGHT, fill="y")

horizontalscrollbar = tk.Scrollbar(canvas_list, orient=HORIZONTAL)
horizontalscrollbar.pack(side=BOTTOM, fill="x")

_list = tk.Listbox(canvas_list, width=55, height=25)
_list.pack(padx=30)

horizontalscrollbar.config(command = _list.xview)
verticalscrollbar.config(command = _list.yview)

canvas_buttons = tk.LabelFrame(window)
canvas_buttons.pack(expand=True, side=LEFT, fill = BOTH)

canvas_create = tk.LabelFrame(canvas_buttons)
canvas_create.pack(side=TOP, fill = BOTH)

label_textbox = tk.Label(canvas_create, text='Введите новую задачу:', font='Arial 9 bold')
label_textbox.grid(row=0, column=0, columnspan=4, padx=0, pady=10)
label_task_name = tk.Label(canvas_create, text='Название\nзадачи:')
label_task_name.grid(row=1, column=0, padx=20)
textbox_name = tk.Entry(canvas_create, width=30)
textbox_name.grid(row=1, column=1, columnspan=2, padx=5)
label_task_add = tk.Label(canvas_create, text='Дополнительная информация:')
label_task_add.grid(row=2, column=0, columnspan=3, padx=5)
textbox_add_info = tk.Entry(canvas_create, width=35)
textbox_add_info.grid(row=3, column=0, columnspan=3)

label_task_priority = tk.Label(canvas_create, text='Приоритет\nзадачи:')
label_task_priority.grid(row=4, column=0)
list_priority = ["Низкий", "Средний", "Высокий"]
# по умолчанию будет выбран первый элемент
priority_var = StringVar(value=list_priority[0])
label = ttk.Label(textvariable=priority_var)
combobox_priority = ttk.Combobox(canvas_create, state="readonly", textvariable=priority_var, values=list_priority, width=10)
combobox_priority.grid(row=4, column=1)
button_color = tk.Button(canvas_create, text='Выбрать цвет', width=13, height=1, command=choose_color)
button_color.grid(row=4, column=2, padx=10)

time_frame = tk.Frame(canvas_create, relief="solid")

enabled_time = IntVar()
time_checkbutton = ttk.Checkbutton(canvas_create, text="Время", variable=enabled_time)
time_checkbutton.grid(row=5, column=0)
hour = tk.Spinbox(time_frame,from_=0,to=23, wrap=True,width=4,justify=CENTER)
hour.grid(row=0, column=0)
minute = tk.Spinbox(time_frame,from_=0,to=59, wrap=True, width=4, justify=CENTER)
minute.grid(row=0, column=1)
time_frame.grid(row=5, column=1)

label_time = tk.Label(canvas_create, text='Время:')
label_time.grid(row=5, column=2, pady=5)
label_date = tk.Label(canvas_create, text='Дата:')
label_date.grid(row=6, column=2, pady=5)

enabled_date = IntVar()
date_checkbutton = ttk.Checkbutton(canvas_create, text="Дата", variable=enabled_date)
date_checkbutton.grid(row=6, column=0, pady=5)
chosen_date = tk.Entry(canvas_create)
chosen_date.grid(row=6, column=1, pady=0)
str_date = strftime('%d.%m.%Y')
chosen_date.insert(0, str_date)
chosen_date.bind('<1>', pick_date)

button_add = tk.Button(canvas_create, text='Добавить задачу', width=15, height=2, command=add_task)
button_add.grid(row=7, column=1, padx=0, pady=5)

canvas_actions = tk.LabelFrame(canvas_buttons)
canvas_actions.pack(side=TOP, fill = BOTH)

label_textbox_remove = tk.Label(canvas_actions, text='Введите номер или содержащееся слово:')
label_textbox_remove.grid(row=0, column=0, columnspan=3, padx=0, pady=5)
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

button_remove_completed = tk.Button(canvas_actions, text='Удалить выполненные', width=19, height=1, command=remove_all_completed)
button_remove_completed.grid(row=4, column=0, padx=0, pady=5)
button_rename = tk.Button(canvas_actions, text='Переименовать', width=15, height=1, command=rename_task)
button_rename.grid(row=4, column=1, padx=0, pady=5)

label_result = tk.Label(canvas_actions, text='Результат:', font='Arial 9 bold')
label_result.grid(row=5, column=0, columnspan=3, padx=0, pady=5)
textbox_info = tk.Entry(canvas_actions, width=55)
textbox_info.grid(row=6, column=0, columnspan=3, padx=10, pady=5)

open_txt()
# check_time()
window.after(1000,check_time)
show_current_time()

window.mainloop()  # Обновление информации о происходящем на экране
