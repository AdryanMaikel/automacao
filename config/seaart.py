from selenium.webdriver.common.by import By

BY = {
    "class": By.CLASS_NAME,
    "id": By.ID,
    "xpath": By.XPATH,
    "css": By.CSS_SELECTOR,
    "name": By.NAME
}


class SeaartConfig:
    def __init__(self,
                 url: str,
                 popup: dict[str, str],
                 textarea: dict[str, str],
                 credits: dict[str, str],
                 sizesimg: list[str]):
        self.url = url
        self.popup = self.dict_element(popup)
        self.textarea = self.dict_element(textarea)
        self.credits = self.dict_element(credits)
        self.sizesimg = sizesimg

    def __repr__(self):
        return self.url

    def dict_element(self, element: dict[str, str]) -> dict[str, str]:
        return {"by": BY.get(element.get("by", By.ID)),
                "value": element.get("value")}

    def to_dict(self):
        buttons = [button.to_dict() for button in self.buttons]
        return {"url": self.url, "popup": self.popup, "buttons": buttons,
                "generate": self.generate,
                "textarea": self.textarea, "credits": self.credits}

    def update_json_config(self):
        save_json("seaart.json", self.to_dict())

    def get_textarea(self):
        return tuple(self.textarea.values())