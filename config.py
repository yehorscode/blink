import tomllib
from dataclasses import dataclass

@dataclass
class WebUI:
    ip: str
    login: str
    password: str

@dataclass
class Sidebar:
    plugin: str

@dataclass
class Playlist:
    name: str
    mode: str
    plugin: str | None = None
    left: str | None = None
    right: str | None = None
    refresh: int = 60
    days: list[str] | None = None
    time_from: str | None = None
    time_to: str | None = None

@dataclass
class Interrupt:
    plugin: str
    priority: int
    duration: int
    mode: str

@dataclass
class Looks:
    text_color: str

@dataclass
class Config:
    web_ui: WebUI
    sidebar: Sidebar
    playlists: list[Playlist]
    interrupts: list[Interrupt]
    looks: Looks



def load_config(path="config.toml") -> Config:
    with open(path, "rb") as f:
        raw_config = tomllib.load(f)
    
    return Config(
        web_ui=WebUI(**raw_config["web_ui"]),
        sidebar=Sidebar(**raw_config["sidebar"]),
        playlists=[Playlist(**p) for p in raw_config["playlists"]],
        interrupts=[Interrupt(**i) for i in raw_config["interrupts"]],
        looks=Looks(**raw_config["looks"])
    )

def load_plugins(path="plugins.toml") -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)