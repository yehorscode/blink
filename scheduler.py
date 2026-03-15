import asyncio
from config import Config, Playlist, Interrupt
from datetime import datetime
# values
interrupt_queue: list[dict] = []

def push_interrupt(plugin: str, duration: int):
    """
    Adds an immediate interrupt for a duration in seconds
    """
    expires = datetime.now().timestamp() + duration
    interrupt_queue.append({
        "plugin": plugin,
        "expires": expires
    })
    interrupt_queue.sort(key=lambda x: x["expires"])

def get_active_interrupt(config: Config) -> Interrupt | None:
    """
    Gets (if exists) an active interrupt that's happening now in a config
    """
    now = datetime.now().timestamp()

    for i in interrupt_queue:
        if i["expires"] < now:
            return None
    active_interrupts = []
    for i in interrupt_queue:
        if i["expires"] > now:
            active_interrupts.append(i)
    interrupt_queue[:] = active_interrupts

    if not interrupt_queue: # if its empty
        return None

    active_plugin = interrupt_queue[0]["plugin"]

    matches = []
    for match in config.interrupts:
        if match.plugin == active_plugin:
            matches.append(match)

    if matches:
        return matches[0]

    return None

def playlist_matches(playlist: Playlist) -> bool:
    """
    Checks if a playlist matches current time
    """
    now = datetime.now()
    current_day = now.strftime("%a").lower()
    current_time = now.strftime("%H:%M")

    if playlist.days and current_day not in playlist.days:
        return False
    if playlist.time_from and current_time < playlist.time_from:
        return False
    if playlist.time_to and current_time > playlist.time_to:
        return False
    return True

def get_current_display(config: Config) -> dict:
    """Gets what to display now
    """
    interrupt = get_active_interrupt(config)
    if interrupt:
        return {
            "mode": "interrupt",
            "plugin": interrupt.plugin,
            "duration": interrupt.duration
        }
    for playlist in config.playlists:
        if playlist_matches(playlist):
            result = {"mode": playlist.mode, "refresh": playlist.refresh, "name": playlist.name}
            if playlist.mode == "full":
                result["plugin"] = playlist.plugin
            elif playlist.mode == "split":
                result["left"] = playlist.left
                result["right"] = playlist.right
            return result

    return {"mode":"full","plugin":"dummy","refresh":60,"name":"Dummy"}

async def run_scheduler(config: Config, on_update):
    """Initialises the scheduler"""
    current = None
    last_update_ts = 0.0

    while True:
        display = get_current_display(config)
        now = datetime.now().timestamp()

        refresh_s = display.get("refresh", 60)
        changed = display != current
        expired = (now - last_update_ts) >= refresh_s

        if changed or expired:
            current = display
            last_update_ts = now
            await on_update(display)

        await asyncio.sleep(1)
