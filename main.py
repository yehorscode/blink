from display import get_display
from config import load_config, load_plugins
from scheduler import run_scheduler
import asyncio
import inspect
from extensions import REGISTRY
from PIL import Image
from extensions.status_bar import StatusBar

async def main():
    config = load_config()
    plugin_configs = load_plugins()
    display = get_display()
    display.init()
    canvas_width = 250
    canvas_height = 122
    # status_bar = StatusBar(width=canvas_width)
    content_height = canvas_height # - status_bar.height

    def create_plugin(plugin_name, width, height):
        plugin_cls = REGISTRY[plugin_name]
        kwargs = {
            "config": plugin_configs.get(plugin_name, {}),
            "width": width,
            "height": height,
        }

        signature = inspect.signature(plugin_cls.__init__)
        supports_var_kwargs = any(
            parameter.kind == inspect.Parameter.VAR_KEYWORD
            for parameter in signature.parameters.values()
        )
        # if supports_var_kwargs or "status_bar" in signature.parameters:
            # kwargs["status_bar"] = status_bar

        return plugin_cls(**kwargs)

    async def on_update(current):
        mode = current["mode"]
        # status_bar.clear()

        if mode == "full":
            plugin_name = current["plugin"]
            plugin = create_plugin(plugin_name, width=canvas_width, height=content_height)
            await plugin.update()
            img = Image.new("RGB", (canvas_width, canvas_height), (255, 255, 255))
            img.paste(await plugin.render(), (0, 0))
            
        elif mode == "split":
            img = Image.new("RGB", (canvas_width, canvas_height), (255, 255, 255))

            left_name = current["left"]
            left = create_plugin(left_name, width=200, height=content_height)
            await left.update()
            
            right_name = current["right"]
            right = create_plugin(right_name, width=200, height=content_height)
            await right.update()
            img.paste(await left.render(), (0, 0))
            img.paste(await right.render(), (200, 0))
        else:
            # Ignore unsupported modes to avoid using an uninitialized image.
            return

        # img.paste(status_bar.render(), (0, content_height))

        display.display(image=img)

    await run_scheduler(config, on_update=on_update)

asyncio.run(main())