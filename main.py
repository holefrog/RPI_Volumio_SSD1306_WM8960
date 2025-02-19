import time
import os
import logging
import sys
from query import get_player_status, extract_result_field
from display import display_text, set_brightness, turn_off_display, turn_on_display

# Logging level
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler("./SSD1306.log"),
        logging.StreamHandler() 
    ]
)

# Timeout constants for dimming and turning off the screen (in seconds)
DIM_SCREEN_TIMEOUT = 5
TURN_OFF_SCREEN_TIMEOUT = 900

# Flags to track current display state
is_off = False
is_dimmed = False
start_time = time.time()  # Record the time of the last content change

# Separate tracking for content state and time updates
last_content_state = None
last_displayed_time = None  # To prevent flicker by avoiding frequent updates

def is_volumio_booted():
    # Check if Volumio is booted by sending a request to the local server
    response = os.system("curl -s http://localhost:3000 > /dev/null")
    return response == 0

# Wait until Volumio is fully booted
logging.info("Display: Booting, Wait")
while not is_volumio_booted():
    display_text("Booting", "Wait", large_font=True)
    time.sleep(1)

# Display "Volumio Ready" for 5 seconds
display_text("Volumio", "Ready", large_font=True)
logging.info("Display: Volumio, Ready")
time.sleep(5)

# Main loop: display player status and song information
logging.info("Main loop began.")
while True:
    current_date = time.strftime("%Y-%m-%d", time.localtime())
    current_time = time.strftime("%H:%M:%S", time.localtime())

    # Retrieve power status
    error, result = get_player_status(["power", "?"])
    power = extract_result_field(result, "_power", default=0)

    # Display information based on power status and playback mode
    if power == 0:
        # Power off: display date and time (update only when seconds change)
        content_state = ("power_off",)
        if current_time != last_displayed_time:
            display_text(current_date, current_time, large_font=True, scroll_speed=0)
            last_displayed_time = current_time

    else:
        error, result = get_player_status(["mode", "?"])
        playback_mode = extract_result_field(result, "_mode", default="stop")

        if playback_mode == "stop":
            content_state = ("Stopped",)
            if current_time != last_displayed_time:
                display_text("Stopped", current_time, large_font=True, scroll_speed=0)
                last_displayed_time = current_time

        elif playback_mode == "pause":
            content_state = ("Paused",)
            if current_time != last_displayed_time:
                display_text("Paused", current_time, large_font=True, scroll_speed=0)
                last_displayed_time = current_time

        elif playback_mode == "play":
            # In play mode, update the display only when the song or artist changes to avoid flicker
            error, result = get_player_status(["current_title", "?"])
            track_title = extract_result_field(result, "_current_title", default="")
            error, result = get_player_status(["artist", "?"])
            artist = extract_result_field(result, "_artist", default="")
            content_state = ("play", artist, track_title)

            if content_state != last_content_state:
                display_text(artist, track_title, large_font=True, scroll_speed=0.00625)
                last_displayed_time = None  # Reset time tracking when content changes

        else:
            content_state = ("Unknown",)
            if current_time != last_displayed_time:
                display_text(current_date, current_time, large_font=True, scroll_speed=0)
                last_displayed_time = current_time

    # If the content state has changed, reset the inactivity timer
    if content_state != last_content_state:
        last_content_state = content_state
        start_time = time.time()
        is_dimmed = False
        if is_off:
            turn_on_display()
            is_off = False

    # Calculate elapsed time since the last content update
    elapsed = time.time() - start_time

    # Dim the screen after 5 seconds of inactivity
    if not is_dimmed and elapsed > DIM_SCREEN_TIMEOUT:
        set_brightness(8)  # Adjust brightness to the desired level
        is_dimmed = True

    # Turn off the screen after 900 seconds of inactivity
    if not is_off and elapsed > TURN_OFF_SCREEN_TIMEOUT:
        turn_off_display()
        is_off = True

    # Update the display every second for time refresh
    time.sleep(1)

