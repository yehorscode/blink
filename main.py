from PIL import Image, ImageDraw, ImageFont
from display import get_display
import os

display = get_display()
display.init()

img = Image.new("RGB", (400, 300), (255, 255, 255))
draw = ImageDraw.Draw(img)
draw.text((10, 10), "This is how the text will look", fill=0, font=ImageFont.truetype("/home/yehors/blink/fonts/literata.ttf", 20))
draw.text((10, 40), "This is how the text will look", fill=0, font=ImageFont.truetype("/home/yehors/blink/fonts/literata.ttf", 10))

display.display(img)

if os.getenv("EINK_EMULATE", "1") != "0":
    display.wait(10)

display.sleep()