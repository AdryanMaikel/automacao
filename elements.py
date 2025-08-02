from selenium.webdriver.common.by import By


class Element:
    def __init__(self, by: By, value: str):
        self.by = by
        self.value = value

    def __getitem__(self, item):
        return getattr(self, item)

    def __iter__(self):
        return iter(['by', 'value'])

    def keys(self):
        return ['by', 'value']

    def to_dict(self):
        return {
            "by": self.by,
            "value": self.value
        }


close_button = Element(By.CSS_SELECTOR, ".close-btn")
popup = Element(By.CLASS_NAME, "popup_parent")
stamina = Element(By.CSS_SELECTOR, ".generate-body .stamina .number")
goto_create = Element(By.CLASS_NAME, "painting")
textarea = Element(By.ID, "easyGenerateInput")
buttons_size_images = Element(By.CLASS_NAME,
                              ".panel-item-content-5 .panel-item")
text_size_image = Element(By.CLASS_NAME, "panel-item-label")
buttons_quantity_images = Element(By.CLASS_NAME,
                                  ".panel-item-content-4 .panel-item")
button_close_popup = Element(By.CLASS_NAME, "user-daily-close")

div_images = Element(By.CSS_SELECTOR, ".c-easy-msg-item")
text_type_creation = Element(By.CSS_SELECTOR,
                             ".msg-item-header-info-panel-tag")
text_date_images = Element(By.CSS_SELECTOR, ".easy-msg-item-time-box")
image_hover = Element(By.CSS_SELECTOR, ".image-hover-mask")
images = Element(By.CSS_SELECTOR, ".media-attachments-img")

scroll = Element(By.CSS_SELECTOR, ".c-easy-task-view-scroll-wrap")
gift = Element(By.CSS_SELECTOR, ".gift-btn")
claim = Element(By.CSS_SELECTOR, ".claim-button")
close_btn = Element(By.CSS_SELECTOR, ".dialog-manager .close-btn")
