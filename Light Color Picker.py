import time

import Temp_Getter

def pick_color():
    current_temp = Temp_Getter.get_temp()
    color = ''

    if current_temp < 40:
        color = '0000CC'
    elif current_temp < 65:
        color = '#82eaff'
    elif current_temp > 80:
        color = '#ff8352'
    else:
        color = '#ff2626'

    print(color)
    return color

while True:
    pick_color()
    time.sleep(5)
