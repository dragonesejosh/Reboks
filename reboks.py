from config import Config

group_booking = "https://reboks.nus.edu.sg/nus_public_web/public/index.php/facilities/group_booking?"
schedule = "https://reboks.nus.edu.sg/nus_public_web/public/index.php/facilities/booking_schedule?"

A = {}

base = Config(1).set_date("28 Mar").set_time("8 AM", "3 PM")
A['field'] = Config(8, base)
A['bball'] = Config(2, base)
#place all mpsh venues
for i, ven in zip((1, 2, 4, 5, 6), (12, 13, 14, 15, 16)):
    A[f'mpsh{i}'] = Config(ven, base)
A['track'] = Config(7, base)
A['usc'] = Config(40, base)
A['courts'] = Config(5, base)

import sys
if __name__ == "__main__":
    for name in sys.argv[1:]:
        config = A.get(name, None)
        if config is None:
            config = Config(int(name), base)
        print(config)
        print()
        config.open_booking()
        config.open_schedule()