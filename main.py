from PIL import Image, ImageDraw, ImageFont
from display import get_display
import os
from utils.draw_utils import wrap_text
from config import load_config, load_plugins
from scheduler import run_scheduler
import asyncio
from extensions import REGISTRY
from PIL import Image
# # values
# serif_font = "/home/yehors/blink/fonts/literata.ttf"
# sans_font = "/home/yehors/blink/fonts/googlesans.ttf"

# title_font = ImageFont.truetype(serif_font, 20)
# body_font = ImageFont.truetype(sans_font, 13)

# display = get_display()
# display.init()

# img = display.get_canvas()
# img.paste((220,218,210), (0, 0, img.width, img.height))
# draw = ImageDraw.Draw(img)

# title_text = "Big title with long text. Just pretend its long"
# body_text = "Smaller text"
# max_text_width = img.width - 20

# title_lines = wrap_text(title_text, title_font, max_width=max_text_width)
# y = 10
# for line in title_lines:
#     draw.text((10, y), line, font=title_font, fill=0)
#     y += title_font.size + 4

# y += 6
# draw.text((10, y), body_text, fill=0, font=body_font)

# display.display(img)

# if os.getenv("EINK_EMULATE", "1") != "0":
#     display.wait(10)

# display.sleep()

async def main():
    config = load_config()
    plugin_configs = load_plugins()
    display = get_display()
    display.init()

    async def on_update(current):
        mode = current["mode"]

        if mode == "full":
            plugin_name = current["plugin"]
            plugin = REGISTRY[plugin_name](
                config=plugin_configs.get(plugin_name, {}),
                width=400,
                height=290,
            )
            await plugin.update()
            img = await plugin.render()
            
        elif mode == "split":
            img = Image.new("RGB", (400, 290), (255, 255, 255))

            left_name = current["left"]
            left = REGISTRY[left_name](
                config=plugin_configs.get(left_name, {}),
                width=200,
                height=290,
            )
            await left.update()
            
            right_name = current["right"]
            right = REGISTRY[right_name](
                config=plugin_configs.get(right_name, {}),
                width=200,
                height=290,
            )
            await right.update()
            img.paste(await left.render(), (0, 0))
            img.paste(await right.render(), (200, 0))
        else:
            # Ignore unsupported modes to avoid using an uninitialized image.
            return

        display.display(image=img)

    await run_scheduler(config, on_update=on_update)

asyncio.run(main())