import os
import shutil
import re


def organizar_fotos(path: str):

    # Coleta imagens soltas (não organizadas em subpastas)
    imagens_livres = [f for f in os.listdir(path)
                      if os.path.isfile(os.path.join(path, f))
                      and os.path.splitext(f)[1].lower()]
    imagens_livres.sort()

    if not imagens_livres:
        print("Nenhuma imagem nova encontrada para organizar.")
        return

    # Identifica pastas numeradas e ordena
    pastas = [nome for nome in os.listdir(path)
              if os.path.isdir(os.path.join(path, nome)) and nome.isdigit()]
    pastas.sort(key=lambda x: int(x))

    # Tenta completar pastas existentes primeiro
    for nome_pasta in pastas:
        pasta_path = os.path.join(path, nome_pasta)
        arquivos_existentes = [f for f in os.listdir(pasta_path)
                               if os.path.isfile(os.path.join(pasta_path, f))
                               and os.path.splitext(f)[1].lower()]

        # Usa regex para contar imagens no padrão "img (N).ext"
        padrao = re.compile(r'^img \((\d+)\)\.[a-z0-9]+$', re.IGNORECASE)
        numeros_usados = [int(padrao.match(f).group(1))
                          for f in arquivos_existentes if padrao.match(f)]
        proximo_num = max(numeros_usados, default=0) + 1

        while proximo_num <= 100 and imagens_livres:
            img = imagens_livres.pop(0)
            ext = os.path.splitext(img)[1].lower()
            novo_nome = f"img ({proximo_num}){ext}"
            src = os.path.join(path, img)
            dest = os.path.join(pasta_path, novo_nome)
            print("movendo: ", src, dest)
            shutil.move(src, dest)
            proximo_num += 1

    # Agora cria novas pastas se ainda sobrar imagem
    proxima_pasta = int(pastas[-1]) + 1 if pastas else 1

    while imagens_livres:
        nova_pasta_path = os.path.join(path, str(proxima_pasta))
        os.makedirs(nova_pasta_path, exist_ok=True)

        for i in range(1, 101):
            if not imagens_livres:
                break
            img = imagens_livres.pop(0)
            ext = os.path.splitext(img)[1].lower()
            novo_nome = f"img ({i}){ext}"
            src = os.path.join(path, img)
            dest = os.path.join(nova_pasta_path, novo_nome)
            print("movendo: ", src, dest)
            shutil.move(src, dest)

        print(f"Pasta {proxima_pasta} criada e preenchida.")
        proxima_pasta += 1

    print("Organização concluída!")


if __name__ == "__main__":
    # path_alvo = r"C:\Users\Adryan\Downloads\Videos\imagens\novas"
    # path_alvo = r"C:\Users\Adryan\OneDrive\Desktop\automacao\img"
    organizar_fotos("img")
