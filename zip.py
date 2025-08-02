import os
import zipfile


def encontrar_e_extrair_zip(origem, destino):
    """
    Encontra arquivos .zip em um diretório e os extrai para um destino
    especificado.

    :param origem: Diretório onde os arquivos .zip serão procurados.
    :param destino: Diretório onde os arquivos serão extraídos.
    """
    # Verifica se os caminhos fornecidos existem
    if not os.path.exists(origem):
        print(f"O diretório de origem '{origem}' não existe.")
        return
    if not os.path.exists(destino):
        os.makedirs(destino)
        print(f"O diretório de destino '{destino}' foi criado.")

    for raiz, _, arquivos in os.walk(origem):
        for arquivo in arquivos:
            if arquivo.endswith('.zip'):
                caminho_zip = os.path.join(raiz, arquivo)
                print(f"Encontrado: {caminho_zip}", end="...")
                try:
                    with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
                        zip_ref.extractall(destino)
                        print("extraído!")
                    os.remove(caminho_zip)
                except zipfile.BadZipFile:
                    print(f"Erro ao abrir o arquivo .zip: {caminho_zip}")
                except Exception as e:
                    print(f"Erro: {e}")


if __name__ == "__main__":
    # origem = r"C:\Users\Adryan\Downloads\Videos\imagens\novas"
    # destino = r"C:\Users\Adryan\Downloads\Videos\imagens\novas"
    # encontrar_e_extrair_zip(origem, destino)
    import secrets
    import string


    def generate_password(length=16):
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(chars) for _ in range(length))

    password = generate_password()
    print(password)

     