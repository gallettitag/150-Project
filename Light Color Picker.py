import time

import Weather_Getter
import time
import board
import neopixel
from adafruit_magtag.magtag import MagTag

from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.group import AnimationGroup


# =============== CUSTOMISATIONS ================
# The strip LED brightness, where 0.0 is 0% (off) and 1.0 is 100% brightness, e.g. 0.3 is 30%
import config

lat = 39.4833
long = -87.3241


strip_pixel_brightness = 1
# The MagTag LED brightness, where 0.0 is 0% (off) and 1.0 is 100% brightness, e.g. 0.3 is 30%.
magtag_pixel_brightness = 0.5

# The rate interval in seconds at which the Cheerlights data is fetched.
# Defaults to one minute (60 seconds).
refresh_rate = 60

# Set up where we'll be fetching data from
DATA_SOURCE = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={config.weather_api}"
TEMP_LOCATION = ['main']['temp']
CONDITIONS_LOCATION = ['weather']['main']

magtag = MagTag(
    url=DATA_SOURCE,
    json_path=(TEMP_LOCATION, CONDITIONS_LOCATION),
)
magtag.network.connect()

print(magtag.fetch()[0])

strip_pixels = neopixel.NeoPixel(board.D10, 30, brightness=strip_pixel_brightness)
magtag_pixels = magtag.peripherals.neopixels
magtag_pixels.brightness = magtag_pixel_brightness

def pick_color():
    current_temp = Weather_Getter.get_temp()
    color = ()
    print(current_temp)

    if current_temp < 10:
        color = (135, 206, 235)
    elif current_temp < 39:
        color = (7, 42, 108)
    elif current_temp > 59:
        color = (0, 255, 255)
    elif current_temp > 80:
        color = (79, 121, 66)
    else:
        color = (102, 0, 0)

    print(color)
    return color


timestamp = None
while True:
    if not timestamp or ((time.monotonic() - timestamp) > refresh_rate):  # Refresh rate in seconds
        try:
            # Turn on the MagTag NeoPixels.
            magtag.peripherals.neopixel_disable = False

            weather_data = magtag.fetch()

            color = pick_color(weather_data[0] * 1.8 - 459.67)

            conditions = weather_data[1]

            if conditions in ("rain", "snow", "sleet"):
                animations = AnimationSequence(
                    AnimationGroup(
                        Sparkle(magtag_pixels, speed=0.1, color=color, num_sparkles=1),
                        Sparkle(strip_pixels, speed=0.01, color=color, num_sparkles=15),
                    )
                )
            elif conditions is "Clear":
                animations = AnimationSequence(
                    AnimationGroup(
                        Blink(magtag_pixels, speed=0.5, color=color),
                        Blink(strip_pixels, speed=0.5, color=color),
                    )
                )
            elif conditions is "Clouds":
                magtag_pixels.fill(color)
                strip_pixels.fill(color)
            elif conditions is "high winds":
                animations = AnimationSequence(
                    AnimationGroup(
                        Comet(magtag_pixels, 0.3, color=color, tail_length=3),
                        Comet(strip_pixels, 0.05, color=color, tail_length=15),
                    )
                )

            timestamp = time.monotonic()

        except (ValueError, RuntimeError) as e:
            # Catch any random errors so the code will continue running.
            print("Some error occured, retrying! -", e)
    try:
        # This runs the animations.
        animations.animate()
    except NameError:
        # If Cheerlights adds a color not included above, the code would fail. This allows it to
        # continue to retry until a valid color comes up.
        print("There may be a Cheerlights color not included above.")


