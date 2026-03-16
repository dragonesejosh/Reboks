from dateutil import parser
from datetime import datetime

def parse_date(date_str):
    """
    e.g. 28 Mar, 28 Mar 2026 -> Sat%2C+28+Mar+2026
    """
    return parser.parse(date_str).date().strftime('%a%%2C+%d+%b+%Y')
    
def unparse_date(date_str):
    """
    e.g. Sat%2C+28+Mar+2026 -> 28 Mar 2026
    """
    return datetime.strptime(date_str, '%a%%2C+%d+%b+%Y').strftime('%d %b %Y')

def parse_time(time_str):
    """
    e.g. 8 AM, 08:00 AM -> 08%3A00+AM
    """
    return parser.parse(time_str).time().strftime('%I%%3A%M+%p')
    
def unparse_time(time_str):
    """
    e.g. 08%3A00+AM -> 08:00 AM
    """
    return datetime.strptime(time_str, '%I%%3A%M+%p').strftime('%I:%M %p')