from seaart import (
    chrome,
    sleep,
    get_chrome,
    close_chrome_if_it_is_running,
    # click_element,
    requests,
    Profile,
    download_image,
    os, dt,
    Keys
)
from elements import By

import random


prompt = str()
with open("config/prompt.txt", "r") as f:
    prompt = f.read()


def select_image():
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

    available_images = [img for img in all_images if img not in used_images]

    if not available_images:
        print("Todas as imagens já foram usadas.")
        return

    selected_image = random.choice(available_images)

    with open(used_file_path, "a") as file:
        if used_images and not used_images[-1].endswith(","):
            file.write(",")
        file.write(selected_image)

    return selected_image


def gerar_video(profile: Profile, _i: int):
    close_chrome_if_it_is_running()
    driver = get_chrome(profile)
    driver.get("https://www.krea.ai/video")
    # input("Pess enter\n")
    # return
    sleep(3)
    try:
        text = driver.find_element(By.CSS_SELECTOR, ".svelte-gmpzcw").text
        if int(text.strip().split("%")[0]) == 100:
            raise Exception("Energia em 100%")
    except Exception as e:
        print(e)
        return

    print("Colocando para gerar 9x16")
    try:
        driver.find_element(
            By.CSS_SELECTOR,
            ".group\\/promptbox div.relative:nth-of-type(3) button"
        ).click()
    except Exception as e:
        print(f"Erro: {e}")

    sleep(2)

    try:
        driver.execute_script("""\
const input = document.querySelector("#image-upload-1");
input.removeAttribute("hidden");
""")
        # selected_image = select_image()
        path = r"C:\Users\Adryan\Videos\tarot\a fazer"
        selected_image = os.path.join(path, [file for file in os.listdir(path)
                                             if file.endswith(".png")][_i])
        print(f"Imagem selecionada: {os.path.basename(selected_image)}")
        upload = driver.find_element(By.ID, "image-upload-1")
        upload.send_keys(selected_image)
    except Exception:
        print("Erro ao colocar imagem.")

    sleep(2)
    try:
        textarea = driver.find_element(By.ID, "prompt")
        # textarea.send_keys(profile.prompt)
        textarea.send_keys("A woman it's pointing at to the camera")
        textarea.send_keys(Keys.ENTER)
    except Exception:
        print("Erro ao gerar video")
    sleep(3)


def download_videos(profile: Profile):
    close_chrome_if_it_is_running()
    driver = get_chrome(profile)
    driver.get("https://www.krea.ai/video")
    sleep(10)

    try:
        driver.execute_script("""\
document.querySelectorAll('.svelte-ssa8x0[role="menu"] button.group')[1]\
.click()""")

    except Exception:
        print("Sem videos a baixar.")
        return

    sleep(2)

    try:
        videos = driver.find_elements(By.CSS_SELECTOR, "main ul li video")

        for i, video in enumerate(videos, start=1):
            src = video.get_attribute("src")
            filename = f"{profile.name}_{i}.mp4"
            now = dt.now().strftime("%d_%m_%Y")
            if src:
                print("Baixando vídeo...", end="")
                video_path = os.path.join("video", now, "krea")
                if not os.path.exists(video_path):
                    os.makedirs(video_path)
                video_path = os.path.join(video_path, filename)
                with open(video_path, "wb") as file:
                    file.write(requests.get(src).content)
                print(f"Vídeo baixado: {filename}")
    except Exception:
        print("Falha ao baixar videos")
        return

    sleep(1)
    driver.execute_script("""\
document.querySelectorAll('.svelte-ssa8x0[role="menu"] button.group')[1]\
.querySelector("p + p ~ div").click();
""")
    sleep(1)
    driver.execute_script("""\
document.querySelector('.mt-10 button.tooltip-parent:nth-child(2)').click();
""")


def download_images_krea(profile):
    close_chrome_if_it_is_running()
    sleep(3)
    driver = get_chrome(profile)
    driver.get("https://www.krea.ai/image")

    input("Baixar imagem?")
    images = driver.find_elements(By.CSS_SELECTOR, "img.object-contain")
    for i, image in enumerate(images):
        image_url = image.get_attribute("src")
        # print(image_url)
        download_image(image_url, f"{i}", profile.name, "krea")


if __name__ == "__main__":
    for i, profile in enumerate(chrome.profiles):
        # download_images_krea(profile)
        path = r"C:\Users\Adryan\Videos\tarot\a fazer"
        selected_image = os.path.join(path, [file for file in os.listdir(path)
                                             if file.endswith(".png")][i])
        gerar_video(profile, i)
        # download_videos(profile)

        # input("continuar?")
