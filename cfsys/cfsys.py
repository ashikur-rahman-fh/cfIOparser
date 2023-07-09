"""
    File: cfsys.py
    Author: Ashikur Rahman
    Descriptin: Intends to provide system functionalities
"""

from datetime import datetime
from colorer.colorer import colored_text

def get_current_time():
    """Returns the current system time"""
    current_dt = datetime.now()
    datetime_str = current_dt.strftime('%Y-%m-%d %H:%M:%S')

    colored_date_time_str = colored_text(datetime_str, color='magenta')

    return colored_date_time_str
