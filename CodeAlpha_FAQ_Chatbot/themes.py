LIGHT_THEME = {
    "bg": "#FFF0F5",
    "chat_bg": "#FFF9FB",
    "input_bg": "#FFFFFF",
    "text": "#57323F",
    "secondary_text": "#9B7180",
    "primary": "#C95C80",
    "primary_light": "#FFD9E5",
    "user": "#8A5A9E",
    "border": "#F3CAD7",
    "button_text": "#C95C80"
}


DARK_THEME = {
    "bg": "#241B20",
    "chat_bg": "#30242A",
    "input_bg": "#3A2C33",
    "text": "#F8EAF0",
    "secondary_text": "#C9AAB7",
    "primary": "#E98AA8",
    "primary_light": "#5A3745",
    "user": "#C5A0D8",
    "border": "#5B414B",
    "button_text": "#F8D4E0"
}


def get_theme(mode):
    if mode == "dark":
        return DARK_THEME.copy()

    return LIGHT_THEME.copy()