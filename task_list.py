import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.messagebox as mb

from time import strftime
from tkinter import colorchooser
import csv, configparser
import ctypes
import tkcalendar as tkc

task_list = []
priority_color = "#F0E68C"
showed = False

rus = {}
eng = {}
language = 'Rus'

def convert_to_bool(input_str):
    """convert str to bool type"""
    if input_str == 'True':
        return True
    else:
        return False

def print_common_info(entry, delete_start, delete_end, insert_start, insert_info):
    """print task info"""
    entry.delete(delete_start, delete_end)
    entry.insert(insert_start, insert_info)

def str_split(str_, split_sign):
    """split string with split sign"""
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

def lang_str_split(str_, split_sign):
    """split input line"""
    split_line = []
    split_line = str_.split(split_sign)
    return split_line

def load_csv(filename):
    """load .csv file with interface languages"""
    global rus, eng, language
    with open(filename, encoding='utf8', newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = []
        for row in reader:
            rows.append(', '.join(row))
        match language:
            case 'Rus':
                for row in rows:
                    rus[row.split(';')[0]] = row.split(';')[1]
            case 'Eng':
                for row in rows:
                    eng[row.split(';')[0]] = row.split(';')[2]

def set_lang(word):
    """set interface language"""
    global rus, eng
    try:
        if language == 'Rus':
            word = rus[f'{word}']
        elif language == 'Eng':
            word = eng[f'{word}']
    except KeyError:
        word = 'None'
    return word

def show_reminder(tasks):
    """show msgbox with reminder tasks to do"""
    global showed
    msg = f"{set_lang('Time to do the tasks')}:\n"
    for key, value in tasks.items():
        msg += str(value) + '. ' + str(key) + '\n'
    showed = False
    global reminder_window
    reminder_window = tk.Toplevel()
    reminder_window.grab_set()
    reminder_window.title(f'{set_lang('Reminder')}!')
    reminder_window.geometry('+590+370')
    reminder_window.resizable(False, False)
    label_tasks_todo = tk.Label(reminder_window, text=msg)
    label_tasks_todo.grid(row=1, column=0, padx=10, pady=10)

def show_current_time():
    """show current time in program window"""
    str_time = strftime('%H:%M:%S')
    str_date = strftime('%d.%m.%Y')
    label_time.config(text=f'{set_lang('Now')}: ' + str_time)
    label_date.config(text=f'{set_lang('Today')}: ' + str_date)
    label_time.after(1000, show_current_time)

def check_time():
    """check current time to start reminder timer"""
    if str(label_time['text']).endswith('00'):
        check_to_do_time_date()
        check_to_do_date()
        window.after_cancel(window.after_id)
        return True
    window.after_id = window.after(1000, check_time)

def check_status(task):
    """check and return task status"""
    if task["completed"]:
        return set_lang('Completed')
    else:
        return set_lang('In progress')

def check_to_do_time_date():
    """check current time and date to start reminder timer"""
    global showed
    print('check_to_do_time_date')
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
    if len(tasks) > 0:
        show_reminder(tasks)
    window.after(60000, check_to_do_time_date)

def check_to_do_date():
    """check current date to start reminder timer"""
    global showed
    print('check_to_do_date')
    tasks = {}
    if showed == False:
        for task in task_list:
            if not task['date'].isspace() and task['time'].isspace():
                if str_split(task['date'], '.') == strftime('%d.%m.%Y') and not task['completed']:
                    tasks[task['name']] = task_list.index(task) + 1
    if len(tasks) > 0:
        show_reminder(tasks)
    window.after(300000, check_to_do_date)

def print_task_info(task):
    """print task info in program window"""
    status = check_status(task)
    str_info = (f'{task_list[int(textbox_insert.get()) - 1]["name"]}'
                f' [{set_lang(task_list[int(textbox_insert.get()) - 1]["priority"])}] - [{set_lang('Status')}: {status}]')
    if not task['additional'].isspace():
        str_info += f' | {set_lang('Add. information')}: {task_list[int(textbox_insert.get()) - 1]["additional"]}'
    if not task['time'].isspace():
        str_info += f' | {set_lang('Time:')} {task['time']}'
    if not task['date'].isspace():
        str_info += f' | {set_lang('Date:')} {task['date']}'
    return str_info

def check_color():
    """check color type and return value"""
    global priority_color
    if isinstance(priority_color, str):
        return priority_color
    elif isinstance(priority_color, tuple):
        return priority_color[1]

def open_txt():
    """open .txt file with tasks and append them to listbox"""
    try:
        with open('task_list.txt', 'r') as text_file:
            lines = text_file.readlines()
            split_line = []
        for line in lines:
            line = line[:-1]
            split_line = line.split('!@!')
            try:
                task = {
                    'name': split_line[0],
                    'priority': split_line[1],
                    'completed': convert_to_bool(split_line[2]),
                    'additional': split_line[3]
                }
            except IndexError:
                task = {
                    'name': split_line[0],
                    'priority': split_line[1],
                    'completed': convert_to_bool(split_line[2]),
                }
            try:
                task['time'] = split_line[4]
            except IndexError:
                pass
            try:
                task['date'] = split_line[5]
            except IndexError:
                pass
            task_list.append(task)
            show_tasks_list()
        text_file.close()
    except FileNotFoundError:
        _list.insert('end', f'{set_lang('No tasks')}!')

def write_txt():
    """write tasks to .txt file"""
    try:
        with open('task_list.txt', 'w') as text_file:
            for task in task_list:
                new_list = []
                for value in task.values():
                    if isinstance(value, bool):
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
        _list.insert('end', f'{set_lang('No tasks')}!')

def show_tasks_list():
    """show task list in listbox"""
    _list.delete(0, 'end')

    global priority_color
    for index, task in enumerate(task_list):
        status = check_status(task)
        task_info = ''
        if task['completed']:
            task_info += f'{u'\u2713'}'
        task_info += f' {index + 1}. {task["name"]} | {set_lang('Priority')}: [{set_lang(task["priority"])}]'
        if not task['additional'].isspace():
            task_info +=  f' | {set_lang('Add. information')}: {task["additional"]}'
        if not task['time'].isspace():
            task_info +=  f' | {set_lang('Time:')} {str_split(task['time'],':')}'
        if not task['date'].isspace():
            task_info +=  f' | {set_lang('Date:')} {str_split(task['date'],'.')}'

        _list.insert('end',task_info)  # Вывод информации о задаче

        if task["priority"] == 'High':
            new_color = priority_color
            _list.itemconfig(index, background=new_color)

def add_task():
    """add task to task list and write it to .txt file"""
    task = {
        'name': textbox_name.get(),  # Название задачи
    }
    match language:
        case 'Rus':
            task['priority'] = list(rus.keys())[list(rus.values()).index(combobox_priority.get())]  # Приоритет задачи
        case 'Eng':
            task['priority'] = list(eng.keys())[list(eng.values()).index(combobox_priority.get())]  # Приоритет задачи

    task['completed'] = False  # Статус выполнения задачи (изначально False)

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
    """remove task from task list"""
    if textbox_insert.get().isnumeric():
        if int(textbox_insert.get()) <= len(task_list) and int(textbox_insert.get()) != 0:
            textbox_info.delete(0, 'end')
            textbox_info.insert(0, f'{set_lang('Task')}: ' + print_task_info(task_list[int(textbox_insert.get()) - 1]) + f' {set_lang('is deleted')}')  # Вывод информации о задаче
            task_list.pop(int(textbox_insert.get()) - 1)
            textbox_insert.delete(0, 'end')
            show_tasks_list()
            write_txt()
        else:
            print_common_info(textbox_info, 0, 'end', 0, set_lang('There is no task with that number!'))
    else:
        print_common_info(textbox_info, 0, 'end', 0, set_lang("You've entered a negative number or non-number in the search string!"))

def remove_all_completed():
    """remove all completed tasks from task list"""
    count = 0
    for task in task_list.copy():
        if task['completed']:
            task_list.remove(task)
            count += 1
    textbox_info.delete(0, 'end')
    textbox_info.insert(0, f'{set_lang('All completed tasks are deleted. Quantity')}: {count}')  # Вывод информации о задаче
    show_tasks_list()
    write_txt()

def rename_open():
    """open window for task renaming"""
    global calendar_, new_task_name_window
    new_task_name_window = tk.Toplevel()
    new_task_name_window.grab_set()
    new_task_name_window.title(set_lang('Renaming'))
    new_task_name_window.geometry('300x120+590+370')
    new_task_name_window.resizable(False, False)

    label_task_number = tk.Label(new_task_name_window, text=f'{set_lang('Task number')}:')
    label_task_number.grid(row=1, column=0, pady=10)
    textbox_task_number = tk.Entry(new_task_name_window, width=15)
    textbox_task_number.grid(row=1, column=1, columnspan=2, padx=5)
    label_task_name = tk.Label(new_task_name_window, text=f'{set_lang('New name')}:')
    label_task_name.grid(row=2, column=0)
    textbox_task_name = tk.Entry(new_task_name_window, width=15)
    textbox_task_name.grid(row=2, column=1, columnspan=2, padx=5)

    def rename():
        """task renaming"""
        task_list[int(textbox_task_number.get()) - 1]['name'] = textbox_task_name.get()
        textbox_info.delete(0, END)
        textbox_info.insert(0, f'{set_lang('Task')} №{int(textbox_task_number.get())} {set_lang('is renamed')}')  # Вывод информации о задаче
        new_task_name_window.destroy()
        show_tasks_list()
        write_txt()
    button_rename = tk.Button(new_task_name_window, text=set_lang('Rename task'), width=20, height=1, command=rename)
    button_rename.grid(row=3, column=0, columnspan=2, padx=70, pady=10)

def find_task_by_number():
    """find task by number"""
    if textbox_insert.get().isnumeric():
        if int(textbox_insert.get()) <= len(task_list) and int(textbox_insert.get()) != 0:
            textbox_info.delete(0, 'end')
            textbox_info.insert(0, f'{set_lang('Found a task:')} ' + print_task_info(task_list[int(textbox_insert.get()) - 1]))  # Вывод информации о задаче
            textbox_insert.delete(0, 'end')
        else:
            print_common_info(textbox_info, 0, 'end', 0, set_lang('There is no task with that number!'))
    else:
        print_common_info(textbox_info, 0, 'end', 0, set_lang("You've entered a negative number or non-number in the search string!"))

def find_task_by_keyword():
    """find task by keyword"""
    found = False  # Флаг, указывающий, найдены ли задачи
    textbox_info.delete(0, 'end')
    for index, task in enumerate(task_list):  # Перебор всех задач
        if (textbox_insert.get().lower() in task['name'].lower() or
                textbox_insert.get().lower() in task['additional'].lower()):  # Проверка, есть ли ключевое слово в названии задачи
            status = check_status(task)
            str_info = (f'{index + 1}. {task["name"]}'
                        f' [{set_lang(task["priority"])}] - [{set_lang('Status')}: {status}]')
            if not task['additional'].isspace():
                str_info += f' | {set_lang('Add. information')}: {task["additional"]}'
            if not task['time'].isspace():
                str_info += f' | {set_lang('Time:')} {task['time']}'
            if not task['date'].isspace():
                str_info += f' | {set_lang('Date:')} {task['date']}'
            found = True  # Установка флага в True, если задача найдена
            textbox_info.insert(END, str_info + '; ')
    if not found:  # Если задачи не найдены
        print_common_info(textbox_info, 0, 'end', 0, set_lang('Tasks not found!'))

def complete_task():
    """make task completed"""
    if textbox_insert.get().isnumeric():
        if int(textbox_insert.get()) <= len(task_list) and int(textbox_insert.get()) != 0:
            task = task_list[int(textbox_insert.get()) - 1]
            if task['completed'] == False:
                task['completed'] = True
                textbox_info.delete(0, 'end')
                textbox_info.insert(0, f'{set_lang('Task number')} {textbox_insert.get()} {set_lang('completed')}!')  # Сообщение о завершении задачи
                textbox_insert.delete(0, 'end')
                show_tasks_list()
                write_txt()
            else:
                textbox_info.delete(0, 'end')
                textbox_info.insert(0, f'{set_lang('Task number')} {textbox_insert.get()} {set_lang('already completed')}!')  # Сообщение о завершении задачи
        else:
            print_common_info(textbox_info, 0, 'end', 0, set_lang('There is no task with that number!'))
    else:
        print_common_info(textbox_info, 0, 'end', 0, set_lang("You've entered a negative number or non-number in the search string!"))

def choose_color():
    """set color for high priority tasks"""
    global priority_color
    temp_color = priority_color
    priority_color = colorchooser.askcolor(
        title=set_lang('Select the color of high-priority tasks'),
        initialcolor="#F0E68C")[1] # Initial color
    for index, task in enumerate(task_list):
        if task["priority"] == 'High':
            _list.itemconfig(index, background=priority_color)
    try:
        save_config(lang_check.get())
    except TypeError:
        priority_color = temp_color
        print(priority_color)
        save_config(lang_check.get())

def pick_date(event):
    """open window with calendar to choose date"""
    global calendar_, date_window
    date_window = tk.Toplevel()
    date_window.grab_set()
    date_window.title(set_lang('Pick a date'))
    date_window.geometry('250x220+590+370')
    date_window.resizable(False, False)
    calendar_ = tkc.Calendar(date_window, selectmode='day', locale=set_lang('en_US'), date_pattern='dd.mm.y')
    calendar_.pack(expand=True, side=TOP, fill = X)
    date_btn = tk.Button(date_window, text=set_lang('Pick a date'), command=grab_date)
    date_btn.pack(expand=True, side=BOTTOM)

def grab_date():
    """set date for task"""
    chosen_date.delete(0, END)
    chosen_date.insert(0, calendar_.get_date())
    date_window.destroy()

def load_config():
    """load config from .ini file"""
    try:
        global priority_color, language
        config = configparser.ConfigParser()
        with open('config.ini', 'r') as config_file:
            config.read('config.ini')
        priority_color = config.get('Settings', 'priority_color')
        language = config.get('Settings', 'language')
        lang_check.set(language)
    except FileNotFoundError:
        save_config(lang_check.get())

def save_config(lang):
    """save config to .ini file"""
    global priority_color, language
    config = configparser.ConfigParser()
    config.add_section('Settings')
    config.set('Settings', 'language', lang)
    config.set('Settings', 'priority_color', priority_color)
    with open('config.ini', 'w') as config_file:
        config.write(config_file)

def set_language():
    """change interface language"""
    global language
    print(language)
    mb.showinfo(set_lang('Language change'), f'{set_lang('Reboot the application to change settings')}!')
    save_config(lang_check.get())

def open_about():
    """open window with 'about' information"""
    about_window = tk.Toplevel()
    about_window.grab_set()
    about_window.title(f'{set_lang('About')}')
    about_window.geometry('+590+370')
    about_window.resizable(False, False)

    with open(f'about_{language.lower()}.txt', 'r', encoding='utf8') as file:
        msg = file.read()
    label_tasks_todo = tk.Label(about_window, text=msg)
    label_tasks_todo.grid(row=1, column=0, padx=10, pady=10)

"""for setting program icon in the Windows taskbar"""
myappid = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

window = tk.Tk()

canvas_list = tk.LabelFrame(window)
canvas_list.pack(side=LEFT, fill = Y)

lang_check = tk.StringVar()
lang_check.set(language)

load_config()
load_csv('languages.csv')

mainmenu = tk.Menu(window, tearoff=0)
submenu = tk.Menu(mainmenu, tearoff=0)
submenu.add_radiobutton(label='Rus', variable=lang_check, value='Rus', command=set_language)
submenu.add_radiobutton(label='Eng', variable=lang_check, value='Eng', command=set_language)
mainmenu.add_cascade(label=set_lang('Language'), menu=submenu)
mainmenu.add_command(label=set_lang('About'), command=open_about)
window.config(menu=mainmenu)

window.geometry('780x500')
window.resizable(False, False)
window.iconbitmap(default="favicon.ico")

window.title(set_lang('Task list v2.2'))
label_list = tk.Label(canvas_list, text=set_lang('Task list'), font='Arial 11 bold')
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

label_textbox = tk.Label(canvas_create, text=set_lang('Enter a new task') + ':', font='Arial 9 bold')
label_textbox.grid(row=0, column=0, columnspan=4, padx=0, pady=10)
label_task_name = tk.Label(canvas_create, text=lang_str_split(set_lang('Task name'),' ')[0] + '\n' + lang_str_split(set_lang('Task name'),' ')[1] + ':')
label_task_name.grid(row=1, column=0, padx=20)
textbox_name = tk.Entry(canvas_create, width=30)
textbox_name.grid(row=1, column=1, columnspan=2, padx=5)
label_task_add = tk.Label(canvas_create, text=set_lang('Additional information') + ':')
label_task_add.grid(row=2, column=0, columnspan=3, padx=5)
textbox_add_info = tk.Entry(canvas_create, width=35)
textbox_add_info.grid(row=3, column=0, columnspan=3)

label_task_priority = tk.Label(canvas_create, text=lang_str_split(set_lang('Task priority'),' ')[0] + '\n' + lang_str_split(set_lang('Task priority'),' ')[1] + ':')
label_task_priority.grid(row=4, column=0)
list_priority = [set_lang('Low'), set_lang('Medium'), set_lang('High')]

priority_var = StringVar(value=list_priority[0])
label = ttk.Label(textvariable=priority_var)
combobox_priority = ttk.Combobox(canvas_create, state="readonly", textvariable=priority_var, values=list_priority, width=10)
combobox_priority.grid(row=4, column=1)
button_color = tk.Button(canvas_create, text=set_lang('Choose color'), width=13, height=1, command=choose_color)
button_color.grid(row=4, column=2, padx=10)

time_frame = tk.Frame(canvas_create, relief="solid")

enabled_time = IntVar()
time_checkbutton = ttk.Checkbutton(canvas_create, text=set_lang('Time'), variable=enabled_time)
time_checkbutton.grid(row=5, column=0)
hour = tk.Spinbox(time_frame,from_=0,to=23, wrap=True,width=4,justify=CENTER)
hour.grid(row=0, column=0)
minute = tk.Spinbox(time_frame,from_=0,to=59, wrap=True, width=4, justify=CENTER)
minute.grid(row=0, column=1)
time_frame.grid(row=5, column=1)

label_time = tk.Label(canvas_create, text=set_lang('Time:'))
label_time.grid(row=5, column=2, pady=5)
label_date = tk.Label(canvas_create, text=set_lang('Date:'))
label_date.grid(row=6, column=2, pady=5)

enabled_date = IntVar()
date_checkbutton = ttk.Checkbutton(canvas_create, text=set_lang('Date'), variable=enabled_date)
date_checkbutton.grid(row=6, column=0, pady=5)
chosen_date = tk.Entry(canvas_create)
chosen_date.grid(row=6, column=1, pady=0)
str_date = strftime('%d.%m.%Y')
chosen_date.insert(0, str_date)
chosen_date.bind('<1>', pick_date)

button_add = tk.Button(canvas_create, text=set_lang('Add task'), width=15, height=2, command=add_task)
button_add.grid(row=7, column=1, padx=0, pady=5)

canvas_actions = tk.LabelFrame(canvas_buttons)
canvas_actions.pack(side=TOP, fill = BOTH)

label_textbox_remove = tk.Label(canvas_actions, text=set_lang('Enter number or contained word:'))
label_textbox_remove.grid(row=0, column=0, columnspan=3, padx=0, pady=5)
textbox_insert = tk.Entry(canvas_actions, width=40)
textbox_insert.grid(row=1, column=0, columnspan=3, padx=0, pady=0)
button_remove = tk.Button(canvas_actions, text=set_lang('Delete by number'), width=15, height=1, command=remove_task)
button_remove.grid(row=2, column=0, padx=0, pady=5)
button_find_num = tk.Button(canvas_actions, text=set_lang('Search by number'), width=14, height=1, command=find_task_by_number)
button_find_num.grid(row=2, column=1, padx=0, pady=5)
button_set_completed = tk.Button(canvas_actions, text=set_lang('Complete by number'), width=18, height=1, command=complete_task)
button_set_completed.grid(row=3, column=0, padx=0, pady=5)
button_find_key = tk.Button(canvas_actions, text=set_lang('Search by word'), width=13, height=1, command=find_task_by_keyword)
button_find_key.grid(row=3, column=1, padx=0, pady=5)

button_remove_completed = tk.Button(canvas_actions, text=set_lang('Delete completed'), width=19, height=1, command=remove_all_completed)
button_remove_completed.grid(row=4, column=0, padx=0, pady=5)
button_rename = tk.Button(canvas_actions, text=set_lang('Rename'), width=15, height=1, command=rename_open)
button_rename.grid(row=4, column=1, padx=0, pady=5)

label_result = tk.Label(canvas_actions, text=set_lang('Result:'), font='Arial 9 bold')
label_result.grid(row=5, column=0, columnspan=3, padx=0, pady=5)
textbox_info = tk.Entry(canvas_actions, width=55)
textbox_info.grid(row=6, column=0, columnspan=3, padx=10, pady=5)

open_txt()
window.after(1000,check_time)
show_current_time()

window.mainloop()