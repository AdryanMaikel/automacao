# from random import uniform
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webelement import WebElement
import requests

from config import chrome
from config.models import Profile
import elements

import os
from typing import Union
from subprocess import Popen
from time import sleep
from psutil import process_iter, Process
from datetime import datetime as dt, timedelta as td, timezone as tz


seaart_url = "https://www.seaart.ai/pt"
seaart_url_image_creation = f"{seaart_url}/create/image"


def close_chrome_if_it_is_running():
    try:
        for process in process_iter(["pid", "name"]):
            name = process.info.get("name", "").lower()
            if "chrome" in name:
                try:
                    proc = Process(process.pid)
                    proc.kill()
                except Exception:
                    pass
    except Exception as e:
        print(f"Erro ao iterar pelos processos: {e}")


def get_chrome(profile: Profile,
               close_chrome: bool = True
               ) -> Union[None, Chrome]:
    if not profile:
        print(f"Perfil não encontrado: {profile.name}")
        return

    if close_chrome:
        close_chrome_if_it_is_running()

        sleep(5)

        print("Abrindo o navegador")
        try:
            Popen([
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                "--remote-debugging-port=9222",
                "--remote-allow-origins=*",
                f"--user-data-dir={chrome.path}",
                f"--profile-directory={profile.name}"
            ])
        except Exception as e:
            input(f"Erro ao abrir o navegador: {e}")
            print("Erro ao abrir o navegador")
            return

    sleep(5)

    try:
        options = Options()
        options.add_argument(f"user-data-dir={chrome.path}")
        options.add_argument(f"profile-directory={profile.name}")
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        for argument in chrome.arguments:
            options.add_argument(argument)
        print("Gerando driver.")
        return Chrome(options, Service(ChromeDriverManager().install()))
    except Exception as e:
        print(f"Erro ao abrir o navegador: {e}")


def element_present_in_element(driver: Chrome,
                               parent_element: WebElement,
                               element: dict[str, str],
                               time: int = 10
                               ) -> bool:
    try:
        WebDriverWait(driver, time).until(
            parent_element.find_element(**element)
        )
        return True
    except Exception:
        return False


def get_text_content(element: WebElement) -> str | int:
    text_content = str(element.text).strip()
    if type == int:
        if text_content.isdigit():
            return int(text_content)
    return text_content


def download_image(url: str, index: int, profile_name: str,
                   folder: str = "seaart"):
    try:
        date_str = dt.now().strftime("%d_%m_%Y")
        directory = os.path.join(os.getcwd(), "img", date_str, folder)
        os.makedirs(directory, exist_ok=True)
        file_name = os.path.join(directory, f"{profile_name}_{index}.png")

        if os.path.exists(file_name):
            print(f"Imagem {file_name} já existe. Pulando download.")
            return

        response = requests.get(url)
        response.raise_for_status()

        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"Imagem baixada e salva como {file_name}")
    except Exception as e:
        print(f"Erro ao baixar a imagem: {e}")


def download_images(profile: Profile):
    print(f"Abrindo perfil: {profile.name}")
    driver = get_chrome(profile)
    print("Indo para seaart")
    driver.get(seaart_url)
    sleep(3)

    try:
        driver.find_element(**elements.goto_create).click()
        print("clicado.")
    except Exception as e:
        print(f"Erro ao clicar no botão de criação: {e}")
        return

    sleep(5)

    print("Procurando div de imagens:")

    dt_now = dt.now(tz.utc) - td(hours=3)
    div_images = driver.find_elements(**elements.div_images)
    scroll_element(driver)
    i = 1
    for div in div_images:
        try:
            text = div.find_element(**elements.text_date_images).text
            if dt.strptime(text, "%A, %B %d, %Y").date() != dt_now.date():
                break
        except Exception:
            pass
        try:
            sleep(1)
            tag = div.find_element(**elements.text_type_creation)
            if tag.text == "Upscaling":
                images = div.find_elements(**elements.images)
                for image in images:
                    image_url = image.get_attribute("src")
                    print(image_url)
                    download_image(image_url, i, profile.name)
                    i += 1
        except Exception:
            pass


def scroll_element(driver: Chrome,
                   scroll_pause_time: float = 1,
                   increment: int = 700,
                   steps: int = 22):
    """Rola um elemento específico em incrementos de
400 pixels com uma pausa de 1 segundo."""
    element = driver.find_element(**elements.scroll)
    current_position = 0

    for _ in range(steps):
        driver.execute_script("""\
arguments[0].scrollTo({
    top: """+str(current_position+increment)+""",
    behavior: 'smooth'
});""", element)
        sleep(scroll_pause_time)
        current_position += increment


def run2(profile: Profile,
         second: bool = False,
         close_chrome: bool = True
         ) -> str:

    if int(profile.credits) < 12 and second:
        return

    print(f"Abrindo perfil: {profile.name}")
    driver = get_chrome(profile, close_chrome=close_chrome)
    driver.maximize_window()
    print("Indo para seaart")
    driver.get(seaart_url)

    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    sleep(3)

    if not second:
        print("fechando popup")
        try:
            driver.find_element(
                By.CSS_SELECTOR,
                ".popup-manager-container .close-btn"
            ).click()
        except Exception:
            print("Falha ao fechar popup")

    sleep(3)

    print("Indo para area de criação")
    try:
        driver.find_element(By.CSS_SELECTOR, ".painting").click()
    except Exception:
        print("falha ao ir para area de criação!")
        raise Exception("Falha ao ir para criação.")

    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    sleep(2)
    if not second:
        try:
            driver.find_element(By.CSS_SELECTOR,
                                ".user-daily .user-daily-close"
                                ).click()
        except Exception:
            print("Erro ao fechar user-daily")

        print("Abrindo baú")
        try:
            driver.find_element(**elements.gift).click()
            sleep(1)
            print("Resgatando recompensa")
            driver.find_element(**elements.claim).click()
            print("Fechando recompensa")
            driver.find_element(**elements.close_btn).click()
            sleep(1)
        except Exception:
            print("Erro ao resgatar recompensa.")

    print("Verificando creditos: ", end="")
    try:
        sleep(5)
        stamina = get_text_content(
            driver.find_element(
                By.CSS_SELECTOR, ".generate-body .stamina .number"
                )
            )
        print(stamina)
        profile.credits = int(stamina)
        chrome.update_json_config()
    except Exception:
        print("falha em localizar a stamina")

    sleep(1)

    if int(profile.credits) < 12:
        print("Sem stamina.")
        return

    print("Clicando para melhorar o prompt.")
    try:
        driver.find_element(
            By.CSS_SELECTOR,
            "div[data-event='generate-magic-mode-open']"
        ).click()
    except Exception:
        print("Erro ao colocar para melhorar prompt")

    sleep(1)

    print("Clicando no tamanho da imagem.")
    try:

        driver.execute_script("""\
document.querySelectorAll(".image-size-options-content-item")[1].click()\
""")
        sleep(1)

        inputs = driver.find_elements(By.CSS_SELECTOR,
                                      ".is-without-controls input")
        if inputs:
            for _ in inputs[0].get_attribute("value"):
                inputs[0].send_keys(Keys.BACKSPACE)
                sleep(0.05)
            inputs[0].send_keys("1024")
            for _ in inputs[1].get_attribute("value"):
                inputs[1].send_keys(Keys.BACKSPACE)
                sleep(0.05)
            inputs[1].send_keys("1024")

    except Exception:
        print("Falha ao colocar em proporção.")

    sleep(1)
    qnt = min(int(profile.credits) // 12, 2)

    print(f"Colocando {qnt} imagens a gerar")
    try:
        div = driver.find_element(By.CLASS_NAME, "panel-item-content-4")
        button = div.find_elements(By.CLASS_NAME, "panel-item")[qnt-1]
        if "active-btn" not in button.get_attribute("class"):
            button.click()
    except Exception:
        print(f"Falha ao clicar para gerar: {qnt}")

    sleep(1)

    print("Esrevendo prompt")
    try:
        textarea = driver.find_element(By.ID, "easyGenerateInput")
        if textarea.get_attribute("value"):
            textarea.clear()
        textarea.send_keys(profile.prompt)
    except Exception:
        print("Falha ao escrever prompt.")
        return

    sleep(1)

    print("Esperando criação.", end="")
    while True:
        try:
            divs = driver.find_elements(By.CSS_SELECTOR, ".c-easy-msg-item")
            total = len(divs)
            for i in range(2 if total > 2 else total):
                divs[i].find_element(By.CSS_SELECTOR, ".media-attachments-img")
            break
        except Exception:
            sleep(1.5)
            print(".", end="")

    try:
        driver.find_element(By.ID, "generate-btn").click()
    except Exception:
        print("Falha ao clicar em gerar")
    sleep(3)

    dt_now = dt.now(tz.utc) - td(hours=3)
    div = None

    while True:
        try:
            div = driver.find_element(By.CSS_SELECTOR, ".c-easy-msg-item")
            text = div.find_element(By.CSS_SELECTOR, ".easy-msg-item-time-box"
                                    ).text
            if dt.strptime(text, "%A, %B %d, %Y").date() != dt_now.date():
                raise Exception(".")
            tag = div.find_element(By.CSS_SELECTOR,
                                   ".msg-item-header-info-panel-tag")
            if tag.text != "Txt2Img":
                raise Exception(".")
            if not div.find_element(By.CSS_SELECTOR, ".media-attachments-img"):
                raise Exception(".")
            print("\nCriado.")
            break
        except Exception:
            print(".", end="")
            sleep(1.5)
            continue

    if not div:
        print("Div não encontrada, algo deu errado.")
        return

    try:
        dialog = driver.find_element(By.CSS_SELECTOR, ".dialog-close")
        if dialog.is_displayed():
            dialog.click()
    except Exception:
        print("Erro ao fechar popup de criação.")

    sleep(2)
    print("Clicando no botão de upscaling: ", end="")
    driver.execute_script("""\
document.querySelectorAll('.image-hover-mask')[0]\
.querySelector('.el-tooltip[data-id="upscale"]').click();""")
    print("pronto")
    sleep(2)

    profile.credits = int(profile.credits) - 6
    chrome.update_json_config()

    if qnt > 1:
        sleep(2)
        print("Clicando no botão de upscaling: ", end="")
        driver.execute_script("""\
document.querySelectorAll('.image-hover-mask')[1]\
.querySelector('.el-tooltip[data-id="upscale"]').click();""")
        print("pronto")
        profile.credits = int(profile.credits) - 6
        chrome.update_json_config()
        sleep(2)


def run_all():
    for _, profile in enumerate(chrome.profiles, start=1):
        try:
            run2(profile)
        except Exception as e:
            run2(profile)
            print(e)
            continue

    while any(int(profile.credits) >= 12 for profile in chrome.profiles):
        for profile in chrome.profiles:
            if int(profile.credits) >= 12:
                try:
                    run2(profile, second=True)
                except Exception:
                    continue

    for _, profile in enumerate(chrome.profiles, start=1):
        download_images(profile)


if __name__ == "__main__":
    run_all()
