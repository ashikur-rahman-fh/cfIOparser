from termcolor import colored

def colored_text(text, color, attrs = None):
    return colored(text, color = color, attrs = attrs)
