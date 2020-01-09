"""
Define a custom theme for Inquirer
"""

inquirer_theme = {
    "Question": {
        "mark_color": "yellow",
        "brackets_color": "normal",
        "default_color": "normal",
    },
    "Editor": {
        "opening_prompt_color": "bright_black",
    },
    "Checkbox": {
        "selection_color": "normal",
        "selection_icon": '>',
        "selected_icon": '[x]',
        "selected_color": "bold_yellow",
        "unselected_color": "normal",
        "unselected_icon": '[ ]',
    },
    "List": {
        "selection_color": "blue",
        "selection_cursor": ">",
        "unselected_color": "normal",
    }
}
