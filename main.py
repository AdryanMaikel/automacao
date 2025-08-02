import krea
import wan_video
import seaart


seaart.run_all()

wan_video.gerar()
# wan_video.download()
#     krea.gerar_video(profile)
for profile in krea.chrome.profiles:
    krea.gerar_video(profile)
    krea.download_videos(profile)
