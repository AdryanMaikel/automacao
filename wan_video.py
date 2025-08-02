# from selenium.webdriver.common.action_chains import ActionChains

import random

from seaart import (
    Chrome,
    chrome,
    By,
    sleep,
    os,
    dt,
    get_chrome,
    requests,
    Profile
)

url_wan = "https://wan.video/wanxiang"
url_creation_img = f"{url_wan}/creation"
url_creation_video = f"{url_wan}/videoCreation"


def check_credits(driver: Chrome, sleep_time: int = 3):
    """
    Clica no botão para obter 10 créditos.
    """
    sleep(sleep_time)
    print("Clicando no botão de resgatar créditos...", end="")
    try:
        button = driver.find_element(By.CSS_SELECTOR, ".sc-frmfij.enPVAH")
        if button:
            button.click()
        print("pronto.")
    except Exception:
        print("Falha ao resgatar créditos")


def generate_video(driver: Chrome, profile: Profile, sleep_time: int = 3):
    today = (dt.now()).strftime("%d_%m_%Y")
    cwd = os.getcwd()
    image_folder = os.path.join(cwd, "img", today, "seaart")

    if not os.path.exists(image_folder):
        print(f"Diretório não encontrado: {image_folder}")
        return

    # File to track used images (CSV format)
    used_file_path = "imgs.txt"

    # Read used images
    if os.path.exists(used_file_path):
        with open(used_file_path, "r") as file:
            used_images = file.read().split(",")
    else:
        used_images = []

    # List all image paths in the folder
    all_images = [
        os.path.join(image_folder, file)
        for file in os.listdir(image_folder)
        if file.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    # Filter images that haven't been used yet
    available_images = [img for img in all_images if img not in used_images]

    if not available_images:
        print("Todas as imagens já foram usadas.")
        return

    # Select a random image
    selected_image = random.choice(available_images)

    # Save the selected image path to the tracking file
    with open(used_file_path, "a") as file:
        if used_images and not used_images[-1].endswith(","):
            file.write(",")
        file.write(selected_image)

    print(f"Imagem selecionada: {os.path.basename(selected_image)}")

    upload = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
    if not upload.is_displayed():
        driver.execute_script("""\
document.querySelector('input[type="file"]').style.display = "block";
""")
    sleep(.7)
    upload.send_keys(selected_image)
    print("Esperando imagem carregar")
    while True:
        sleep(5)
        print(".", end="")
        try:
            img = driver.find_element(
                By.XPATH, '//*[@id="img-loader"]/div[2]/picture/img'
                )
            if img.get_attribute("src"):
                print("Imagem carregada.")
            break
        except Exception:
            pass
    sleep(5)

    textarea = driver.find_element(By.CSS_SELECTOR,
                                   ".promptCou--G6gSegXB .ant-input")
    textarea.send_keys(profile.prompt)

    print("Gerando vídeo...", end="")
    try:
        qnt = driver.find_element(By.CSS_SELECTOR, ".sc-fjqcsI.fynqyt")
        if qnt and qnt.text.strip() == "10":
            button = driver.find_element(By.CSS_SELECTOR, ".sc-eKtKts.gyitYm")
            button.click()
            sleep(sleep_time)
            print("pronto.")
    except Exception as e:
        print(e)
        print("Erro ao clicar no botão de gerar vídeo.")


def gerar(sleep_time: int = 3):
    """
    Gera imagens usando o SeaArt.
    """
    for _, profile in enumerate(chrome.profiles, start=1):
        driver = get_chrome(profile)
        if driver.current_url != url_creation_video:
            driver.get(url_creation_video)
        sleep(sleep_time)
        check_credits(driver, sleep_time)
        generate_video(driver, profile, sleep_time)
        sleep(sleep_time)


btn_delete = ".btnLine--kz2jqeAV .btnItem--JUeSIEB8.radius--VPDTvNpv"
confirm_delete = ".item--ZO3gLjE5.ok--hITNHPeQ"


def delete_creation(driver: Chrome):
    print("Procurando lixeiras: ", end="")
    try:
        elements = driver.find_elements(By.CSS_SELECTOR, btn_delete)
    except Exception:
        print("nenhuma lixeira encontrada.")
        return
    print(f"{len(elements)} encontradas.")
    for i, element in enumerate(elements, start=1):
        print(f"Deletando {i}: ", end="")
        try:
            element.click()
            sleep(1)
            driver.find_element(By.CSS_SELECTOR, confirm_delete).click()
            print("pronto.")
            sleep(2)
        except Exception:
            print("falha.")


def download():
    for _, profile in enumerate(chrome.profiles, start=1):
        driver = get_chrome(profile)
        if driver.current_url != url_creation_video:
            driver.get(url_creation_video)
        sleep(5)
        try:
            videos = driver.find_elements(By.CSS_SELECTOR,
                                          ".videoCou--qFqQJn0s video")
        except Exception:
            print("Nenhum vídeo encontrado.")
            return
        for i, video in enumerate(videos, start=1):
            src = video.get_attribute("src")
            filename = f"{profile.name}_{i}.mp4"
            now = dt.now().strftime("%d_%m_%Y")
            if src:
                print("Baixando vídeo...", end="")
                video_path = os.path.join("video", now)
                if not os.path.exists(video_path):
                    os.makedirs(video_path)
                video_path = os.path.join(video_path, filename)
                with open(video_path, "wb") as file:
                    file.write(requests.get(src).content)
                print(f"Vídeo baixado: {filename}")
        delete_creation(driver)
        # input("Aperte enter para continuar")
    # for profile in chrome.profiles:
    #     download_images(profile)
    # organizar_fotos("img")


if __name__ == "__main__":
    gerar()
    # download()
    # print(os.listdir("img/20_05_2025/seaart"))
