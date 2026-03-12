import urllib.parse as parse
from filters import filters
import webbrowser

group_booking = "https://reboks.nus.edu.sg/nus_public_web/public/index.php/facilities/group_booking?"
schedule = "https://reboks.nus.edu.sg/nus_public_web/public/index.php/facilities/booking_schedule?"

"""
data = {
        'group_filter_one': '94', #Sports
        'group_filter_two': '108', #Other Sports Activity
        'group_activity_filter': '246', #Other Sports Activity
        #'group_venue_filter': '',
        'group_subvenue_filter': '',
        
        #'day_filter': '2', # 1:Monday - 6:Saturday
        #'date_filter_from': 'Sat%2C+28+Mar+2026', #Date From
        #'date_filter_to': 'Sat%2C+28+Mar+2026', #Date To
        #'time_filter_from': '08%3A00+AM', #Time From
        #'time_filter_to': '03%3A00+PM', #Time To
        
        'search': 'Search'
    }
"""

class Config:
    data = {
        'group_filter_one': '94', #Sports
        'group_filter_two': '108', #Other Sports Activity
        'group_activity_filter': '246', #Other Sports Activity
        'group_subvenue_filter': '',
        'search': 'Search'
    }

    def __init__(self, venue_id:int, config_base=None):
        if config_base:
            self.data = config_base.data.copy()
        self.set_venue(venue_id)

    def set_venue(self, venue_id):
        """
        Set the venue by id.
        """
        self.data['group_venue_filter'] = str(venue_id)
        return self

    def set_day(self, day=None):
        """
        1:Monday - 6:Saturday

        Use with no params to search for all days.
        """
        if day is None:
            self.data.pop('day_filter', None)
            return
        self.data['day_filter'] = str(day)
        return self

    def set_date(self, date_from, date_to=None):
        """
        e.g. 28 Mar, 28 Mar 2026
        """
        self.data['date_filter_from'] = parse.quote(date_from)
        if date_to:
            self.data['date_filter_to'] = parse.quote(date_to)
        else:
            self.data['date_filter_to'] = parse.quote(date_from)
        return self
    
    def set_time(self, time_from, time_to):
        """
        e.g. 08:00 AM, 8 AM
        """
        self.data['time_filter_from'] = parse.quote(time_from)
        self.data['time_filter_to'] = parse.quote(time_to)
        return self

    def open_booking(self):
        """
        Search for available booking on Reboks.
        """
        url = group_booking + '&'.join(f"{k}={v}" for (k, v) in self.data.items())
        webbrowser.open(url)

    def open_schedule(self):
        """
        Search for the current bookings by others on Reboks.
        """
        d2 = {
            'venue_id': self.data['group_venue_filter'],
            'date_from': self.data['date_filter_from'],
            'date_to': self.data['date_filter_to']
        }
        url = schedule + '&'.join(f"{k}={v}" for (k, v) in d2.items())
        webbrowser.open(url)
    
    def _filter(self, filter_type, filter_id):
        return filters[filter_type].get(self.data[filter_id], 'Unknown')

    def __str__(self):
        return f"""Venue:\t{self._filter(3, 'group_venue_filter')}
Day:\t{self._filter(4, 'day_filter') if 'day_filter' in self.data else 'Any'}
Date:\t{parse.unquote(self.data['date_filter_from'])} to {parse.unquote(self.data['date_filter_to'])}
Time:\t{parse.unquote(self.data['time_filter_from'])} to {parse.unquote(self.data['time_filter_to'])}"""