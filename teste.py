from subprocess import Popen
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
from time import sleep, time

profiles = [
    "maikeladryan",
    "adrynhos2",
    "adryankhn",
    "adryankuhne"
    "adryanmckuhne",
    "WinxRoxa",
    "cco",
    "adryanviu"
]

# Caminhos e perfil
user_data_dir = r"C:\ChromeAutomacao"
profile_name = "adryankhn"

Popen([
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--remote-debugging-port=9222",
    f"--user-data-dir={user_data_dir}",
    f"--profile-directory={profile_name}"
])


def wait_for_debugger(timeout=15):
    end = time() + timeout
    while time() < end:
        try:
            r = requests.get("http://127.0.0.1:9222/json", timeout=1)
            if r.status_code == 200:
                print("Chrome com depuração pronto!")
                return True
        except Exception:
            pass
        sleep(0.5)
    raise RuntimeError("Chrome não respondeu na porta 9222")


wait_for_debugger()

# 3. Conecta com o Selenium
options = Options()
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument(f"--profile-directory={profile_name}")
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

for profile in profiles:
    
    input("proximo")
    

# 4. Testa o controle
driver.get("https://www.google.com")
print("Chrome com perfil controlado com sucesso!")
