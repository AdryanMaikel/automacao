from typing import Union
from selenium.webdriver.common.by import By

from json import load, dump


def get_by(value: str) -> By:
    by_mapping = {
        "class name": By.CLASS_NAME,
        "id": By.ID,
        "xpath": By.XPATH,
        "css selector": By.CSS_SELECTOR,
        "name": By.NAME
    }
    return by_mapping.get(value, By.ID)


class Profile:
    def __init__(self, name, profile, sizeimg, prompt, credits):
        self.name = name
        self.profile = profile
        self.sizeimg = sizeimg
        self.prompt = prompt
        self.credits = credits

    def __repr__(self):
        return self.profile

    def to_dict(self):
        return {"name": self.name, "profile": self.profile,
                "sizeimg": self.sizeimg, "prompt": self.prompt,
                "credits": self.credits}


class ChromeConfig:
    def __init__(self, path: str,
                 path_downloads: str,
                 profiles: list[dict],
                 arguments: list[str]):
        self.path = path
        self.path_downloads = path_downloads
        self.profiles = [Profile(**profile) for profile in profiles]
        self.arguments = arguments

    def __repr__(self):
        return self.path

    def to_dict(self):
        profiles = [profile.to_dict() for profile in self.profiles]
        return {"path": self.path, "path_downloads": self.path_downloads,
                "profiles": profiles, "arguments": self.arguments}

    def update_json_config(self):
        save_json("chrome.json", self.to_dict())


class Button:
    def __init__(self, name: str, by: str, value: str):
        self.name = name
        self.by = get_by(by)
        self.value = value

    def __repr__(self):
        return (self.by, self.value)

    def to_dict(self):
        return {"name": self.name, "by": self.by, "value": self.value}


class SeaartConfig:
    def __init__(self,
                 url: str,
                 popup: dict[str, str],
                 buttons: list[dict],
                 textarea: dict[str, str],
                 credits: dict[str, str],
                 sizesimg: list[str]):
        self.url = url
        self.popup = {"by": get_by(popup.get("by")),
                      "value": popup.get("value")}
        self.buttons = [Button(**button) for button in buttons]
        self.textarea = {"by": get_by(textarea.get("by")),
                         "value": textarea.get("value")}
        self.credits = {"by": get_by(credits.get("by")),
                        "value": credits.get("value")}
        self.sizesimg = sizesimg

    def __repr__(self):
        return self.url

    def to_dict(self):
        buttons = [button.to_dict() for button in self.buttons]
        return {"url": self.url, "popup": self.popup, "buttons": buttons,
                "generate": self.generate,
                "textarea": self.textarea, "credits": self.credits}

    def update_json_config(self):
        save_json("seaart.json", self.to_dict())

    def get_textarea(self):
        return tuple(self.textarea.values())


def save_json(filename: str, data: Union[dict, list[dict]]):
    print("Salvando json: "+filename)
    try:
        with open(f"config/{filename}", "w", encoding="utf-8") as file:
            dump(data, file, indent=4, ensure_ascii=False)
    except Exception:
        print("Falha ao salvar json.")


with open("config/chrome.json", "r", encoding="utf-8") as file:
    chrome_data = load(file)
chrome = ChromeConfig(**chrome_data)

with open("config/seaart.json", "r", encoding="utf-8") as file:
    seaart_data = load(file)
seaart = SeaartConfig(**seaart_data)


if __name__ == "__main__":
    chrome_config = ChromeConfig(
        path=r"C:\Users\NGS\AppData\Local\Google\Chrome\User Data",
        profiles=[
            {"name": "Adryan", "profile": "Profile 15"},
            {"name": "Airton", "profile": "Profile 16"},
        ],
    )
    print(chrome_config.to_dict())

    seaart_config = SeaartConfig(
        url="https://www.seaart.ai/pt",
        buttons=[
            {"name": "create", "by": "class name", "value": "painting"},
        ],
        textarea={"by": "id", "value": "easyGenerateInput"},
    )
    print(seaart_config.to_dict())
