from config import chrome
import seaart
# from organizar import organizar_fotos


def gerar():
    """
    Gera imagens usando o SeaArt.
    """
    for _, profile in enumerate(chrome.profiles, start=1):
        try:
            seaart.run(profile, False, False)
        except Exception:
            continue

    while any(profile.credits >= 6 for profile in chrome.profiles):
        for profile in chrome.profiles:
            if profile.credits >= 6:
                try:
                    seaart.run(profile, True, False)
                except Exception:
                    continue


def download():
    for profile in chrome.profiles:
        seaart.download_images(profile)
        # organizar_fotos("img")


if __name__ == "__main__":
    gerar()
    download()
    # seaart.close_chrome_if_it_is_running()
    # organizar_fotos(r"img\12_05_2025")
