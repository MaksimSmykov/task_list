def check_status(task):
    if task["completed"]:
        return 'Выполнено'
    else:
        return 'В процессе'

def convert_to_bool(str_):
    if str_ == 'True':
        return True
    else:
        return False

def print_common_info(entry, delete_start, delete_end, insert_start, insert_info):
    entry.delete(delete_start, delete_end)
    entry.insert(insert_start, insert_info)

