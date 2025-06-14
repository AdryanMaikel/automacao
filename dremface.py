from seaart import (
    chrome,
    get_chrome,
    sleep,
    os, dt,
    By,
)

url = "https://tools.dreamfaceapp.com"
url_creations = f"{url}/user"

files_path = r"C:\Users\Adryan\Downloads\A Fazer\Genérico"
bx_path = os.path.join(files_path, "bx")
os.makedirs(bx_path, exist_ok=True)
downloads_path = r"C:\Users\Adryan\Downloads"
dreamface_path = os.path.join(downloads_path, "dreamface")
os.makedirs(dreamface_path, exist_ok=True)

files = [file for file in os.listdir(files_path)
         if os.path.isfile(os.path.join(files_path, file))]

profile = [profile for profile in chrome.profiles
           if profile.name == "maikeladryan"][0]

avatars = []


def gerar():
    driver = get_chrome(profile)
    driver.get(url)
    sleep(3)

    window = driver.current_window_handle

    try:
        avatars = driver.find_elements(By.CSS_SELECTOR,
                                       "._userItem_1uozc_12 img")[:2]
    except Exception:
        print("Falha ao encontrar os avatares")

    for file in files:
        print(f"Processando arquivo: {file}")
        filepath = os.path.join(files_path, file)

        if driver.current_url != url:
            driver.get(url)
            sleep(3)

        avatars[0].click()

        try:
            for div in driver.find_elements(By.CLASS_NAME, "_tab_i12jo_12"):
                if div.text == "Audio":
                    div.click()
        except Exception:
            print("Falha ao selecionar aba de audio")

        try:
            if driver.find_element(By.CLASS_NAME, "_title_fwe9n_12").text:
                driver.find_element(By.CLASS_NAME, "_del_fwe9n_40").click()
        except Exception:
            pass

        try:
            driver.execute_script("""\
document.querySelector('input[type="file"]').removeAttribute('style')""")
            _input_ = driver.find_element(By.CSS_SELECTOR,
                                          'input[type="file"]')
            _input_.send_keys(filepath)
        except Exception:
            print("Falha ao inserir arquivo.")
        sleep(3)

        try:
            driver.find_element(By.CSS_SELECTOR,
                                "._generate_io6io_1 button").click()
        except Exception:
            pass

        count = 0

        print("Esperando gerar.", end="")
        while len(driver.window_handles) == 1:
            sleep(1)
            print(".", end="")
            if count == 10:
                count = 0
                try:
                    driver.find_element(By.CSS_SELECTOR,
                                        "._generate_io6io_1 button").click()
                except Exception:
                    pass
            count += 1
        print()
        sleep(1)

        for handle in driver.window_handles:
            if handle != window:
                new_window = handle
                break

        driver.switch_to.window(new_window)
        sleep(2)
        driver.close()
        driver.switch_to.window(window)
        os.rename(filepath, os.path.join(bx_path, file))


def download():
    now = dt.now().date()
    driver = get_chrome(profile)
    driver.get(url_creations)
    sleep(3)

    if driver.current_url != url_creations:
        driver.get(url_creations)
        sleep(3)

    try:
        div = driver.find_element(By.CLASS_NAME, "_item_13vc9_7")
        if "_active_13vc9_17" not in div.get_attribute("class"):
            div.click()
    except Exception:
        print("Falha ao selecionar aba AVATAR VIDEO.")

    sleep(2)

    try:
        button = driver.find_element(
            By.ID, "radix-vue-tabs-v-0-trigger-Completed"
        )
        if button.get_attribute("data-state").strip() != "active":
            button.click()
    except Exception:
        print("Falha ao selecionar Completed")

    sleep(2)

    while True:
        try:
            card = driver.find_element(By.CLASS_NAME, "_card_1ahg4_1")
        except Exception:
            print("Falha ao encontrar card")
            continue

        driver.execute_script("""\
document.querySelector("._buttons_1ahg4_13").style.display = "flex";""")

        try:
            title, date_element = card.find_elements(
                By.CSS_SELECTOR, "._desc_box_1ahg4_91 p"
            )
            video_name = title.text + ".mp4"
            date = dt.strptime(date_element.text, "%Y-%m-%d %H:%M:%S").date()
            if not date == now:
                print("Video com data diferente de hoje.")
                break

            card.find_element(By.CLASS_NAME, "_button_1e5n8_9").click()
            sleep(2)
            print(f"Esperando baixar {video_name}", end="")
            while video_name not in os.listdir(downloads_path):
                sleep(1)
                print(".", end="")
            print()
            sleep(1)
            if video_name in os.listdir(dreamface_path):
                os.remove(os.path.join(dreamface_path, video_name))

            dst = os.path.join(dreamface_path, video_name.replace(".mp3", ""))
            os.rename(os.path.join(downloads_path, video_name), dst)
            sleep(1)
            card.find_element(By.CSS_SELECTOR, "._button_1e5n8_9~button").\
                click()
            sleep(1)
            card.find_element(By.CLASS_NAME, "_confirm_1e5n8_59").click()
            sleep(2)
        except Exception:
            print("Falha ao processar card")
    driver.close()


if __name__ == "__main__":
    gerar()
    # download()
