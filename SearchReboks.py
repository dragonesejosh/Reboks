from Filters import filters

opp_filters = [dict(zip(d.values(), d.keys())) for d in filters]

group_booking = "https://reboks.nus.edu.sg/nus_public_web/public/index.php/facilities/group_booking?"
schedule = "https://reboks.nus.edu.sg/nus_public_web/public/index.php/facilities/booking_schedule?"

def stats(d):
    print(filters[3][d['group_venue_filter']])

def search_booking(d):
    url = group_booking + '&'.join(f"{k}={v}" for (k, v) in d.items())
    return url

def get_schedule(d):
    d2 = {
        'venue_id': d['group_venue_filter'],
        'date_from': d['date_filter_from'],
        'date_to': d['date_filter_to']
    }
    return schedule + '&'.join(f"{k}={v}" for (k, v) in d2.items())

base = {
    'group_filter_one': '94', #Sports
    'group_filter_two': '108', #Other Sports Activity
    'group_activity_filter': '246', #Other Sports Activity
    'group_venue_filter': '',
    'group_subvenue_filter': '',
    
    #'day_filter': '2', # 1:Monday - 6:Saturday
    'date_filter_from': 'Sat%2C+28+Mar+2026', #Date From
    'date_filter_to': 'Sat%2C+28+Mar+2026', #Date To
    'time_filter_from': '08%3A00+AM', #Time From
    'time_filter_to': '03%3A00+PM', #Time To
    
    'search': 'Search'
}

A = {}
def place(name, venue, subvenue=-1):
    """
    name = Identifier
    venue = #ID of Venue
    subvenue = #ID of Subvenue (-1 for all)
    """
    A[name] = base.copy()
    A[name].update({'group_venue_filter': str(venue)})
    if subvenue != -1:
        A[name].update({'group_subvenue_filter': str(subvenue)})

place('field', 8)
place('bball', 2)
#place all mpsh venues
for i, ven in zip((1, 2, 4, 5, 6), (12, 13, 14, 15, 16)):
    place(f'mpsh{i}', ven)
place('track', 7)
place('usc', 40)
place('courts', 5)

import webbrowser

def opend(d):
    stats(d)
    webbrowser.open(search_booking(d))
    webbrowser.open(get_schedule(d))

import sys
if __name__ == "__main__":
    for name in sys.argv[1:]:
        print(name.upper())
        try:
            place(name, int(name))
        except:
            pass
        opend(A[name])
