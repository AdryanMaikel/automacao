import krea
import wan_video
from config import chrome


if __name__ == "__main__":
    # wan_video.gerar()
    wan_video.download()
    for profile in chrome.profiles:
        # krea.gerar_video(profile)
        krea.download_videos(profile)
