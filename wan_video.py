from config import chrome
from config.models import By
import seaart

from time import sleep


def gerar():
    """
    Gera imagens usando o SeaArt.
    """
    for _, profile in enumerate(chrome.profiles, start=1):
        driver = seaart.get_chrome(profile)
        driver.get("https://wan.video/wanxiang/videoCreation")
        sleep(3)
        driver.find_element(By.CSS_SELECTOR, ".gKLZVH").click()
        sleep(3)
        driver.execute_script("""\
const button = document.querySelector('.sign--bBKtUwB_');
if (!button.classList.contains('signDisabled--gOEHFhLD')) {
    button.click();
}""")
        sleep(3)
        rate_creations = 0
        try:
            rate_creations = int(
                driver.find_element(By.CSS_SELECTOR, ".progress--EYsgARjt")
                .text.split("/")[0]
            )
        except Exception:
            pass
        # if rate_creations == 0:

        # input(rate_creations)


def download():
    pass
    # for profile in chrome.profiles:
    #     seaart.download_images(profile)
    # organizar_fotos("img")


if __name__ == "__main__":
    gerar()
    download()
