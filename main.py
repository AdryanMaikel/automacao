from config import chrome
import seaart
from organizar import organizar_fotos


def gerar_imagens_seaart():
    """
    Gera imagens usando o SeaArt.
    """
    for _, profile in enumerate(chrome.profiles, start=1):
        try:
            seaart.run(profile, False)
        except Exception:
            continue

    while any(profile.credits >= 6 for profile in chrome.profiles):
        for profile in chrome.profiles:
            if profile.credits >= 6:
                try:
                    seaart.run(profile, True)
                except Exception:
                    continue

    for profile in chrome.profiles:
        seaart.download_images(profile)
        organizar_fotos("img")


def __main__():
    gerar_imagens_seaart()


if __name__ == "__main__":
    __main__()
    seaart.close_chrome_if_it_is_running()
