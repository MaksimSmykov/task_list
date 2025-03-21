<h1 align="center">
  <img src="screenshot.png" width="782px" height="552px" alt="Task list">
</h1>

# Task list (Python 3.12, Tkinter)

## Instructions

### Launch
> Before launching, make sure that all project files are in the same
> folder, next to the `task_list.exe` file:
> - `about_eng.txt`
> - `about_rus.txt`
> - `config.ini`
> - `favicon.ico`
> - `languages.csv`

### Adding tasks
> The `Task name` field is required to add a task.
> Also, do not forget to specify the `Task priority`, because this parameter will be specified automatically based on the selected item.
> The `Additional information`, `Time` and `Date` fields are optional. 
> The `Choose color` button allows you to select a color for all high priority tasks at once.

### Setting up the calendar when editing a project
> The calendar does not work correctly on python 3.12. To fix this, in the file at the path:
> 
> `\.venv\Lib\site-packages\tkcalendar\calendar_.py` you need to write the import:
> - `import calendar`
> - `from babel.dates import format_date, parse_date, get_day_names, get_month_names`
> - `from babel.numbers import * `
