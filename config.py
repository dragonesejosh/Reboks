from filters import group_venue_filter
import webbrowser
import dateutil.parser as dateparser
from datetime import datetime

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

# Date format (for schedule): Sat%2C+28+Mar+2026

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
        if str(venue_id) not in group_venue_filter:
            raise ValueError(f"Venue id {venue_id} not found in list of venues.")
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
    
    def _parse_date(self, date_str):
        """
        e.g. 28 Mar, 28 Mar 2026 -> Sat%2C+28+Mar+2026
        """
        return dateparser.parse(date_str).date().strftime('%a%%2C+%d+%b+%Y')
    
    def _unparse_date(self, date_str):
        """
        e.g. Sat%2C+28+Mar+2026 -> 28 Mar 2026
        """
        return datetime.strptime(date_str, '%a%%2C+%d+%b+%Y').strftime('%d %b %Y')
        #return dateparser.parse(date_str, format='%a%%2C+%d+%b+%Y').date().strftime('%d %b %Y')

    def set_date(self, date_from, date_to=None):
        """
        e.g. 28 Mar, 28 Mar 2026
        """
        # Parse the date strings into datetime objects -> Sat%2C+28+Mar+2026
        parsed_date_from = self._parse_date(date_from)
        self.data['date_filter_from'] = parsed_date_from
        if date_to:
            self.data['date_filter_to'] = self._parse_date(date_to)
        else:
            self.data['date_filter_to'] = self.data['date_filter_from']
        print(self.data['date_filter_from'])
        print(self.data['date_filter_to'])
        return self
    
    def _parse_time(self, time_str):
        """
        e.g. 8 AM, 08:00 AM -> 08%3A00+AM
        """
        return dateparser.parse(time_str).time().strftime('%I%%3A%M+%p')
    
    def _unparse_time(self, time_str):
        """
        e.g. 08%3A00+AM -> 08:00 AM
        """
        return datetime.strptime(time_str, '%I%%3A%M+%p').strftime('%I:%M %p')
        #return dateparser.parse(time_str, format='%I%%3A%M+%p').time().strftime('%I:%M %p')

    def set_time(self, time_from, time_to):
        """
        e.g. 8 AM, 08:00 AM
        """
        self.data['time_filter_from'] = self._parse_time(time_from)
        self.data['time_filter_to'] = self._parse_time(time_to)
        return self

    def open_booking(self):
        """
        Search for available booking on Reboks.
        """
        webbrowser.open(self.booking_url())

    def booking_url(self):
        """
        Return the group booking URL for this configuration.
        """
        return group_booking + '&'.join(f"{k}={v}" for (k, v) in self.data.items())

    def open_schedule(self):
        """
        Search for the current bookings by others on Reboks.
        """
        webbrowser.open(self.schedule_url())

    def schedule_url(self):
        """
        Return the schedule URL for this configuration.
        """
        d2 = {
            'venue_id': self.data['group_venue_filter'],
            'date_from': self.data['date_filter_from'],
            'date_to': self.data['date_filter_to']
        }
        return schedule + '&'.join(f"{k}={v}" for (k, v) in d2.items())
    
    def get_venue(self):
        return group_venue_filter[self.data['group_venue_filter']]
    
    def get_day(self):
        if 'day_filter' not in self.data:
            return 'Any'
        return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][int(self.data['day_filter']) - 1]
    
    def get_date(self):
        if self.data['date_filter_from'] == self.data['date_filter_to']:
            return self._unparse_date(self.data['date_filter_from'])
        return self._unparse_date(self.data['date_filter_from']) + " to " + self._unparse_date(self.data['date_filter_to'])
    
    def get_time(self):
        return self._unparse_time(self.data['time_filter_from']) + " to " + self._unparse_time(self.data['time_filter_to'])

    def __str__(self):
        return f"""Venue:\t{self.get_venue()}
Day:\t{self.get_day()}
Date:\t{self.get_date()}
Time:\t{self.get_time()}"""
