from seaart import (
    chrome,
    sleep,
    get_chrome,
    close_chrome_if_it_is_running,
    # click_element,
    download_image
)
from elements import Element, By
from organizar import organizar_fotos

prompt = str()
with open("config/prompt.txt", "r") as f:
    prompt = f.read()


def download_images_krea(profilename: str):
    driver.get("https://www.krea.ai/image")
    sleep(3)
    try:
        driver.execute_script('''\
document.querySelector(
    "body > div > main > div > div > div > div > div > div > \
button:nth-child(2)"
).click()''')
    except Exception:
        return

    input("Baixar imagem?")
    images = driver.find_elements(By.CSS_SELECTOR, "img.object-contain")
    for i, image in enumerate(images):
        image_url = image.get_attribute("src")
        # print(image_url)
        download_image(image_url, f"{i}", profilename)
    organizar_fotos("img")


if __name__ == "__main__":
    for profile in chrome.profiles:
        close_chrome_if_it_is_running()
        driver = get_chrome(profile)
        download_images_krea(profile.name)
        input("continuar?")
        continue
        driver.execute_script('''\
document.querySelector(
    "main > div > div > div > div > div > div > div > div > div > div > div > \
div > div > div > div > button:nth-child(6) > div"
).click()''')
        

        textarea = driver.find_element(By.ID, "prompt")
        if textarea.get_attribute("value"):
            textarea.clear()
        textarea.send_keys(prompt)

        button_create = Element(
            By.CSS_SELECTOR,
            "main > div > div > div > div > div > div > div > div > button"
            )
        # click_element(driver, **button_create)

        input("driver :")

    pass
