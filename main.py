from PIL import Image, ImageDraw, ImageFont
from display import get_display
import os

display = get_display()
display.init()

img = Image.new("RGB", (400, 300), (255, 255, 255))
draw = ImageDraw.Draw(img)
draw.text((10, 10), "Big title with long text. Just pretend its long", fill=0, font=ImageFont.truetype("/home/yehors/blink/fonts/literata.ttf", 20))
# draw.text((10, 40), "Smaller text", fill=0, font=ImageFont.truetype("/home/yehors/blink/fonts/literata.ttf", 10))
draw.text((10, 50), "Smaller text", fill=0, font=ImageFont.truetype("/home/yehors/blink/fonts/googlesans.ttf", 13))
# draw.text((10, 60), "Smaller text", fill=0, font=ImageFont.truetype("/home/yehors/blink/fonts/minecraftia.ttf", 10))

display.display(img)

if os.getenv("EINK_EMULATE", "1") != "0":
    display.wait(10)

display.sleep()