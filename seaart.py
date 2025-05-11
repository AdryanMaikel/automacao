from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webelement import WebElement

from config import seaart, chrome
from config.models import Profile
import elements
import requests
import os

from typing import Union
from subprocess import Popen
from time import sleep
from psutil import process_iter, Process
from datetime import datetime as dt, timezone as tz


def close_chrome_if_it_is_running():
    try:
        for process in process_iter(["pid", "name"]):
            name = process.info.get("name", "").lower()
            if "chrome" in name:
                try:
                    proc = Process(process.pid)
                    proc.kill()
                except Exception as e:
                    print(f"Erro ao encerrar o processo {process.pid}: {e}")
    except Exception as e:
        print(f"Erro ao iterar pelos processos: {e}")


def get_chrome(profile: Profile,
               close_chrome: bool = True,
               open_chrome: bool = True
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


def is_element_present(driver: Chrome,
                       element: dict[str, str] = {},
                       by: By = "",
                       value: str = "",
                       time: int = 0
                       ) -> bool:
    try:
        WebDriverWait(driver, time).until(
            EC.presence_of_element_located(
                locator=(element.get("by", by), element.get("value", value))
            )
        )
        return True
    except Exception:
        return False


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


def click_element(driver: Chrome,
                  element: dict[str, str] = {},
                  by: By = "",
                  value: str = "",
                  time: int = 15,
                  print_error: bool = False
                  ) -> bool:
    try:
        button = WebDriverWait(driver, time).until(
            EC.element_to_be_clickable(
                mark=(element.get("by", by), element.get("value", value))
            )
        )
        if not button:
            raise Exception("botão não encontrado.")
        button.click()
        return True
    except Exception as e:
        print("Erro ao clicar no botão.")
        if print_error:
            print(f"Erro: {e}")
        return False


def get_text_content(element: WebElement) -> str | int:
    text_content = str(element.text).strip()
    if type == int:
        if text_content.isdigit():
            return int(text_content)
    return text_content


def run(profile: Profile, second: bool = False) -> str:
    print(f"Abrindo perfil: {profile.name}")
    driver = get_chrome(profile)
    # input("Rodar perfil?")
    # return
    print("Indo para seaart")
    driver.get(seaart.url)

    # if not second:
    #     input("Clique no bagui")

    sleep(5)
    try:
        driver.execute_script(
            "document.querySelectorAll('.close-btn')[1].click();"
        )
    except Exception as e:
        print(e)
        pass
    #     print("Verificando se o popup está presente: ", end="")
    #     if is_element_present(driver, **elements.close_button, time=10):
    #         try:
    #             sleep(3)
    #             # driver.find_element(**elements.close_button).click()
    #             if click_element(driver, **elements.close_button, time=5):
    #                 print("fechado.")
    #         except Exception:
    #             print("não fechado.")
    #     else:
    #         print("não encontrado.")

    print("Procurando botão de criação: ", end="")
    if not is_element_present(driver, **elements.goto_create, time=5):
        print("não encontrado.")
        return
    try:
        click_element(driver, **elements.goto_create)
        print("clicado.")
    except Exception as e:
        print(f"Erro ao clicar no botão de criação: {e}")
        return

    if not second:
        print("Produrando daily-popup: ", end="")
        if is_element_present(driver, **elements.button_close_popup, time=5):
            try:
                click_element(driver, **elements.button_close_popup)
            except Exception:
                print("não clicado.")
                return
        else:
            print("não encontrado.")

        print("Verificando se tem tem recompensa adicional: ", end="")
        try:
            if is_element_present(driver, **elements.gift, time=5):
                click_element(driver, **elements.gift)
                print("clicado.")
                sleep(3)
                print("Verificando se da pra resgatar: ", end="")
                if is_element_present(driver, **elements.claim, time=5):
                    click_element(driver, **elements.claim)
                    print("clicado.")
                    print("Fechando recompensa.")
                    if is_element_present(driver,
                                          **elements.close_btn, time=5):
                        click_element(driver, **elements.close_btn)
                        print("fechado.")
                    sleep(3)
                else:
                    print("não encontrado.")
        except Exception:
            print("não encontrado.")

    # return

    sleep(5)

    print("Procurando stamina: ", end="")
    if not is_element_present(driver, **elements.stamina, time=5):
        print("não encontrado.")
        return
    try:
        element_stamina = driver.find_element(**elements.stamina)
    except Exception as e:
        print(f"Erro ao encontrar a stamina: {e}")
        return
    stamina = get_text_content(element_stamina)
    if not stamina:
        return
    stamina = int(stamina)
    profile.credits = stamina
    print(stamina)
    chrome.update_json_config()
    if stamina < 6:
        print("stamina insuficiente.")
        return

    # input()

    print(f"Colocando para gerar imagens: {profile.sizeimg} ", end="")
    selector_div_sizes = {"by": By.CLASS_NAME, "value": "panel-item-content-5"}
    selector_panel_item = {"by": By.CLASS_NAME, "value": "panel-item"}
    if not is_element_present(driver, **selector_div_sizes):
        print("Div para alterar tamanho das imagens não encontrada.")
        return False
    div_sizes = driver.find_element(**selector_div_sizes)
    buttons = div_sizes.find_elements(**selector_panel_item)
    for button in buttons:
        type = button.find_element(By.CLASS_NAME, "panel-item-label").text
        if type not in seaart.sizesimg:
            continue
        if type == profile.sizeimg:
            button.click()

    if stamina >= 6:
        qnt_first = 1
        qnt_second = 0

    if stamina >= 12:
        qnt_first = 2
        qnt_second = 0

    if stamina >= 18:
        qnt_first = 3
        qnt_second = 0

    if stamina >= 24:
        qnt_first = 4
        qnt_second = 0

    if stamina >= 30:
        qnt_first = 4
        qnt_second = 1

    if stamina >= 36:
        qnt_first = 4
        qnt_second = 2

    if stamina >= 42:
        qnt_first = 4
        qnt_second = 3

    if stamina >= 48:
        qnt_first = 4
        qnt_second = 4

    print(f"Colocando para gerar {qnt_first} imagens: ", end="")
    div_quantity = driver.find_element(By.CLASS_NAME, "panel-item-content-4")
    buttons = div_quantity.find_elements(**selector_panel_item)

    if len(buttons) < qnt_first:
        print("Quantidade de botões insuficiente.")
        return False

    button_quantity = buttons[qnt_first - 1]

    if not button_quantity:
        print("Botão de quantidade não encontrado")
        return False
    if "active-btn" not in button_quantity.get_attribute("class"):
        button_quantity.click()

    print("Procurando textarea: ", end="")
    if not is_element_present(driver, **elements.textarea):
        print("não encontrado.")
        return
    try:
        textarea = driver.find_element(**elements.textarea)
        if textarea.get_attribute("value"):
            textarea.clear()
        textarea.send_keys(profile.prompt)
    except Exception:
        print("Falha ao escrever prompt.")
        return

    sleep(1)

    # input("CLICAR NO BOTÂO DE GERAR?")

    print("Gerando imagens.")
    driver.execute_script(
        "document.querySelectorAll('.generate-btn')[2].click();"
        )
    sleep(3)

    if qnt_second <= 0:
        return

    sleep(5)

    print(f"Colocando para gerar {qnt_second} imagens: ", end="")
    div_quantity = driver.find_element(By.CLASS_NAME, "panel-item-content-4")
    buttons = div_quantity.find_elements(**selector_panel_item)

    if len(buttons) < qnt_second:
        print("Quantidade de botões insuficiente.")
        return False

    button_quantity = buttons[qnt_second - 1]

    if not button_quantity:
        print("Botão de quantidade não encontrado")
        return False
    if "active-btn" not in button_quantity.get_attribute("class"):
        button_quantity.click()

    print("Procurando textarea: ", end="")
    if not is_element_present(driver, **elements.textarea):
        print("não encontrado.")
        return
    try:
        textarea = driver.find_element(**elements.textarea)
        if textarea.get_attribute("value"):
            textarea.clear()
        textarea.send_keys(profile.prompt)
    except Exception:
        print("Falha ao escrever prompt.")
        return

    sleep(1)
    print("Gerando imagens.")
    driver.execute_script(
        "document.querySelectorAll('.generate-btn')[2].click();"
        )
    sleep(3)


def download_image(url: str, index: int, profile_name: str):
    try:
        date_str = dt.now().strftime("%d_%m_%Y")
        directory = os.path.join(os.getcwd(), "img")
        os.makedirs(directory, exist_ok=True)
        file_name = os.path.join(directory,
                                 f"{profile_name}_{date_str}_{index}.png")

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
    driver.get(seaart.url)

    print("Procurando botão de criação: ", end="")
    if not is_element_present(driver, **elements.goto_create, time=5):
        print("não encontrado.")
        return
    try:
        click_element(driver, **elements.goto_create)
        print("clicado.")
    except Exception as e:
        print(f"Erro ao clicar no botão de criação: {e}")
        return

    sleep(5)

    print("Procurando div de imagens:")

    data_atual = dt.now(tz.utc).strftime("%A, %B %d, %Y")
    print("\n", data_atual, "\n")
    # data_atual = "Tuesday, March 11, 2025"
    # data_atual = (dt.now(tz.utc) - td(days=1)).strftime("%A, %B %d, %Y")
    div_images = driver.find_elements(**elements.div_images)
    scroll_element(driver)
    for i, div in enumerate(div_images):
        if i != 0:
            try:
                text = div.find_element(**elements.text_date_images).text.\
                    strip()
                print(text)
                if text and text != data_atual:
                    print(text)
                    break
            except Exception:
                pass
        try:
            sleep(1)
            images = div.find_elements(**elements.images)
            for j, image in enumerate(images):
                image_url = image.get_attribute("src")
                print(image_url)
                download_image(image_url, f"{i}{j}", profile.name)
        except Exception:
            pass


def scroll_element(driver: Chrome,
                   scroll_pause_time: float = 1.0,
                   increment: int = 500):
    """Rola um elemento específico em incrementos de
400 pixels com uma pausa de 1 segundo."""
    element = driver.find_element(**elements.scroll)
    current_position = 0
    # last_height = driver.execute_script("return arguments[0].scrollHeight",
    #                                     element)

    for _ in range(8):
        driver.execute_script("""\
arguments[0].scrollTo({
    top: """+str(current_position+increment)+""",
    behavior: 'smooth'
});""", element)
        sleep(scroll_pause_time)
        current_position += increment


if __name__ == "__main__":
    for _, profile in enumerate(chrome.profiles, start=1):
        try:
            run(profile, False)
        except Exception:
            continue
