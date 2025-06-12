from typing import Union

from json import load, dump


class Profile:
    def __init__(self, name, profile, sizeimg, prompt, credits):
        self.name = name
        self.profile = profile
        self.sizeimg = sizeimg
        self.prompt = prompt
        self.credits = credits

    def __repr__(self):
        return self.name

    def to_dict(self):
        return {"name": self.name,
                "profile": self.profile,
                "sizeimg": self.sizeimg,
                "prompt": self.prompt,
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


if __name__ == "__main__":
    chrome_config = ChromeConfig(
        path=r"C:\Users\NGS\AppData\Local\Google\Chrome\User Data",
        profiles=[
            {"name": "Adryan", "profile": "Profile 15"},
            {"name": "Airton", "profile": "Profile 16"},
        ],
    )
    print(chrome_config.to_dict())
