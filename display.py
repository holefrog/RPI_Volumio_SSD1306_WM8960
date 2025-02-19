import time
import threading
import logging
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont

# Create SSD1306 display instance (I2C address 0x3C, I2C bus 3)
disp = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_bus=3, i2c_address=0x3C)

# Initialize the display
disp.begin()
disp.clear()
disp.display()

# Load fonts
try:
    # Attempt to load the specified font files
    font_small = ImageFont.truetype("./msyh.ttf", 14)
    font_large = ImageFont.truetype("./msyh.ttf", 22)
except Exception as e:
    logging.error(f"An unknown error occurred: {e}, loading default font.")
    font_small = ImageFont.load_default()
    font_large = ImageFont.load_default()

# Define SSD1306 commands
SSD1306_SETCONTRAST = 0x81
SSD1306_DISPLAYOFF = 0xAE
SSD1306_DISPLAYON = 0xAF

def set_brightness(contrast_value):
    disp.command(SSD1306_SETCONTRAST)
    disp.command(contrast_value)

def turn_off_display():
    disp.command(SSD1306_DISPLAYOFF)

def turn_on_display():
    disp.command(SSD1306_DISPLAYON)
    set_brightness(255)

# Screen dimensions
width = disp.width
height = disp.height

# Global variables for scroll thread management
current_scroll_thread = None          # Reference to the current scrolling thread
scroll_stop_event = threading.Event() # Event to signal the scroll thread to stop

def scroll_text(top_text, bottom_text, large_font=False, scroll_speed=0.00625, stop_event=None):
    """
    Scroll the bottom text on the display while keeping the top text static.
    """
    # Create an initial image to compute text dimensions
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    
    # Select fonts
    top_font = font_small
    bottom_font = font_small if not large_font else font_large

    # Calculate top text position (centered in the top area of height 14)
    top_bbox = draw.textbbox((0, 0), top_text, font=top_font)
    top_width = top_bbox[2] - top_bbox[0]
    top_height = top_bbox[3] - top_bbox[1]
    top_x = (width - top_width) // 2
    # Adjust top_y: center in 14-pixel area and shift up by 1 pixel to avoid overlap
    top_y = (14 - top_height) // 2 - 1

    # Calculate bottom text width and set vertical position
    bottom_bbox = draw.textbbox((0, 0), bottom_text, font=bottom_font)
    bottom_text_width = bottom_bbox[2] - bottom_bbox[0]
    bottom_y = 20  # Bottom text starts at y = 20

    # Continuous scrolling loop until stop_event is set
    while not (stop_event and stop_event.is_set()):
        # Scroll from left edge (offset = 0) to the left limit
        for offset in range(0, -(bottom_text_width - width) - 1, -1):
            if stop_event and stop_event.is_set():
                break
            disp.clear()
            # Create a new image each iteration to avoid artifacts
            image = Image.new('1', (width, height))
            draw = ImageDraw.Draw(image)
            # Draw static top text
            draw.text((top_x, top_y), top_text, font=top_font, fill=255)
            # Draw scrolling bottom text at current offset
            draw.text((offset, bottom_y), bottom_text, font=bottom_font, fill=255)
            disp.image(image)
            disp.display()
            time.sleep(scroll_speed)

def display_text(top_text, bottom_text, large_font=False, scroll_speed=0.00625):
    """
    Display top and bottom texts on the LCD. If the bottom text is wider than the screen,
    it will be scrolled.
    """
    global current_scroll_thread, scroll_stop_event

    # If a scroll thread is already running, stop it
    if current_scroll_thread and current_scroll_thread.is_alive():
        scroll_stop_event.set()
        current_scroll_thread.join()
    scroll_stop_event.clear()

    # Create an image to measure bottom text width
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    bottom_font = font_small if not large_font else font_large
    bottom_bbox = draw.textbbox((0, 0), bottom_text, font=bottom_font)
    bottom_text_width = bottom_bbox[2] - bottom_bbox[0]

    if bottom_text_width > width:
        # Add spaces for a smooth scroll effect
        bottom_text = "  " + bottom_text + "  "
        bottom_bbox = draw.textbbox((0, 0), bottom_text, font=bottom_font)
        bottom_text_width = bottom_bbox[2] - bottom_bbox[0]

        # Clear display before starting scrolling
        disp.clear()
        disp.display()

        # Start a new scroll thread
        current_scroll_thread = threading.Thread(
            target=scroll_text,
            args=(top_text, bottom_text, large_font, scroll_speed, scroll_stop_event)
        )
        current_scroll_thread.start()
    else:
        # For static text, create a full image and update the display at once
        image = Image.new('1', (width, height))
        draw = ImageDraw.Draw(image)
        
        # Calculate top text position (centered in a 14-pixel-high area)
        top_font = font_small
        top_bbox = draw.textbbox((0, 0), top_text, font=top_font)
        top_width = top_bbox[2] - top_bbox[0]
        top_height = top_bbox[3] - top_bbox[1]
        top_x = (width - top_width) // 2
        top_y = (14 - top_height) // 2 - 1

        # Calculate bottom text position (centered horizontally)
        bottom_x = (width - bottom_text_width) // 2
        bottom_y = 20

        # Draw both texts onto the image
        draw.text((top_x, top_y), top_text, font=top_font, fill=255)
        draw.text((bottom_x, bottom_y), bottom_text, font=bottom_font, fill=255)

        # Update the display with the new image
        disp.image(image)
        disp.display()

